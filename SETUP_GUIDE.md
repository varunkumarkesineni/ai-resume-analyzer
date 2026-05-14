# Setup Guide — AI Resume Analyzer v2

## Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

## Step 2 — Run the pipeline
```bash
python notebooks/run_all.py
```

## Step 3 — Launch the GUI
```bash
python gui_app.py
```

## Step 4 — Use the GUI
1. Analyzer tab → Browse & upload your resume (PDF/DOCX/TXT)
2. Click "Analyze Resume" → See match scores for 5 job roles
3. AI Rewrite tab → Paste API key → Select target role → Generate
4. SQL Queries tab → Run preset queries against the database
5. Rankings tab → View all candidates ranked by score

## Step 5 — Get Claude API key (for AI Rewrite feature)
1. Go to: https://console.anthropic.com
2. Sign up (free) → API Keys → Create Key
3. Copy the key (starts with sk-ant-...)
4. Paste it in the GUI → AI Rewrite tab → API Key field

## Troubleshooting
| Error | Fix |
|---|---|
| ModuleNotFoundError | pip install -r requirements.txt |
| No module nltk | pip install nltk |
| PDF not reading | pip install PyPDF2 |
| DOCX not reading | pip install python-docx |
| API error | Check your Anthropic API key |
