# Glassdoor Interview Scraper

A Selenium-based scraper that collects interview questions from any Glassdoor interview page and exports them to a PDF. Feed the PDF to any LLM (ChatGPT, Claude, etc.) and use it to prepare for your interviews more effectively.

## Prerequisites

- Python 3.8+
- Google Chrome installed
- A Glassdoor account

## Getting Started

### 1. Clone the repo and install dependencies

```bash
git clone <your-repo-url>
cd GlassdoorScraperWSelenium

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 2. Create a `.env` file with your Glassdoor credentials

Create a file named `.env` in the project root (this file is gitignored — your credentials will never be committed):

```
GLASSDOOR_EMAIL=your_email@example.com
GLASSDOOR_PASSWORD=your_password
```

### 3. Find the Glassdoor URL for the role you want

1. Go to [glassdoor.com](https://www.glassdoor.com) and search for the company
2. Go to their company profile and click the **Interviews** tab
3. Filter by the job title you are interviewing for
4. Copy the URL from your browser

### 4. Update `main.py` with your URL and output filename

Open `main.py` and edit these two lines at the top:

```python
INTERVIEW_URL = "paste your Glassdoor URL here"
OUTPUT_FILE = "my_interview_questions.pdf"
```

### 5. Run the scraper

```bash
python main.py
```

A Chrome window will open automatically. If a CAPTCHA appears:
- Solve it manually in the browser
- Come back to the terminal and press **Enter**

The scraper will then page through all results automatically — no further input needed.

### 6. Use the PDF to prepare

A PDF will be saved in the project folder with all the scraped questions. Upload it to any LLM and ask it to help you prepare — practice answers, anticipate follow-ups, or run a mock interview.

## Notes

- The scraper uses `undetected-chromedriver` to bypass bot detection
- Glassdoor may occasionally require a manual CAPTCHA solve — this is the only manual step
- Pagination is handled automatically, so you don't need to configure the number of pages
- `.env` is excluded from git — your credentials will never be committed
