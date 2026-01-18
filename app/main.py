from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import courses_collection
from .scraper import get_udemy_courses
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Udemy Course API", version="0.1.0")

# -----------------------------
# CORS middleware
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
@app.get("/scrape")
def scrape_now():
    try:
        new_courses = get_udemy_courses()
        return {"new_courses": new_courses}
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return {"detail": f"Scraping failed: {e}"}

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
