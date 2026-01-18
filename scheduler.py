from apscheduler.schedulers.blocking import BlockingScheduler
from app.scraper import scrape_discudemy
from app.telegram_bot import post_to_telegram
import logging
import pytz

logging.basicConfig(level=logging.INFO)

scheduler = BlockingScheduler(timezone=pytz.UTC)

# Scraper every 4 hours
scheduler.add_job(scrape_discudemy, 'interval', hours=4, id="udemy_scraper")

# Telegram posting every 2.5 hours
scheduler.add_job(post_to_telegram, 'interval', hours=2, minutes=30, id="telegram_poster")

logging.info("🚀 Scheduler worker started: scraper + Telegram bot")
scheduler.start()
