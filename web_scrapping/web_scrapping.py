from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.shl.com"
START_URL = BASE_URL + "/solutions/products/product-catalog/?start={}&type=2"

# ✅ Setup headless browser
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(), options=options)

# ✅ Parse card-based assessments
def parse_card_based_assessments(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="product-card")
    results = []

    for card in cards:
        try:
            name = card.find("h3").text.strip()
            url = card.find("a", href=True)["href"]
            full_url = BASE_URL + url if url.startswith("/") else url
            desc = card.find("div", class_="product-card__desc").text.strip()

            info_tags = card.find_all("span", class_="product-card__feature-label")
            duration, remote, adaptive, test_type = [""] * 4

            for tag in info_tags:
                text = tag.text.strip().lower()
                if "minute" in text:
                    duration = text
                elif "remote" in text:
                    remote = "Yes" if "yes" in text else "No"
                elif "adaptive" in text or "irt" in text:
                    adaptive = "Yes" if "yes" in text else "No"
                elif len(text) == 1 and text.isalpha():
                    test_type = text.upper()

            results.append({
                "Assessment Name": name,
                "URL": full_url,
                "Description": desc,
                "Duration": duration,
                "Remote Testing": remote,
                "Adaptive/IRT": adaptive,
                "Test Type": test_type,
            })
        except Exception as e:
            print("Error parsing card:", e)
    return results

# ✅ Parse table-based job solutions
def parse_table_based_solutions(html):
    soup = BeautifulSoup(html, "html.parser")
    table_rows = soup.find_all("tr", attrs={"data-course-id": True})
    results = []

    for row in table_rows:
        try:
            columns = row.find_all("td")
            name_tag = columns[0].find("a")
            name = name_tag.text.strip()
            url = name_tag["href"]
            full_url = BASE_URL + url

            remote = "Yes" if columns[1].find("span", class_="-yes") else "No"
            adaptive = "Yes" if columns[2].find("span", class_="-yes") else "No"

            types = columns[3].find_all("span", class_="product-catalogue__key")
            test_types = ", ".join(t.text.strip() for t in types)

            results.append({
                "Assessment Name": name,
                "URL": full_url,
                "Description": "Pre-packaged Job Solution",
                "Duration": "",
                "Remote Testing": remote,
                "Adaptive/IRT": adaptive,
                "Test Type": test_types,
            })
        except Exception as e:
            print("Error parsing table row:", e)
    return results

# ✅ Loop through all pages
def scrape_all_pages(driver, start_range=0, end_range=132, step=12):
    all_results = []
    for start in range(start_range, end_range + 1, step):
        url = START_URL.format(start)
        print(f"Scraping page: {url}")
        driver.get(url)
        time.sleep(5)  # Allow JavaScript to load
        html = driver.page_source

        # Scrape both formats
        results_cards = parse_card_based_assessments(html)
        results_table = parse_table_based_solutions(html)

        all_results.extend(results_cards)
        all_results.extend(results_table)
    return all_results

# ✅ Save results to CSV
def save_results(data, filename="data/shl_inital.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n✅ Saved {len(df)} records to {filename}")

# ✅ Main runner
if __name__ == "__main__":
    driver = setup_driver()
    try:
        all_data = scrape_all_pages(driver, start_range=0, end_range=132, step=12)
        save_results(all_data)
    finally:
        driver.quit()
