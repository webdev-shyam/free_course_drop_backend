import requests
from bs4 import BeautifulSoup
from .database import courses_collection
import logging
from datetime import datetime

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

    # Debug logs
    logging.info(f"HTML length: {len(r.text)}")
    logging.info(f"Page title: {soup.title.text if soup.title else 'No title'}")
    logging.info(f"All <a> tags found: {len(soup.find_all('a'))}")

    courses = []

    # Scrape course links
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/course/" in href:
            title_tag = a_tag.find("div")
            img_tag = a_tag.find("img")
            if title_tag and img_tag:
                course_url = "https://www.udemy.com" + href.split("?")[0]
                course = {
                    "title": title_tag.text.strip(),
                    "url": course_url,
                    "couponCode": None,
                    "thumbnail": img_tag.get("src") or "",
                    "category": "Programming",
                    "posted_to_telegram": False,
                    "createdAt": datetime.utcnow()
                }

                # Avoid duplicates
                if not courses_collection.find_one({"url": course["url"]}):
                    courses_collection.insert_one(course)
                    courses.append(course)

    logging.info(f"✅ Scraping done. {len(courses)} new courses added.")
    return courses
