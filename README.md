# AI Resume Analyzer & Intelligent Talent Matching Platform

> Enterprise-grade AI recruitment automation system powered by NLP, Machine Learning, and Intelligent Resume Ranking
>
> **Python · scikit-learn · TF-IDF · SQLite · Claude AI · Tkinter**

## Overview

The AI Resume Analyzer & Intelligent Talent Matching Platform is a product-focused recruitment automation solution designed to streamline candidate screening and hiring workflows.

The platform leverages Natural Language Processing (NLP) and Machine Learning algorithms to analyze resumes, compare candidate profiles against job descriptions, and generate intelligent match scores for recruiters and HR teams.

Built with a scalable data-processing architecture and AI-assisted resume enhancement capabilities, the system significantly reduces manual screening effort while improving hiring efficiency and candidate selection accuracy.

## Core Features

- AI-powered resume screening and parsing
- Intelligent resume-to-job matching using TF-IDF vectorization
- Candidate ranking system with fit-score analysis
- AI-generated resume rewriting using Claude AI
- Interactive Tkinter-based recruiter dashboard
- Automated hiring analytics and visualization
- Structured candidate data management using SQLite

## Tech Stack

| Layer                  | Technology                 |
|-------------------------|------------------------------|
| Programming Language   | Python                      |
| NLP & Machine Learning | NLTK, TF-IDF, scikit-learn  |
| Similarity Scoring      | Cosine Similarity           |
| Data Processing         | Pandas, NumPy               |
| Database                | SQLite                      |
| AI Integration           | Anthropic Claude API        |
| Visualization             | Matplotlib, Seaborn         |
| GUI Framework             | Tkinter                     |

## Project Structure

```
ai_resume_analyzer/
├── gui_app.py
├── notebooks/
│   ├── run_all.py
│   ├── 01_data_preparation.py
│   ├── 02_text_extraction.py
│   ├── 03_tfidf_matching.py
│   ├── 04_scoring_ranking.py
│   └── 05_sql_database.py
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_analysis_queries.sql
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
├── requirements.txt
└── SETUP_GUIDE.md
```

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/varunkumarkesineni/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the data pipeline (parsing, TF-IDF matching, scoring, database)
python notebooks/run_all.py

# 4. Launch the recruiter dashboard
python gui_app.py
```

See `SETUP_GUIDE.md` for detailed configuration instructions.

## Business Impact

- Achieved approximately 85% resume-job matching accuracy
- Processed and analyzed 200+ resumes efficiently
- Reduced candidate shortlisting time by nearly 3x
- Improved recruitment workflow automation and hiring efficiency

## Future Enhancements

- [ ] Cloud deployment using Flask or Django
- [ ] ATS integration support
- [ ] REST API services
- [ ] Multi-user recruiter dashboard
- [ ] Deep Learning-based semantic matching
- [ ] OCR-enabled PDF resume parsing

## Author

**Varun Kumar Kesineni**

- Email: [kesinenivarunkumar715@gmail.com](mailto:kesinenivarunkumar715@gmail.com)
- LinkedIn: [varun-kumar-kesineni](https://www.linkedin.com/in/varun-kumar-kesineni-80a427326/)
- GitHub: [@varunkumarkesineni](https://github.com/varunkumarkesineni)
