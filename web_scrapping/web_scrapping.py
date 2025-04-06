from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.shl.com"
URL_TEMPLATE = BASE_URL + "/solutions/products/product-catalog/?start={start}&type={type}"

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(), options=options)

def parse_table_based_solutions(html, test_type_label):
    soup = BeautifulSoup(html, "html.parser")
    table_rows = soup.find_all("tr", attrs={"data-course-id": True})
    results = []

    for row in table_rows:
        try:
            columns = row.find_all("td")
            name_tag = columns[0].find("a")
            name = name_tag.text.strip()
            url = name_tag["href"]
            full_url = BASE_URL + url if url.startswith("/") else url

            remote = "Yes" if columns[1].find("span", class_="-yes") else "No"
            adaptive = "Yes" if columns[2].find("span", class_="-yes") else "No"

            types = columns[3].find_all("span", class_="product-catalogue__key")
            test_types = ", ".join(t.text.strip() for t in types)

            results.append({
                "Assessment Name": name,
                "URL": full_url,
                "Category": test_type_label,
                "Remote Testing": remote,
                "Adaptive/IRT": adaptive,
                "Test Type": test_types
            })
        except Exception as e:
            print("❌ Error parsing row:", e)
    return results

def scrape_all_table_tests(driver, type_value, label):
    start = 0
    all_results = []

    while True:
        url = URL_TEMPLATE.format(start=start, type=type_value)
        print(f"🔄 Scraping {label} page at start={start} & type={type_value}")
        driver.get(url)
        time.sleep(30)
        html = driver.page_source

        results = parse_table_based_solutions(html, label)
        if not results:
            print("✅ No more results. Done.")
            break

        all_results.extend(results)
        start += 12
    return all_results

def save_results(data, filename="./data/shl_combined_results.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n✅ Saved {len(df)} total records to {filename}")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        # Scrape both test categories
        prepackaged_results = scrape_all_table_tests(driver, type_value=2, label="Pre-packaged Job Solutions")
        individual_results = scrape_all_table_tests(driver, type_value=1, label="Individual Test Solutions")

        # Combine and save
        all_data = prepackaged_results + individual_results
        save_results(all_data)
    finally:
        driver.quit()
