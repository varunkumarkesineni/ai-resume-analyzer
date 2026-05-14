CREATE TABLE IF NOT EXISTS candidates (
    resume_id TEXT PRIMARY KEY, candidate_name TEXT, email TEXT,
    experience_years INTEGER DEFAULT 0, education TEXT, keywords TEXT
);
CREATE TABLE IF NOT EXISTS job_roles (
    job_id TEXT PRIMARY KEY, job_title TEXT, company TEXT,
    location TEXT, experience_required INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS match_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT, resume_id TEXT, job_id TEXT,
    match_score REAL, final_score REAL, final_rank INTEGER,
    match_level TEXT, is_shortlisted INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS skill_gap (
    id INTEGER PRIMARY KEY AUTOINCREMENT, candidate_name TEXT,
    job_title TEXT, skill TEXT, has_skill INTEGER, gap INTEGER
);
CREATE INDEX IF NOT EXISTS idx_score ON match_results(final_score);
CREATE INDEX IF NOT EXISTS idx_job   ON match_results(job_id);
