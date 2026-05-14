import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
import os

PROC_DIR   = "data/processed"
OUTPUT_DIR = "outputs"
CHART_DIR  = f"{OUTPUT_DIR}/charts"
os.makedirs(CHART_DIR, exist_ok=True)

df_res  = pd.read_csv(f"{PROC_DIR}/resumes_clean.csv")
df_jobs = pd.read_csv(f"{PROC_DIR}/jobs_clean.csv")

vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
all_texts  = list(df_res["clean_text"].fillna("")) + list(df_jobs["clean_text"].fillna(""))
vectorizer.fit(all_texts)

resume_vecs = vectorizer.transform(df_res["clean_text"].fillna(""))
job_vecs    = vectorizer.transform(df_jobs["clean_text"].fillna(""))
sim_matrix  = cosine_similarity(resume_vecs, job_vecs)

rows = []
for r_idx, row in df_res.iterrows():
    for j_idx, job in df_jobs.iterrows():
        rows.append({
            "resume_id":        row["resume_id"],
            "candidate_name":   row["candidate_name"],
            "experience_years": row["experience_years"],
            "education":        row["education"],
            "job_id":           job["job_id"],
            "job_title":        job["job_title"],
            "company":          job["company"],
            "exp_required":     job["experience_required"],
            "match_score":      round(sim_matrix[r_idx, j_idx] * 100, 2),
        })

df_matches = pd.DataFrame(rows)
df_matches["rank"] = df_matches.groupby("job_id")["match_score"].rank(ascending=False, method="min").astype(int)

def match_level(score):
    if score >= 60: return "Excellent Match"
    if score >= 40: return "Good Match"
    if score >= 20: return "Partial Match"
    return "Low Match"

df_matches["match_level"] = df_matches["match_score"].apply(match_level)
df_matches.to_csv(f"{OUTPUT_DIR}/match_scores.csv", index=False)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("TF-IDF Resume Matching Results", fontsize=14, fontweight="bold")

top10_idx = list(range(min(10, len(df_res))))
heat_data = sim_matrix[top10_idx, :] * 100
heat_df   = pd.DataFrame(heat_data, index=df_res.iloc[top10_idx]["candidate_name"], columns=df_jobs["job_title"])
sns.heatmap(heat_df, annot=True, fmt=".0f", cmap="YlOrRd", ax=axes[0,0], cbar_kws={"label": "Match %"})
axes[0,0].set_title("Match Score Heatmap")
axes[0,0].tick_params(axis="x", rotation=30)

colors = {"Excellent Match": "#1d9e75", "Good Match": "#3266ad", "Partial Match": "#ef9f27", "Low Match": "#d85a30"}
level_counts = df_matches["match_level"].value_counts()
axes[0,1].bar(level_counts.index, level_counts.values, color=[colors.get(l, "gray") for l in level_counts.index], alpha=0.85)
axes[0,1].set_title("Match Level Distribution")
axes[0,1].tick_params(axis="x", rotation=15)

job_scores = [df_matches[df_matches["job_title"] == t]["match_score"].values for t in df_jobs["job_title"]]
axes[1,0].boxplot(job_scores, labels=df_jobs["job_title"], patch_artist=True)
axes[1,0].set_title("Score Distribution by Role")
axes[1,0].tick_params(axis="x", rotation=20)

for level, color in colors.items():
    subset = df_matches[df_matches["match_level"] == level]
    axes[1,1].scatter(subset["experience_years"], subset["match_score"], c=color, label=level, alpha=0.4, s=15)
axes[1,1].set_title("Experience vs Match Score")
axes[1,1].set_xlabel("Years of Experience")
axes[1,1].set_ylabel("Match Score %")
axes[1,1].legend(fontsize=8)

plt.tight_layout()
plt.savefig(f"{CHART_DIR}/tfidf_matching.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"Matching complete. {len(df_matches):,} pairs scored.")
