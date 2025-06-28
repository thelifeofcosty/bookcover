import os
import warnings
from urllib3.exceptions import NotOpenSSLWarning

# ─── Silence the LibreSSL/OpenSSL warning ───────────────────────────────────────
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ─── Define output directory (expands ~ to your home dir) ───────────────────────
output_dir = os.path.expanduser("~/Desktop/Cover")
print("Saving covers into:", output_dir)   # <<< add this for debug
os.makedirs(output_dir, exist_ok=True)

# ─── Goodreads book ID mapping ─────────────────────────────────────────────────
book_id_map = {
    Wildest Dreams (Forbidden Love, #2)": "217068061",
}

# ─── Goodreads base URL ────────────────────────────────────────────────────────
base_url = "https://www.goodreads.com/book/show/"

# ─── Set up Selenium WebDriver (headless) ───────────────────────────────────────
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
driver = webdriver.Chrome(options=options)

def download_image(url, filename):
    """Download image from URL and save it locally."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"✅ Downloaded: {filename}")
    else:
        print(f"❌ Failed to download image from {url}")

# ─── Main loop ────────────────────────────────────────────────────────────────
for book, book_id in book_id_map.items():
    print(f"🔍 Fetching cover for: {book}")
    driver.get(base_url + book_id)

    try:
        cover_img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.BookCover__image img"))
        )
        img_url = cover_img.get_attribute("src")

        # sanitize filename
        safe_title = "".join(c for c in book if c.isalnum() or c in (" ", "_")).rstrip()
        image_path = os.path.join(output_dir, f"{safe_title}.jpg")

        download_image(img_url, image_path)

    except Exception as e:
        print(f"❌ Error processing {book}: {e}")

# ─── Clean up ──────────────────────────────────────────────────────────────────
driver.quit()
