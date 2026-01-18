from pymongo import MongoClient
import os
import certifi

MONGO_URI = os.getenv("MONGO_URI")  # Use this in Render secrets

# Connect with SSL certificate verification
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

# Use your database
db = client["udemy_courses_db"]
courses_collection = db["courses"]

# Ensure unique index
courses_collection.create_index("url", unique=True)
