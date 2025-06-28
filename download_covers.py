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
    "A Court of Frost and Starlight (A Court of Thorns and Roses, #3.5)": "50659471",
    "Even Exchange (Crystal Bay University, #3)": "222085096",
    "A Curse for True Love (Once Upon a Broken Heart, #3)": "62816044",
    "A Cursed Age": "218652630",
    "Queen of Vengeance: An Enemies to Lovers Bad Boy Romance (Hand of Revenge Book 2)": "230847565",
    "A Gorgeous Villain (St. Mary’s Rebels #2)": "55237214",
    "A Lie for a Lie (All In, #1)": "44776456",
    "A Love Letter to Whiskey": "31549837",
    "Aftermath (Fractured Pasts Book 1)": "222664799",
    "All I Need (The Knights, #1)": "200320170",
    "All the Little Lies (English Prep #1)": "57142706",
    "Bananapants": "209318939",
    "Blind Side (Red Zone Rivals, #2)": "60633773",
    "Boneyard Tides (Aphotic Waters Trilogy #1)": "127317830",
    "Butcher & Blackbird (The Ruinous Love Trilogy, #1)": "196915235",
    "Could Have Been Us (Willow Creek Valley, #2)": "55809364",
    "Darling Venom": "59766350",
    "Deep End": "212808709",
    "Deeply Personal": "220509754",
    "Don't Kiss the Bride": "56894372",
    "Falling on a Duke": "230588249",
    "Finding You in the Dark": "228050519",
    "Gild (The Plated Prisoner, #1)": "56483061",
    "Gleam (The Plated Prisoner, #3)": "57214537",
    "Glint (The Plated Prisoner, #2)": "56530123",
    "Glow (The Plated Prisoner, #4)": "58159316",
    "Home Game (Vancouver Wolves Hockey, #2)": "45170561",
    "How to Kill Your Family": "50224049",
    "In a Jam (Friendship, Rhode Island #1)": "62597278",
    "In the Unlikely Event": "48847096",
    "It Happened One Summer (Bellinger Sisters, #1)": "55659629",
    "Kiss of the Vampire: A Forbidden Lovers Vampire Romance (The Vampire's Kingdom)": "228097471",
    "Kulti": "24044596",
    "Leather & Lark (The Ruinous Love Trilogy, #2)": "127611580",
    "Long Live Evil (Time of Iron, #1)": "201626991",
    "Love and Other Words": "36206591",
    "Midnight Blue": "36376514",
    "Moonlit Thorns (Midnight Manor #1)": "205713620",
    "My Dark Romeo (Dark Prince Road, #1)": "123008168",
    "My Roommate Is a Vampire (My Vampires, #1)": "60041932",
    "Nightshade (Sorrowsong University #1)": "224044336",
    "Once upon a Boyband: Boy Band Series, Book 1": "226094433",
    "One Percent of You": "43701279",
    "P.S. I'm Still Yours": "63252796",
    "Purple Hearts": "30753721",
    "Rally (Treasure State Wildcats, #3)": "208955995",
    "Runaway Love (Cherry Tree Harbor, #1)": "123244793",
    "Tell Me What You Want": "200024487",
    "Ten Trends to Seduce Your Bestfriend": "59979662",
    "Thank You for Listening": "59314703",
    "The Breakaway (Campus Confessions Book 1)": "220631669",
    "The Brightest Light of Sunshine (The Brightest Light, #1)": "63831009",
    "The Love Hypothesis": "56732449",
    "The Reluctant Bride (Arranged Marriage, #1)": "58927051",
    "The Vampires Will Save You (Pandemic Monsters, #1)": "59425148",
    "Two Can Play": "217108838",
    "We Can't Be Friends (Close To You)": "222312831",
    "When Alec Met Evie (Appies, #6)": "223634485",
    "Wild Love (Rose Hill, #1)": "199368721",
    "Wildest Dreams (Forbidden Love, #2)": "217068061",
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
