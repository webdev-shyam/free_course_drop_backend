import requests
from bs4 import BeautifulSoup
from .database import courses_collection
import logging

logging.basicConfig(level=logging.INFO)

def get_udemy_courses():
    logging.info("🔍 Starting Udemy scraping...")
    url = "https://www.udemy.com/courses/search/?price=price-free"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Udemy page: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    courses = []

    for card in soup.select(".course-card--container--3w8Zm"):
        title = card.select_one(".course-card--course-title--2f7tE")
        link = card.select_one("a.udlite-custom-focus-visible")
        thumbnail = card.select_one("img")
        if title and link and thumbnail:
            course = {
                "title": title.text.strip(),
                "url": "https://www.udemy.com" + link['href'],
                "couponCode": None,
                "thumbnail": thumbnail['src'],
                "category": "Programming",
                "posted_to_telegram": False
            }
            # Avoid duplicates
            if not courses_collection.find_one({"url": course["url"]}):
                courses_collection.insert_one(course)
                courses.append(course)

    logging.info(f"✅ Scraping done. {len(courses)} new courses added.")
    return courses
