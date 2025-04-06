# 🔍 SHL Test Recommendation System

This project is built to streamline the manual process of identifying the most suitable SHL assessment tests for a given job role. It uses **web scraping**, **text preprocessing**, **embeddings**, and a **Streamlit-powered dashboard** to suggest and rank relevant SHL tests based on a user's job description prompt or a `.txt` file upload.

---

## 🚀 Project Overview

### 🎯 Goal
Build a dashboard where HR professionals can input a job prompt (or upload a job description file) and get a **ranked list of SHL assessments** best suited for that role, using semantic similarity between the job prompt and SHL test descriptions.

### 👩‍💻 Users
- HR Teams
- Talent Acquisition Specialists
- Recruitment Consultants

---

## 📦 Project Structure

```
SHL-Test-Recommendation/
│
├── data/
│   ├── raw_tests.csv               # Initial scraped data
│   ├── detailed_tests.json         # Cleaned and structured data with full descriptions
│   ├── embeddings.npy              # Precomputed vector embeddings for descriptions
│
├── app/
│   └── streamlit_app.py            # Streamlit front-end application
│
├── notebooks/
│   ├── scrape_tests.ipynb          # Scraping code for SHL catalog
│   ├── preprocess_descriptions.ipynb  # Text preprocessing and cleaning
│   └── compute_embeddings.ipynb    # Embed descriptions using Sentence Transformers
│
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Component              | Tool/Library                     |
|------------------------|----------------------------------|
| Language               | Python 3.10+                     |
| Web Scraping           | `requests`, `BeautifulSoup`      |
| NLP & Embeddings       | `nltk`, `sentence-transformers`  |
| Dashboard UI           | `Streamlit`                      |
| Data Storage           | `pandas`, `json`, `numpy`        |

---

## 📥 Step-by-Step Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sonalrajsr/SHL-Assessment-Recommendation-System-.git
cd shl-test-recommendation
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On macOS/Linux
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

## 🔄 Data Pipeline

### 📌 Step 1: Web Scraping

Use `scrape_tests.ipynb` to extract:
- Assessment name
- Detail page URL
- Description
- Test duration, test type, remote testing info

> Pagination handled automatically to cover all pages of SHL’s [Product Catalog](https://www.shl.com/solutions/products/product-catalog/)

### 🧼 Step 2: Text Cleaning

Run `preprocess_descriptions.ipynb` to:
- Remove stopwords
- Lemmatize words
- Normalize text (lowercase, strip special characters)

Output:
- `cleaned_full_text` (used for embeddings)

### 🧠 Step 3: Embedding Descriptions

Run `compute_embeddings.ipynb` to:
- Generate vector embeddings for each cleaned description using models like `all-MiniLM-L6-v2` from `sentence-transformers`
- Save embeddings in `.npy` format

---

## 💡 How It Works

1. **User Input**:
   - Text prompt typed in manually _or_
   - `.txt` file upload

2. **Preprocessing**:
   - Clean and embed the input using the same NLP pipeline

3. **Semantic Search**:
   - Cosine similarity between input embedding and test embeddings

4. **Ranking**:
   - Return top 5–10 most similar SHL tests

---

## 🖥️ Streamlit Dashboard

### 🔧 To Run the App

```bash
streamlit run app/streamlit_app.py --server.runOnSave=false
```

### 🧾 Features
- Upload `.txt` file or enter job role prompt
- See a table with:
  - Assessment Name
  - Description
  - Duration
  - Test Type
  - Job Level
  - Match Score

---

## 🧪 Example Use Case

**Prompt**:
```
Looking for a mid-level sales executive who manages client relationships and drives revenue.
```

**Output**:
| Rank | Test Name                  | Match Score |
|------|----------------------------|-------------|
| 1    | Account Manager Solution   | 0.91        |
| 2    | Sales Professional Solution| 0.87        |
| ...  | ...                        | ...         |

---

## 📄 Future Enhancements
- Use OpenAI/GPT for more context-aware ranking
- Incorporate filters (Job Level, Duration range)
- Admin dashboard for updating the test catalog
- Add visualizations (e.g., similarity heatmap)

---

## 🤝 Acknowledgements

- [SHL Product Catalog](https://www.shl.com/solutions/products/product-catalog/)
- HuggingFace's [`sentence-transformers`](https://www.sbert.net/)
- Streamlit for rapid dashboard development

---

## 📬 Contact

Feel free to reach out if you have any questions or want to collaborate!

**Author**: [Sonal Raj]  
**Email**: sonalraj0852@gmail.com  
**LinkedIn**: [Your Profile](https://linkedin.com/in/sonalrajsr)

---