from apscheduler.schedulers.blocking import BlockingScheduler
from app.scraper import get_udemy_courses
from app.telegram_bot import post_to_telegram
import logging

logging.basicConfig(level=logging.INFO)

scheduler = BlockingScheduler()

# Scraper every 4 hours
scheduler.add_job(get_udemy_courses, 'interval', hours=4, id="udemy_scraper")

# Telegram posting every 2.5 hours
scheduler.add_job(post_to_telegram, 'interval', hours=2, minutes=30, id="telegram_poster")

logging.info("🚀 Scheduler worker started: scraper + Telegram bot")
scheduler.start()
