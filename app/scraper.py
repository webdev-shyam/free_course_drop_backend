import requests
from bs4 import BeautifulSoup
from .database import courses_collection
import logging
import re
import time

logging.basicConfig(level=logging.INFO)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

DISCUDMY_URL = "https://www.discudemy.com/all"

def extract_slug(udemy_url: str) -> str | None:
    """
    https://www.udemy.com/course/python-for-beginners/?couponCode=FREE
    -> python-for-beginners
    """
    match = re.search(r"/course/([^/]+)/", udemy_url)
    return match.group(1) if match else None


def fetch_udemy_thumbnail(slug: str) -> tuple[str | None, str | None]:
    """
    Fetch thumbnail + category from Udemy public API
    """
    api_url = "https://www.udemy.com/api-2.0/courses/"
    params = {
        "search": slug,
        "page_size": 1
    }

    try:
        r = requests.get(api_url, headers=HEADERS, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        if data.get("results"):
            course = data["results"][0]
            thumbnail = course.get("image_480x270")
            category = course.get("primary_category", {}).get("title")
            return thumbnail, category

    except Exception as e:
        logging.warning(f"Udemy API failed for {slug}: {e}")

    return None, None


def scrape_discudemy():
    logging.info("🔍 Scraping DiscUdemy...")

    r = requests.get(DISCUDMY_URL, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    cards = soup.select(".card")

    new_courses = []

    for card in cards:
        title_el = card.select_one(".card-header")
        link_el = card.select_one("a")

        if not title_el or not link_el:
            continue

        title = title_el.text.strip()
        discudemy_link = link_el["href"]

        # Step 1: open DiscUdemy redirect page
        try:
            redirect_page = requests.get(discudemy_link, headers=HEADERS, timeout=15)
            redirect_page.raise_for_status()
        except:
            continue

        redirect_soup = BeautifulSoup(redirect_page.text, "html.parser")
        udemy_btn = redirect_soup.select_one("a.btn.btn-primary")

        if not udemy_btn:
            continue

        udemy_url = udemy_btn["href"]
        slug = extract_slug(udemy_url)

        if not slug:
            continue

        # Avoid duplicates early
        if courses_collection.find_one({"url": udemy_url}):
            continue

        thumbnail, category = fetch_udemy_thumbnail(slug)

        course = {
            "title": title,
            "url": udemy_url,
            "thumbnail": thumbnail,
            "category": category or "General",
            "posted_to_telegram": False,
            "source": "discudemy"
        }

        courses_collection.insert_one(course)
        new_courses.append(course)

        logging.info(f"✅ Added: {title}")

        time.sleep(1)  # be polite

    logging.info(f"🎉 Scraping finished. {len(new_courses)} new courses added.")
    return new_courses
