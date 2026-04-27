# Glassdoor Interview Scraper

Scrapes Amazon Systems Engineer interview questions from Glassdoor and exports them to a PDF, ready to use as context for LLM-based interview prep.

## Prerequisites

- Python 3.8+
- Google Chrome installed
- A Glassdoor account

## Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd GlassdoorScraperWSelenium

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root (never commit this):

```
GLASSDOOR_EMAIL=your_email@example.com
GLASSDOOR_PASSWORD=your_password
```

## Usage

```bash
python main.py
```

A Chrome window will open automatically. If a CAPTCHA appears, solve it manually in the browser and press **Enter** in the terminal to continue. The scraper will then page through all interview results automatically.

## Output

The script saves a PDF file named `amazon_systems_engineer_interview_questions.pdf` in the project directory. This file contains all scraped interview questions and can be uploaded directly as context to any LLM (ChatGPT, Claude, etc.) for interview preparation.

## Notes

- The scraper uses `undetected-chromedriver` to bypass bot detection
- Glassdoor may occasionally require a manual CAPTCHA solve
- Only the first run requires CAPTCHA; subsequent runs may pass automatically
