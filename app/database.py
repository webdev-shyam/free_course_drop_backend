import os
import certifi
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI not set")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000
)

db = client["udemy_courses_db"]
courses_collection = db["courses"]

# Force connection test
client.admin.command("ping")

print("✅ MongoDB connected successfully")
