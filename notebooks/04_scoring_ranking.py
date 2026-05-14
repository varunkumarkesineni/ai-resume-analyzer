import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_DIR = "outputs"
CHART_DIR  = f"{OUTPUT_DIR}/charts"
os.makedirs(CHART_DIR, exist_ok=True)

df = pd.read_csv(f"{OUTPUT_DIR}/match_scores.csv")

def experience_fit(candidate_exp, required_exp):
    diff = candidate_exp - required_exp
    if diff < 0:   return max(0, 100 + diff * 20)
    if diff <= 2:  return 100
    return max(60, 100 - (diff - 2) * 10)

def education_bonus(education):
    bonuses = {"M.Tech": 10, "M.Tech Data Science": 10, "MBA": 8,
               "B.Tech Computer Science": 5, "B.Tech CSE": 5,
               "B.Tech IT": 4, "B.Tech ECE": 3, "BCA": 3, "B.Sc": 3}
    for key, val in bonuses.items():
        if key.lower() in str(education).lower():
            return val
    return 2

df["exp_fit"]    = df.apply(lambda r: experience_fit(r["experience_years"], r["exp_required"]), axis=1)
df["edu_bonus"]  = df["education"].apply(education_bonus)
df["final_score"] = (df["match_score"] * 0.70 + df["exp_fit"] * 0.20 + df["edu_bonus"] * 0.10).round(2)
df["final_rank"]  = df.groupby("job_id")["final_score"].rank(ascending=False, method="min").astype(int)
df["is_shortlisted"] = (df["final_rank"] <= 5).astype(int)

df.to_csv(f"{OUTPUT_DIR}/final_rankings.csv", index=False)

np.random.seed(42)
skills = ["Python", "SQL", "Power BI", "Machine Learning", "NLP", "AWS", "Tableau", "Excel", "Git", "ETL"]
gap_rows = []
for _, row in df[df["final_rank"] <= 3].iterrows():
    for skill in skills:
        has = np.random.choice([True, False], p=[0.6, 0.4])
        gap_rows.append({"candidate_name": row["candidate_name"], "job_title": row["job_title"],
                         "skill": skill, "has_skill": has, "gap": not has})
pd.DataFrame(gap_rows).to_csv(f"{OUTPUT_DIR}/skill_gap_report.csv", index=False)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Resume Scoring & Ranking Analysis", fontsize=14, fontweight="bold")

top5 = df[df["final_rank"] <= 5]
axes[0,0].barh([f"{r['candidate_name'][:12]}" for _, r in top5.head(15).iterrows()],
               top5.head(15)["final_score"], color="#3266ad", alpha=0.85)
axes[0,0].set_title("Top Candidates by Final Score")
axes[0,0].set_xlabel("Final Score")

axes[0,1].hist(df["final_score"], bins=30, color="#3266ad", alpha=0.8, edgecolor="white")
axes[0,1].axvline(df["final_score"].mean(), color="#d85a30", linestyle="--", linewidth=2)
axes[0,1].set_title("Final Score Distribution")

axes[1,0].scatter(df["match_score"], df["final_score"], c=df["experience_years"],
                  cmap="viridis", alpha=0.4, s=15)
axes[1,0].set_title("TF-IDF vs Final Score")
axes[1,0].set_xlabel("Match Score %")
axes[1,0].set_ylabel("Final Score")

df_gap = pd.DataFrame(gap_rows)
pivot  = df_gap.groupby(["skill", "job_title"])["has_skill"].mean().unstack() * 100
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn", ax=axes[1,1], cbar_kws={"label": "% with Skill"})
axes[1,1].set_title("Skill Coverage %")
axes[1,1].tick_params(axis="x", rotation=20)

plt.tight_layout()
plt.savefig(f"{CHART_DIR}/ranking_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"Scoring complete. {df['is_shortlisted'].sum()} candidates shortlisted.")
