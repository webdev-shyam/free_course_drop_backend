from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")  # Add your connection string in Render environment
client = MongoClient(MONGO_URL)
db = client["udemy_courses_db"]
courses_collection = db["courses"]

# Optional: create unique index to prevent duplicates
courses_collection.create_index("url", unique=True)
