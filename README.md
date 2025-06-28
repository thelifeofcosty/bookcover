
# Bookcover Downloader

A headless-Chrome scraper that downloads Goodreads book covers to `~/Desktop/Cover`.

## Prerequisites

- Python 3.8+ installed  
- Chrome browser  
- ChromeDriver on your PATH (`brew install chromedriver`)

## Installation

```bash
git clone https://github.com/thelifeofcosty/bookcover.git
cd bookcover
python3 -m venv venv             # optional but recommended
source venv/bin/activate
pip install -r requirements.txt
