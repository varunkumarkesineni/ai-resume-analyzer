import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "outputs"
CHART_DIR  = f"{OUTPUT_DIR}/charts"
PROC_DIR   = "data/processed"
os.makedirs(CHART_DIR, exist_ok=True)

DB_PATH = f"{OUTPUT_DIR}/resume_analyzer.db"
conn    = sqlite3.connect(DB_PATH)

conn.executescript("""
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS job_roles;
DROP TABLE IF EXISTS match_results;
DROP TABLE IF EXISTS skill_gap;

CREATE TABLE candidates (
    resume_id TEXT PRIMARY KEY, candidate_name TEXT, email TEXT,
    experience_years INTEGER, education TEXT, keywords TEXT
);
CREATE TABLE job_roles (
    job_id TEXT PRIMARY KEY, job_title TEXT, company TEXT,
    location TEXT, experience_required INTEGER
);
CREATE TABLE match_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT, resume_id TEXT, job_id TEXT,
    match_score REAL, final_score REAL, final_rank INTEGER,
    match_level TEXT, is_shortlisted INTEGER
);
CREATE TABLE skill_gap (
    id INTEGER PRIMARY KEY AUTOINCREMENT, candidate_name TEXT,
    job_title TEXT, skill TEXT, has_skill INTEGER, gap INTEGER
);
CREATE INDEX idx_final_score ON match_results(final_score);
CREATE INDEX idx_job         ON match_results(job_id);
""")
conn.commit()

df_res   = pd.read_csv(f"{PROC_DIR}/resumes_clean.csv")
df_jobs  = pd.read_csv(f"{PROC_DIR}/jobs_clean.csv")
df_match = pd.read_csv(f"{OUTPUT_DIR}/final_rankings.csv")
df_gap   = pd.read_csv(f"{OUTPUT_DIR}/skill_gap_report.csv")

df_res[["resume_id", "candidate_name", "email", "experience_years", "education", "keywords"]]\
    .to_sql("candidates",    conn, if_exists="append", index=False)
df_jobs[["job_id", "job_title", "company", "location", "experience_required"]]\
    .to_sql("job_roles",     conn, if_exists="append", index=False)
df_match[["resume_id", "job_id", "match_score", "final_score", "final_rank", "match_level", "is_shortlisted"]]\
    .to_sql("match_results", conn, if_exists="append", index=False)
df_gap[["candidate_name", "job_title", "skill", "has_skill", "gap"]]\
    .to_sql("skill_gap",     conn, if_exists="append", index=False)
conn.commit()

queries = {
    "Top 5 candidates per job": """
        SELECT j.job_title, c.candidate_name, c.experience_years, m.match_score, m.final_score, m.final_rank
        FROM match_results m
        JOIN candidates c ON m.resume_id = c.resume_id
        JOIN job_roles  j ON m.job_id    = j.job_id
        WHERE m.final_rank <= 5
        ORDER BY j.job_title, m.final_rank
    """,
    "Match level distribution": """
        SELECT match_level, COUNT(*) AS count, ROUND(AVG(final_score),1) AS avg_score
        FROM match_results GROUP BY match_level ORDER BY avg_score DESC
    """,
    "Skill gap summary": """
        SELECT skill, SUM(has_skill) AS have, SUM(gap) AS missing,
               ROUND(SUM(gap)*100.0/COUNT(*),1) AS gap_pct
        FROM skill_gap GROUP BY skill ORDER BY gap_pct DESC
    """,
}

results = {}
for title, query in queries.items():
    results[title] = pd.read_sql_query(query, conn)

conn.close()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("AI Resume Analyzer — Dashboard Statistics", fontsize=14, fontweight="bold")

sl = results["Top 5 candidates per job"][results["Top 5 candidates per job"]["final_rank"] == 1]
axes[0,0].barh(sl["job_title"], sl["final_score"], color="#3266ad", alpha=0.85)
axes[0,0].set_title("Top Candidate Score per Role")
axes[0,0].set_xlabel("Final Score")

ml = results["Match level distribution"]
colors = {"Excellent Match": "#1d9e75", "Good Match": "#3266ad", "Partial Match": "#ef9f27", "Low Match": "#d85a30"}
axes[0,1].bar(ml["match_level"], ml["count"], color=[colors.get(l, "gray") for l in ml["match_level"]], alpha=0.85)
axes[0,1].set_title("Match Level Distribution")
axes[0,1].tick_params(axis="x", rotation=15)

sg = results["Skill gap summary"]
axes[1,0].barh(sg["skill"][::-1], sg["gap_pct"][::-1], color="#d85a30", alpha=0.85)
axes[1,0].set_title("Skill Gap % by Skill")
axes[1,0].set_xlabel("Gap %")

axes[1,1].barh(sg["skill"][::-1], sg["have"][::-1], color="#1d9e75", alpha=0.85)
axes[1,1].set_title("Skill Coverage Count")
axes[1,1].set_xlabel("Candidates with Skill")

plt.tight_layout()
plt.savefig(f"{CHART_DIR}/dashboard_stats.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"Database ready: {DB_PATH}")
