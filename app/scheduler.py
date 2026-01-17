from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import get_udemy_courses
from .telegram_bot import post_to_telegram
import logging

logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()
scheduler.add_job(get_udemy_courses, 'interval', hours=4, id="udemy_scraper")
scheduler.add_job(post_to_telegram, 'interval', hours=2, minutes=30, id="telegram_poster")

scheduler.start()
logging.info("📅 Scheduler started: Scraper every 4h, Telegram every 2.5h")
