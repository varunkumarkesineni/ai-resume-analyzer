import pandas as pd
import nltk
import re
import os

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

RAW_DIR  = "data/raw"
PROC_DIR = "data/processed"
os.makedirs(PROC_DIR, exist_ok=True)

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

TECH_KEYWORDS = [
    "python", "pandas", "numpy", "sql", "mysql", "postgresql", "sqlite",
    "machine learning", "scikit", "tensorflow", "pytorch", "keras", "nlp",
    "tfidf", "tf-idf", "cosine", "nltk", "bert", "word2vec",
    "power bi", "tableau", "matplotlib", "seaborn", "plotly",
    "aws", "gcp", "azure", "s3", "bigquery", "docker",
    "git", "github", "rest", "api", "json", "django", "flask", "react",
    "javascript", "java", "html", "css", "excel", "etl", "oop",
    "algorithm", "data structure", "deep learning", "regression",
    "classification", "clustering", "random forest", "neural",
    "dashboard", "kpi", "visualization", "analytics", "reporting",
]

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [LEMMATIZER.lemmatize(t) for t in text.split() if t not in STOP_WORDS or len(t) <= 3]
    return " ".join(tokens)

def extract_keywords(text):
    found = []
    text_lower = str(text).lower()
    for kw in TECH_KEYWORDS:
        if kw in text_lower and kw not in found:
            found.append(kw)
    return ", ".join(found[:15])

df_res = pd.read_csv(f"{RAW_DIR}/resumes.csv")
df_res["clean_text"] = df_res["resume_text"].apply(clean_text)
df_res["keywords"]   = df_res["resume_text"].apply(extract_keywords)
df_res.to_csv(f"{PROC_DIR}/resumes_clean.csv", index=False)

df_jobs = pd.read_csv(f"{RAW_DIR}/job_descriptions.csv")
df_jobs["clean_text"] = df_jobs["job_description"].apply(clean_text)
df_jobs["keywords"]   = df_jobs["job_description"].apply(extract_keywords)
df_jobs.to_csv(f"{PROC_DIR}/jobs_clean.csv", index=False)

print(f"Processed {len(df_res)} resumes and {len(df_jobs)} jobs.")
