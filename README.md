# AI Resume Analyzer & Intelligent Talent Matching Platform

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()

> Enterprise-grade AI recruitment automation system powered by NLP, Machine Learning, and Intelligent Resume Ranking
>
> **Python · scikit-learn · TF-IDF · SQLite · Claude AI · Tkinter**

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Business Impact](#business-impact)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The AI Resume Analyzer & Intelligent Talent Matching Platform is a product-focused recruitment automation solution designed to streamline candidate screening and hiring workflows.

The platform leverages Natural Language Processing (NLP) and Machine Learning algorithms to analyze resumes, compare candidate profiles against job descriptions, and generate intelligent match scores for recruiters and HR teams.

Built with a scalable data-processing architecture and AI-assisted resume enhancement capabilities, the system significantly reduces manual screening effort while improving hiring efficiency and candidate selection accuracy.

## Key Features

- AI-powered resume screening and parsing
- Intelligent resume-to-job matching using TF-IDF vectorization
- Candidate ranking system with fit-score analysis
- AI-generated resume rewriting using Claude AI
- Interactive Tkinter-based recruiter dashboard
- Automated hiring analytics and visualization
- Structured candidate data management using SQLite

## Architecture

The pipeline processes candidates end-to-end across five sequential stages, with a desktop dashboard layered on top for recruiter interaction:

```
Raw Resumes & Job Descriptions
        │
        ▼
01_data_preparation.py    →  Clean and normalize input data
        │
        ▼
02_text_extraction.py     →  Extract structured text from resumes
        │
        ▼
03_tfidf_matching.py       →  Vectorize text & compute TF-IDF similarity
        │
        ▼
04_scoring_ranking.py       →  Generate fit scores & rank candidates
        │
        ▼
05_sql_database.py           →  Persist results to SQLite
        │
        ▼
gui_app.py (Tkinter)           →  Recruiter dashboard: review, rank,
                                    and trigger Claude AI resume rewrites
```

## Tech Stack

| Layer                   | Technology                   |
|--------------------------|--------------------------------|
| Programming Language    | Python                        |
| NLP & Machine Learning  | NLTK, TF-IDF, scikit-learn    |
| Similarity Scoring       | Cosine Similarity             |
| Data Processing          | Pandas, NumPy                 |
| Database                 | SQLite                        |
| AI Integration             | Anthropic Claude API          |
| Visualization               | Matplotlib, Seaborn           |
| GUI Framework               | Tkinter                       |

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

- Python 3.9 or later
- pip
- An [Anthropic API key](https://console.anthropic.com/) (required for the Claude-powered resume rewriting feature)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/varunkumarkesineni/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### Usage

```bash
# Run the full data pipeline (parsing → TF-IDF matching → scoring → database)
python notebooks/run_all.py

# Launch the recruiter dashboard
python gui_app.py
```

See `SETUP_GUIDE.md` for detailed configuration instructions.

## Business Impact

| Metric                              | Result                |
|---------------------------------------|--------------------------|
| Resume–job matching accuracy        | ~85%                    |
| Resumes processed                    | 200+                     |
| Candidate shortlisting time          | Reduced by ~3x           |
| Recruitment workflow                  | Automated & streamlined |

## Roadmap

- [ ] Cloud deployment using Flask or Django
- [ ] ATS integration support
- [ ] REST API services
- [ ] Multi-user recruiter dashboard
- [ ] Deep Learning-based semantic matching
- [ ] OCR-enabled PDF resume parsing

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

**Varun Kumar Kesineni**

- Email: [kesinenivarunkumar715@gmail.com](mailto:kesinenivarunkumar715@gmail.com)
- LinkedIn: [varun-kumar-kesineni](https://www.linkedin.com/in/varun-kumar-kesineni-80a427326/)
- GitHub: [@varunkumarkesineni](https://github.com/varunkumarkesineni)
