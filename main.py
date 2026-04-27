import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import time

load_dotenv()

EMAIL = os.getenv("GLASSDOOR_EMAIL")
PASSWORD = os.getenv("GLASSDOOR_PASSWORD")
OUTPUT_FILE = "amazon_systems_engineer_interview_questions.pdf"

# Amazon's Glassdoor company ID is 6036
INTERVIEW_URL = (
    "https://www.glassdoor.com/Interview/"
    "Amazon-Systems-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,23.htm"
)


def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = uc.Chrome(options=options, version_main=147)
    return driver


def close_modal(driver):
    selectors = [
        (By.CSS_SELECTOR, "button[alt='Close']"),
        (By.CSS_SELECTOR, "[class*='modal_closeIcon']"),
        (By.CSS_SELECTOR, "[class*='CloseButton']"),
        (By.XPATH, "//button[contains(@class,'close') or contains(@aria-label,'Close')]"),
    ]
    for by, selector in selectors:
        try:
            btn = driver.find_element(by, selector)
            btn.click()
            time.sleep(0.5)
            return
        except Exception:
            pass


def find_input(driver, wait, selectors):
    for by, value in selectors:
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            continue
    return None


def is_logged_in(driver):
    return "login_input" not in driver.current_url and "sign-in" not in driver.current_url


def login(driver):
    print("Navigating to Glassdoor login...")
    driver.get("https://www.glassdoor.com/profile/login_input.htm")
    time.sleep(3)

    if is_logged_in(driver):
        print("Already logged in — skipping login step.")
        return

    wait = WebDriverWait(driver, 15)

    email_selectors = [
        (By.ID, "inlineUserEmail"),
        (By.NAME, "username"),
        (By.NAME, "email"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[autocomplete='email']"),
        (By.CSS_SELECTOR, "input[autocomplete='username']"),
    ]
    email_field = find_input(driver, wait, email_selectors)

    if email_field is None:
        driver.save_screenshot("login_debug.png")
        raise RuntimeError(
            "Could not find email field. Screenshot saved as login_debug.png — "
            "open it to see what the login page looks like."
        )

    email_field.clear()
    email_field.send_keys(EMAIL)

    try:
        continue_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and not(@disabled)]")
            )
        )
        continue_btn.click()
        time.sleep(2)
    except TimeoutException:
        pass

    password_selectors = [
        (By.ID, "inlineUserPassword"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[autocomplete='current-password']"),
    ]
    password_field = find_input(driver, wait, password_selectors)

    if password_field is None:
        driver.save_screenshot("login_debug.png")
        raise RuntimeError(
            "Could not find password field. Screenshot saved as login_debug.png."
        )

    password_field.send_keys(PASSWORD)

    sign_in_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit' and not(@disabled)]")
        )
    )
    sign_in_btn.click()

    time.sleep(4)
    print("Login complete.")


def expand_all_show_more(driver):
    """Click every expand button on the page to reveal hidden content."""
    css_selectors = [
        "[data-test='interview-source-show-more']",
    ]
    xpath_selectors = [
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mostrar')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more')]",
        "//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'mostrar todo')]",
        "//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show all')]",
    ]
    clicked = 0
    for sel in css_selectors:
        for btn in driver.find_elements(By.CSS_SELECTOR, sel):
            try:
                driver.execute_script("arguments[0].click();", btn)
                clicked += 1
                time.sleep(0.4)
            except Exception:
                pass
    for xpath in xpath_selectors:
        for btn in driver.find_elements(By.XPATH, xpath):
            try:
                driver.execute_script("arguments[0].click();", btn)
                clicked += 1
                time.sleep(0.4)
            except Exception:
                pass
    if clicked:
        print(f"  Expanded {clicked} 'Show more' section(s).")
        time.sleep(1.5)


def extract_questions_from_page(driver):
    found = []

    # Each interview entry has a unique ID pattern; grab all of them
    import re
    page_src = driver.page_source
    interview_ids = list(dict.fromkeys(re.findall(r'Interview(\d+)', page_src)))

    for iid in interview_ids:
        entry_text = []

        # Main question container
        q_container = driver.find_elements(
            By.CSS_SELECTOR, f"[data-test='Interview{iid}ApplicationDetails'] [data-test='interview-question-container']"
        )
        if not q_container:
            q_container = driver.find_elements(By.CSS_SELECTOR, "[data-test='interview-question-container']")

        for el in q_container:
            t = el.text.strip()
            if t and len(t) > 10:
                entry_text.append(t)

        # Expanded process/source section
        process = driver.find_elements(
            By.CSS_SELECTOR, f"[data-test='Interview{iid}Process']"
        )
        for el in process:
            t = el.text.strip()
            if t and len(t) > 10:
                entry_text.append(t)

        if entry_text:
            combined = "\n".join(dict.fromkeys(entry_text))
            if combined not in found:
                found.append(combined)

    # Fallback: grab all question containers if per-entry scraping found nothing
    if not found:
        for sel in ["[data-test='interview-question-container']", "[data-test='question-container']"]:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            candidates = [el.text.strip() for el in elements if el.text.strip() and len(el.text.strip()) > 10]
            if candidates:
                found = candidates
                break

    return found


