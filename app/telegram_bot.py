import os
from dotenv import load_dotenv
from telegram import Bot
from .database import courses_collection
import logging

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)

def post_to_telegram():
    courses = list(courses_collection.find({"posted_to_telegram": False}).limit(1))
    if not courses:
        logging.info("No new courses to post.")
        return

    for course in courses:
        message = f"*{course['title']}*\nCategory: {course['category']}\n[Enroll Now]({course['url']})"
        try:
            bot.send_photo(chat_id=CHAT_ID, photo=course['thumbnail'], caption=message, parse_mode="Markdown")
            courses_collection.update_one({"_id": course["_id"]}, {"$set": {"posted_to_telegram": True}})
            logging.info(f"✅ Posted to Telegram: {course['title']}")
        except Exception as e:
            logging.error(f"Failed to post {course['title']} to Telegram: {e}")
