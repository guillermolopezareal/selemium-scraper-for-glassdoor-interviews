# Glassdoor Interview Scraper

A Selenium-based scraper that collects interview questions from any Glassdoor interview page and exports them to a PDF. Feed the PDF to any LLM (ChatGPT, Claude, etc.) and use it to prepare for your interviews more effectively.

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

## Customization

To scrape a different role or company, open `main.py` and update these two variables at the top of the file:

```python
# The Glassdoor interview questions URL for the role/company you want
INTERVIEW_URL = "https://www.glassdoor.com/Interview/..."

# Name of the output PDF
OUTPUT_FILE = "my_interview_questions.pdf"
```

**How to get the right URL:**
1. Go to [glassdoor.com](https://www.glassdoor.com)
2. Search for the company, go to their profile, and click the **Interviews** tab
3. Filter by the job title you are interviewing for
4. Copy the URL from your browser and paste it as `INTERVIEW_URL`

Glassdoor paginates results — the scraper automatically follows all pages until there are no more results, so you don't need to configure the page count manually.

## Usage

```bash
python main.py
```

A Chrome window will open automatically. If a CAPTCHA appears, solve it manually in the browser and press **Enter** in the terminal to continue. The scraper will then page through all results automatically.

## Output

A PDF file is saved in the project directory with all the scraped interview questions. Upload it as context to any LLM and ask it to help you prepare — practice answers, anticipate follow-ups, or simulate a mock interview.

## Notes

- The scraper uses `undetected-chromedriver` to bypass bot detection
- Glassdoor may occasionally require a manual CAPTCHA solve
- `.env` is excluded from git — your credentials will never be committed