def is_blocked(driver):
    blocked_phrases = [
        "just a moment", "un momento", "humans only", "solo personas reales",
        "real people only", "unauthorized", "access denied",
        "verif", "ser humano", "not a robot", "checking your browser",
        "please wait", "ray id", "cloudflare"
    ]
    content = (driver.title + " " + driver.page_source[:3000]).lower()
    return any(phrase in content for phrase in blocked_phrases)


def wait_for_user_if_blocked(driver):
    if is_blocked(driver):
        print("\n" + "="*60)
        print("CAPTCHA detected in the Chrome window.")
        print("Please solve it manually in the browser, then come back here.")
        input("Press ENTER once the page has fully loaded...")
        print("="*60 + "\n")


def scrape_questions(driver):
    print("Navigating to Amazon company page first...")
    driver.get("https://www.glassdoor.com/Overview/Working-at-Amazon-EI_IE6036.11,17.htm")
    time.sleep(4)
    wait_for_user_if_blocked(driver)

    print("Navigating to interviews page...")
    driver.get(INTERVIEW_URL)
    time.sleep(5)
    wait_for_user_if_blocked(driver)
    time.sleep(2)

    # Save HTML after any CAPTCHA is cleared so we capture real page content
    with open("interview_page_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    wait = WebDriverWait(driver, 15)
    all_questions = []
    page = 1

    while True:
        time.sleep(3)
        close_modal(driver)
        expand_all_show_more(driver)

        page_questions = extract_questions_from_page(driver)
        new_count = 0
        for q in page_questions:
            if q not in all_questions:
                all_questions.append(q)
                new_count += 1

        print(f"Page {page}: +{new_count} new questions (total: {len(all_questions)})")

        if page == 1 and new_count == 0:
            driver.save_screenshot("interview_page_debug.png")
            print("No questions found on page 1. Saved debug files.")
            break

        try:
            next_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='next-page']"))
            )
            driver.execute_script("arguments[0].click();", next_btn)
            page += 1
            time.sleep(2)
            wait_for_user_if_blocked(driver)
        except TimeoutException:
            print("No more pages found.")
            break

    return all_questions


def save_to_pdf(questions, filename=OUTPUT_FILE):
    # If file is open/locked, append a number to avoid permission error
    if os.path.exists(filename):
        try:
            open(filename, "ab").close()
        except PermissionError:
            base, ext = os.path.splitext(filename)
            i = 2
            while os.path.exists(f"{base}_{i}{ext}"):
                i += 1
            filename = f"{base}_{i}{ext}"
            print(f"Original file is open — saving to {filename} instead.")

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=colors.HexColor("#00a67e"),
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.grey,
        spaceAfter=20,
    )
    question_style = ParagraphStyle(
        "Question",
        parent=styles["Normal"],
        fontSize=11,
        leading=17,
        spaceAfter=12,
    )

    content = []

    content.append(Paragraph("Amazon — Systems Engineer", title_style))
    content.append(Paragraph("Interview Questions scraped from Glassdoor", subtitle_style))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    content.append(Spacer(1, 0.2 * inch))
    content.append(
        Paragraph(f"Total questions collected: <b>{len(questions)}</b>", subtitle_style)
    )
    content.append(Spacer(1, 0.15 * inch))

    for i, question in enumerate(questions, 1):
        safe_q = (
            question.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        content.append(Paragraph(f"<b>{i}.</b> {safe_q}", question_style))

    doc.build(content)
    print(f"\nPDF saved: {filename}")


if __name__ == "__main__":
    driver = setup_driver()
    try:
        login(driver)
        questions = scrape_questions(driver)

        if not questions:
            print(
                "\nNo questions were extracted. Glassdoor may have changed its page "
                "structure. Try running without headless mode and inspect the page manually."
            )
        else:
            print(f"\nTotal unique questions collected: {len(questions)}")
            save_to_pdf(questions)
            print(f"Open '{OUTPUT_FILE}' to review the questions.")
    finally:
        driver.quit()
