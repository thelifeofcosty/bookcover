import os
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# ─── Silence the LibreSSL/OpenSSL warning ───────────────────────────────────────
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from apify import Actor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def main():
    # ─── Read user input ─────────────────────────────────────────────────────────
    input = await Actor.get_input()
    books = input["books"]  # list of { "title": ..., "id": ... }

    # ─── Prepare storage folder ───────────────────────────────────────────────────
    # Apify provides APIFY_STORAGE_DIR or datasets folder
    output_dir = os.path.join(os.getenv("APIFY_STORAGE_DIR", "/tmp"), "covers")
    os.makedirs(output_dir, exist_ok=True)
    print("Saving covers into:", output_dir)

    # ─── Build the map ────────────────────────────────────────────────────────────
    book_id_map = { b["title"]: b["id"] for b in books }

    # ─── Selenium setup ──────────────────────────────────────────────────────────
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(options=options)

    # ─── Helper to download an image ──────────────────────────────────────────────
    def download_image(url, filename):
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Downloaded: {filename}")
        else:
            print(f"❌ Failed to download {url}")

    base_url = "https://www.goodreads.com/book/show/"

    # ─── Main loop ────────────────────────────────────────────────────────────────
    for title, book_id in book_id_map.items():
        print(f"🔍 Fetching cover for: {title}")
        driver.get(base_url + book_id)

        try:
            elm = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.BookCover__image img"))
            )
            img_url = elm.get_attribute("src")
            safe = "".join(c for c in title if c.isalnum() or c in (" ", "_")).rstrip()
            path = os.path.join(output_dir, f"{safe}.jpg")
            download_image(img_url, path)

        except Exception as e:
            print(f"❌ Error processing {title}: {e}")

    driver.quit()

    # ─── Push results (list of saved files) ──────────────────────────────────────
    saved = os.listdir(output_dir)
    await Actor.push_data({ "saved_files": saved })

if __name__ == "__main__":
    Actor.run(main)
