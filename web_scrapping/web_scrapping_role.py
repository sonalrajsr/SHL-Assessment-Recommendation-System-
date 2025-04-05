import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# === Setup Headless Chrome ===
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(), options=options)

# === Extract info from individual page ===
def extract_details(driver, url):
    driver.get(url)
    time.sleep(3)  # Let page load
    soup = BeautifulSoup(driver.page_source, "html.parser")

    def get_text_by_heading(heading):
        block = soup.find("div", class_="product-catalogue-training-calendar__row", string=None)
        if block:
            h = block.find("h4")
            if h and heading.lower() in h.text.strip().lower():
                p = block.find("p")
                return p.text.strip() if p else ""
        return ""

    def get_all_blocks():
        return soup.find_all("div", class_="product-catalogue-training-calendar__row")

    # Extract by scanning all blocks
    description = job_level = length = test_type = remote = ""
    for block in get_all_blocks():
        h4 = block.find("h4")
        if not h4:
            continue
        title = h4.text.strip().lower()
        if "description" in title:
            description = block.find("p").text.strip()
        elif "job level" in title:
            job_level = block.find("p").text.strip()
        elif "assessment length" in title:
            length = block.find("p").text.strip()
            keys = block.find_all("span", class_="product-catalogue__key")
            test_type = ", ".join(k.text.strip() for k in keys)
            remote_span = block.find("span", class_="catalogue__circle -yes")
            remote = "Yes" if remote_span else "No"

    return {
        "Description": description,
        "Job Level": job_level,
        "Assessment Length": length,
        "Test Type": test_type,
        "Remote Testing": remote,
    }

# === Main Function ===
def enrich_csv_with_details(input_csv="web_scrapping\shl_all_assessments.csv", output_csv="shl_detailed_assessments.csv"):
    df = pd.read_csv(input_csv)
    driver = setup_driver()
    results = []

    for idx, row in df.iterrows():
        url = row["URL"]
        name = row["Assessment Name"]
        print(f"[{idx+1}/{len(df)}] Scraping: {name} - {url}")
        try:
            details = extract_details(driver, url)
            combined = {**row.to_dict(), **details}
            results.append(combined)
        except Exception as e:
            print("❌ Error:", e)
            continue

    driver.quit()
    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f"\n✅ Saved enriched dataset to: {output_csv}")

# === Run it ===
if __name__ == "__main__":
    enrich_csv_with_details()
