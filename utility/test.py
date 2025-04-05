import pandas as pd
import json

# Step 1: Load your Excel file
excel_path = "web_scrapping/shl_all_assessments.csv"  # Replace with your filename
df = pd.read_csv(excel_path)

# Step 2: Handle missing values
df.fillna('', inplace=True)

# Step 3: Convert the entire DataFrame to list of dicts (all columns included)
records = df.to_dict(orient='records')

# Step 4: Save to JSON
with open("data/shl_data.json", "w", encoding='utf-8') as f:
    json.dump(records, f, indent=4, ensure_ascii=False)
