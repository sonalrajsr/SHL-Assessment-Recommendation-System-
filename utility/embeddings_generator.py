from sentence_transformers import SentenceTransformer
import json

# Load JSON
with open("../data/shl_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Add embeddings
for item in data:
    text = item.get("cleaned_full_text", "")
    embedding = model.encode(text).tolist()
    item["embedding"] = embedding

# Save to new file
with open("../data/shl_data_with_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
