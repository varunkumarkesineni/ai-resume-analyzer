import subprocess
import sys
import os

steps = [
    ("01_data_preparation.py",  "Data Preparation     — Generating resume & job dataset"),
    ("02_text_extraction.py",   "Text Extraction       — NLP cleaning & keyword extraction"),
    ("03_tfidf_matching.py",    "TF-IDF Matching       — Cosine similarity scoring"),
    ("04_scoring_ranking.py",   "Scoring & Ranking     — Weighted final scores"),
    ("05_sql_database.py",      "SQL Database          — Loading results & queries"),
]

print("=" * 55)
print("  AI RESUME ANALYZER — Full Pipeline")
print("  Varun Kumar Kesineni | B.Tech CSE")
print("=" * 55)

for script, label in steps:
    print(f"\n>>> {label}")
    result = subprocess.run([sys.executable, os.path.join("notebooks", script)])
    if result.returncode != 0:
        print(f"Error in {script}. Fix and retry.")
        sys.exit(1)

print("\n" + "=" * 55)
print("  ALL STEPS COMPLETE!")
print("  outputs/           — CSV result files")
print("  outputs/charts/    — Visualizations")
print("  outputs/resume_analyzer.db — SQLite DB")
print("=" * 55)
print("\nNext: Run the GUI → python gui_app.py")
