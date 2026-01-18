from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from .database import courses_collection
from .scraper import scrape_discudemy
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Udemy Course API", version="0.1.0")

# -----------------------------
# CORS middleware
# @app.get("/scrape")
# def scrape_now():
#     new_courses = scrape_discudemy()
#     return {"new_courses": new_courses}


app = FastAPI(title="Udemy Course API", version="0.1.0")

@app.get("/scrape")
def debug_scrape():
    url = "https://www.discudemy.com/category/development"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    r = requests.get(url, headers=headers, timeout=30)

    return {
        "status_code": r.status_code,
        "html_length": len(r.text),
        "preview": r.text[:700]
    }
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV: "*" is fine, replace with frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -----------------------------
# Scrape now
# -----------------------------


# -----------------------------
# Get all courses
# -----------------------------
@app.get("/courses")
def get_all_courses():
    try:
        courses = list(courses_collection.find())
        for c in courses:
            c["_id"] = str(c["_id"])
        return courses
    except Exception as e:
        logging.error(f"Failed to fetch courses: {e}")
        return {"detail": f"Error fetching courses: {e}"}

# -----------------------------
# Get latest courses
# -----------------------------
@app.get("/courses/latest")
def get_latest_courses():
    try:
        courses = list(courses_collection.find().sort("createdAt", -1).limit(20))
        for c in courses:
            c["_id"] = str(c["_id"])
        return courses
    except Exception as e:
        logging.error(f"Failed to fetch latest courses: {e}")
        return {"detail": f"Error fetching latest courses: {e}"}

# -----------------------------
# Get courses by category
# -----------------------------
@app.get("/courses/category/{category}")
def get_courses_by_category(category: str):
    try:
        courses = list(courses_collection.find({"category": category}))
        for c in courses:
            c["_id"] = str(c["_id"])
        return courses
    except Exception as e:
        logging.error(f"Failed to fetch courses by category '{category}': {e}")
        return {"detail": f"Error fetching courses by category: {e}"}
