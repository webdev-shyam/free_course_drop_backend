from fastapi import FastAPI
from .scraper import get_udemy_courses
from .database import courses_collection
from .scheduler import scheduler

app = FastAPI(title="Udemy Course API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/courses")
def get_all_courses():
    courses = list(courses_collection.find({}, {"_id": 0}))
    return courses

@app.get("/courses/latest")
def get_latest_courses():
    courses = list(courses_collection.find({}, {"_id": 0}).sort("_id", -1).limit(10))
    return courses

@app.get("/courses/category/{category}")
def get_courses_by_category(category: str):
    courses = list(courses_collection.find({"category": category}, {"_id": 0}))
    return courses

@app.get("/scrape")
def scrape_now():
    return {"new_courses": get_udemy_courses()}
