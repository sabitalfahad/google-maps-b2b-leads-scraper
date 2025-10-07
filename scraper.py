from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import time, re, pandas as pd

# User Input
place_input = input("Enter place(s), separated by commas: ").strip()
cities = [city.strip() for city in place_input.split(",") if city.strip()]

category_input = input("Enter category (restaurants, cafes, schools, etc.): ").strip()
max_leads_input = input("Enter number of leads per city: ").strip()
max_leads_input = int(max_leads_input) if max_leads_input.isdigit() else 20

# Setup Driver
def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")
    options.page_load_strategy = "eager"
    return webdriver.Chrome(options=options)

driver = setup_driver()
driver.maximize_window()
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

# Helper Functions
def clean_google_url(url):
    try:
        parsed = urlparse(url)
        q = parse_qs(parsed.query).get("q")
        return q[0] if q else url
    except:
        return url

def clean_text(text):
    if text:
        text = re.sub(r"[^\x00-\x7F]+", "", text)
        return text.strip()
    return "N/A"

# Scraping Functions
def get_result_cards(place, category, max_scrolls=20):
    query = f"{category} in {place}".replace(" ", "+")
    driver.get(f"https://www.google.com/maps/search/{query}?hl=en")
    time.sleep(3)

    try:
        scroll_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[contains(@aria-label,"Results for") or @role="feed"]')))
    except:
        print(f"⚠️ Results container not found for {place}.")
        return []

    for _ in range(max_scrolls):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(1.5)

    cards = driver.find_elements(By.XPATH, '//div[contains(@class,"Nv2PK")]')
    print(f"✅ Found {len(cards)} cards in {place}")
    return cards

def get_place_details(card, place):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", card)
        try:
            action.move_to_element(card).click().perform()
        except:
            card.click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.XPATH, '//h1')))
        soup = BeautifulSoup(driver.page_source, "html.parser")

        name = soup.select_one("h1.DUwDvf")
        address = soup.select_one('button[data-item-id="address"]')
        phone = soup.select_one('button[data-item-id^="phone"]')
        website = soup.select_one('a[data-item-id="authority"]')

        rating, reviews = "N/A", "N/A"
        rating_reviews_div = soup.find("div", class_="F7nice")
        if rating_reviews_div:
            r_span = rating_reviews_div.find("span", {"aria-hidden": "true"})
            rating = r_span.text.strip() if r_span else "N/A"
            rev_span = rating_reviews_div.find("span", {"aria-label": re.compile(r"reviews")})
            if rev_span:
                reviews = rev_span.get("aria-label").split()[0]

        data = {
            "Place": clean_text(place),
            "Name": clean_text(name.text if name else None),
            "Rating": rating,
            "Reviews": reviews,
            "Address": clean_text(address.text if address else None),
            "Phone": clean_text(phone.text if phone else None),
            "Website": clean_google_url(website["href"]) if website else "N/A"
        }

        print(f"✅ {data['Name']} | ⭐ {data['Rating']} ({data['Reviews']} reviews) | 📍 {data['Address']} | ☎ {data['Phone']}")
        return data

    except Exception as e:
        print(f"⚠️ Detail fetch failed for {place}: {e}")
        return None

def scrape_places(place_list, category, max_leads=20):
    results = []
    for place in place_list:
        print(f"\n🌆 Scraping '{category}' in {place}...\n")
        cards = get_result_cards(place, category)
        for i, card in enumerate(cards[:max_leads], 1):
            print(f"➡️ {i}/{min(len(cards), max_leads)}: Extracting full details...")
            data = get_place_details(card, place)
            if data:
                results.append(data)
    return results

# ---------------------- Run Scraper ----------------------
all_leads = scrape_places(cities, category_input, max_leads=max_leads_input)

df = pd.DataFrame(all_leads)
filename = f"{category_input}_{'_'.join([c.replace(' ', '_') for c in cities])}_leads.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")
print(f"\n✅ Done! Collected {len(all_leads)} leads from {len(cities)} cities. CSV saved as '{filename}'.")

driver.quit()
