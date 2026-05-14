# Power BI Dashboard Guide — AI Resume Analyzer & Talent Matching Platform

## Step 1 — Load Dataset into Power BI

Open **Power BI Desktop**

Navigate to:

```bash
Home → Get Data → Text/CSV
```

Load the following datasets:

```bash
outputs/final_rankings.csv
outputs/skill_gap_report.csv
```

After importing:

```bash
Click Load
```

---

# Dashboard Architecture

## Page 1 — Hiring Overview Dashboard

### KPI Cards

Create KPI cards for:

- Total Applicants
- Shortlisted Candidates
- Average Match Score
- Highest Match Score

---

### Visualizations

#### Applicants per Job Role

Visualization Type:

```bash
Bar Chart
```

Fields:

- Axis → job_title
- Values → Count of candidate_name

---

#### Match Funnel Analysis

Visualization Type:

```bash
Funnel Chart
```

Stages:

- Excellent Match
- Good Match
- Partial Match
- Low Match

---

### Interactive Filters

Add slicers for:

- Job Title
- Match Level
- Shortlisted Status

---

# Page 2 — Candidate Rankings Dashboard

## Candidate Performance Table

Visualization Type:

```bash
Table
```

Columns:

- candidate_name
- job_title
- experience_years
- match_score
- final_score
- final_rank

---

## Conditional Formatting

Apply formatting on:

```bash
final_score
```

Rules:

- High scores → Green
- Medium scores → Yellow
- Low scores → Red

---

## Filters & Slicers

Add slicers for:

- job_title
- is_shortlisted
- experience_years

---

# Page 3 — Skill Gap Analysis Dashboard

## Skill Gap Matrix

Visualization Type:

```bash
Matrix
```

Configuration:

- Rows → skill
- Columns → job_title
- Values → Missing Skill Count

---

## Top Missing Skills

Visualization Type:

```bash
Horizontal Bar Chart
```

Fields:

- Axis → skill
- Values → frequency/count

---

# DAX Measures

## Average Match Score

```DAX
Avg Match Score =
AVERAGE(final_rankings[match_score])
```

---

## Shortlist Rate

```DAX
Shortlist Rate =
DIVIDE(
    COUNTROWS(
        FILTER(
            final_rankings,
            final_rankings[is_shortlisted] = 1
        )
    ),
    COUNTROWS(final_rankings)
)
```

---

## Total Applicants

```DAX
Total Applicants =
COUNTROWS(final_rankings)
```

---

## Total Shortlisted Candidates

```DAX
Total Shortlisted =
CALCULATE(
    COUNTROWS(final_rankings),
    final_rankings[is_shortlisted] = 1
)
```

---

## Highest Match Score

```DAX
Top Match Score =
MAX(final_rankings[match_score])
```

---

# Recommended Dashboard Design

## Theme Suggestions

- Dark Professional Theme
- Corporate Blue & White Theme
- Minimal HR Analytics Layout

---

## Recommended Visual Layout

### Top Section
- KPI Cards
- Global Filters

### Middle Section
- Ranking Charts
- Funnel Analysis

### Bottom Section
- Skill Gap Insights
- Candidate Tables

---

# Final Deliverables

The Power BI dashboard provides:

- AI-powered hiring analytics
- Resume ranking visualization
- Skill-gap intelligence
- Recruiter decision support
- Candidate shortlisting insights

---

# Recommended Export Options

```bash
File → Export
```

Supported Formats:

- PDF Report
- Power BI Service Dashboard
- PPT Presentation Export

---

# Final Workflow

```bash
Run Python Pipeline
        ↓
Generate CSV Outputs
        ↓
Load into Power BI
        ↓
Create Visualizations
        ↓
Build Interactive Dashboard
        ↓
Publish HR Analytics Report
```
