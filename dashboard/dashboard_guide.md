# Power BI Dashboard Guide

## Load Data
Open Power BI Desktop → Get Data → Text/CSV → load:
- outputs/final_rankings.csv
- outputs/skill_gap_report.csv

## Page 1 — Hiring Overview
- KPI Cards: Total Applicants, Shortlisted, Avg Match Score, Top Score
- Bar Chart: Applicants per Job Role
- Funnel: Excellent → Good → Partial → Low Match
- Slicer: Job Title, Match Level

## Page 2 — Candidate Rankings
- Table: candidate_name, job_title, experience_years, match_score, final_score, final_rank
- Conditional formatting on final_score (green high, red low)
- Slicer: Job Title, is_shortlisted

## Page 3 — Skill Gap
- Matrix: skill (rows) vs job_title (columns)
- Bar: Top missing skills

## DAX Measures
Avg Match Score = AVERAGE(final_rankings[match_score])
Shortlist Rate = DIVIDE(COUNTROWS(FILTER(final_rankings, final_rankings[is_shortlisted]=1)), COUNTROWS(final_rankings))
