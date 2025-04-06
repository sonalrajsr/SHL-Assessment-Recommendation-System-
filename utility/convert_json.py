import pandas as pd
import json

# Load your Excel file
excel_path = "./data/shl_cleaned_data.csv"
df = pd.read_csv(excel_path)

# Handle missing values
df.fillna('', inplace=True)

# Convert the entire DataFrame to list of dicts
records = df.to_dict(orient='records')

# Save to JSON
with open("data/shl_data.json", "w", encoding='utf-8') as f:
    json.dump(records, f, indent=4, ensure_ascii=False)
