import streamlit as st
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data
with open("data/shl_data_with_embeddings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract embeddings and info
embeddings = np.array([item["embedding"] for item in data])
test_names = [item["Assessment Name"] for item in data]
descriptions = [item["Description"] for item in data]
urls = [item["URL"] for item in data]
durations = [item["Duration"] for item in data]
job_levels = [item["Job Level"] for item in data]
remote = [item["Remote Testing"] for item in data]
adaptive = [item["Adaptive/IRT"] for item in data]
test_types = [item["Test Type"] for item in data]

st.title("🧠 SHL Assessment Recommender")

st.write("Enter a job role or description OR upload a .txt file with the job description.")

# Text input
text_input = st.text_area("✏️ Enter Job Prompt:", placeholder="e.g., Mid-level software developer with leadership qualities")

# File upload
uploaded_file = st.file_uploader("📄 Or upload a .txt file", type=["txt"])
file_text = ""
if uploaded_file is not None:
    file_text = uploaded_file.read().decode("utf-8")

# Use text_input if available, else file_text
final_prompt = text_input.strip() if text_input.strip() else file_text.strip()

if st.button("🔍 Find Best Tests"):
    if not final_prompt:
        st.warning("Please enter a prompt or upload a .txt file.")
    else:
        # Embed the prompt
        prompt_embedding = model.encode(final_prompt, convert_to_tensor=True).float()
        embeddings = embeddings.astype(np.float32)
        # Calculate cosine similarity
        similarity_scores = util.cos_sim(prompt_embedding, embeddings)[0].cpu().numpy()
        top_indices = np.argsort(similarity_scores)[::-1][:10]

        # Display results
        st.subheader("📋 Recommended Tests")
        for idx in top_indices:
            st.markdown(f"### [{test_names[idx]}]({urls[idx]})")
            st.markdown(f"**Similarity Score:** {similarity_scores[idx]:.3f}")
            st.markdown(f"**Duration:** {durations[idx]} mins | **Remote:** {remote[idx]} | **Adaptive:** {adaptive[idx]}")
            st.markdown(f"**Job Level:** {job_levels[idx]} | **Test Types:** {test_types[idx]}")
            st.markdown(f"**Description:** {descriptions[idx]}")
            st.markdown("---")
