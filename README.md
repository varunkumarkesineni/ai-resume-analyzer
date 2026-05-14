# AI Resume Analyzer & Job Match System

> NLP-powered resume screening | Python · TF-IDF · scikit-learn · SQLite · Claude AI · Tkinter GUI
> Built by: Varun Kumar Kesineni | B.Tech CSE | CMR College of Engineering & Technology, Hyderabad

## Overview

Automates resume screening using TF-IDF vectorization and cosine similarity to match resumes
against job descriptions, rank candidates by fit score, and generate AI-rewritten resumes.

## Tech Stack

| Layer | Tool |
|---|---|
| NLP / Text Processing | Python, NLTK, TF-IDF (scikit-learn) |
| Similarity Scoring | Cosine Similarity (scikit-learn) |
| Data Processing | Pandas, NumPy |
| Database | SQLite (MySQL-compatible schema) |
| GUI | Tkinter |
| AI Rewriter | Anthropic Claude API |
| Visualization | Matplotlib, Seaborn |

## Project Structure

```
ai_resume_analyzer/
├── gui_app.py                  ← Main GUI application
├── notebooks/
│   ├── run_all.py              ← Run full pipeline
│   ├── 01_data_preparation.py
│   ├── 02_text_extraction.py
│   ├── 03_tfidf_matching.py
│   ├── 04_scoring_ranking.py
│   └── 05_sql_database.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_analysis_queries.sql
├── data/raw/                   ← Input CSVs
├── data/processed/             ← Cleaned data
├── outputs/                    ← Results + charts
├── requirements.txt
└── SETUP_GUIDE.md
```

## How to Run

```bash
pip install -r requirements.txt
python notebooks/run_all.py
python gui_app.py
```

## Key Results

- ~85% keyword-match accuracy using TF-IDF vectorization
- 200+ resume entries processed
- Top 10% candidates shortlisted 3x faster than manual review
- AI rewriting powered by Claude (Anthropic API)

## Author

**Varun Kumar Kesineni**
- Email: kesinenivarunkumar715@gmail.com
- LinkedIn: https://www.linkedin.com/in/varun-kumar-kesineni-80a427326/
- GitHub: https://github.com/varunkumarkesineni
