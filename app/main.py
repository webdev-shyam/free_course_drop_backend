from fastapi import FastAPI
from .scraper import get_udemy_courses
from .database import courses_collection

app = FastAPI(title="Udemy Course API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/courses")
def get_all_courses():
    return list(courses_collection.find({}, {"_id": 0}))

@app.get("/courses/latest")
def get_latest_courses():
    return list(courses_collection.find({}, {"_id": 0}).sort("_id", -1).limit(10))

@app.get("/courses/category/{category}")
def get_courses_by_category(category: str):
    return list(courses_collection.find({"category": category}, {"_id": 0}))

@app.get("/scrape")
def scrape_now():
    return {"new_courses": get_udemy_courses()}
