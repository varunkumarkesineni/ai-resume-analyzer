# Setup Guide — AI Resume Analyzer & Intelligent Talent Matching Platform

## Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

Install all required Python libraries including NLP, Machine Learning, database, and GUI dependencies.

---

## Step 2 — Execute the Processing Pipeline

```bash
python notebooks/run_all.py
```

This command performs the complete backend workflow:

- Data preprocessing
- Resume text extraction
- TF-IDF vectorization
- Resume-job similarity matching
- Candidate scoring and ranking
- Database generation
- Analytics preparation

---

## Step 3 — Launch the Recruitment Dashboard

```bash
python gui_app.py
```

Starts the Tkinter-based desktop application for resume analysis and recruiter interaction.

---

## Step 4 — Application Workflow

### Resume Analyzer Module
1. Upload resumes in PDF, DOCX, or TXT format
2. Click **Analyze Resume**
3. View AI-generated match scores for multiple job roles
4. Compare candidate rankings based on similarity percentage

### AI Resume Optimization Module
1. Paste your Anthropic Claude API key
2. Select the target job role
3. Generate an AI-enhanced professional resume

### SQL Analytics Module
1. Execute predefined SQL queries
2. Analyze candidate datasets and ranking metrics

### Candidate Rankings Dashboard
1. View all processed candidates
2. Sort applicants based on fit scores and relevance

---

## Step 5 — Generate Anthropic Claude API Key

### Create API Access

1. Visit:
   https://console.anthropic.com

2. Sign up or log in to your Anthropic account

3. Navigate to:
   API Keys → Create Key

4. Copy the generated API key
   Example:
   ```bash
   sk-ant-xxxxxxxxxxxxxxxx
   ```

5. Paste the key into:
   GUI → AI Rewrite Module → API Key Field

---

## Troubleshooting Guide

| Issue | Solution |
|---|---|
| ModuleNotFoundError | pip install -r requirements.txt |
| Missing NLTK package | pip install nltk |
| PDF extraction issue | pip install PyPDF2 |
| DOCX extraction issue | pip install python-docx |
| Claude API connection error | Verify Anthropic API key |
| GUI not opening | Check Tkinter installation |
| SQLite database error | Re-run run_all.py pipeline |

---

## Recommended Python Version

```bash
Python 3.10+
```

---

## Recommended Environment Setup

```bash
python -m venv venv
```

Activate virtual environment:

### Windows
```bash
venv\Scripts\activate
```

### macOS/Linux
```bash
source venv/bin/activate
```

---

## Final Execution Commands

```bash
pip install -r requirements.txt
python notebooks/run_all.py
python gui_app.py
```
