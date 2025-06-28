
# Bookcover Downloader

A headless-Chrome scraper that downloads Goodreads book covers to `~/Desktop/Cover`.

## Prerequisites

- Python 3.8+ installed  
- Chrome browser  
- ChromeDriver on your PATH (`brew install chromedriver`)

## 🔧 Customizing your book list

By default, `download_covers.py` comes with a pre-filled `book_id_map`, but you can easily make it your own.  

1. **Find the Goodreads ID**  
   - Go to any book’s page on Goodreads (e.g. https://www.goodreads.com/book/show/217068061)  
   - The number at the end (`217068061`) is its ID.  

2. **Edit the `book_id_map`**  
   Open `download_covers.py` and look for the block:

   ```python
   book_id_map = {
       "Wildest Dreams (Forbidden Love, #2)": "217068061",
       # add your entries below
   }

## Installation

```bash
git clone https://github.com/thelifeofcosty/bookcover.git
cd bookcover
python3 -m venv venv             # optional but recommended
source venv/bin/activate
pip install -r requirements.txt
