-- Top 5 candidates per job role
SELECT j.job_title, c.candidate_name, c.experience_years,
       m.match_score, m.final_score, m.final_rank
FROM match_results m
JOIN candidates c ON m.resume_id = c.resume_id
JOIN job_roles  j ON m.job_id    = j.job_id
WHERE m.final_rank <= 5
ORDER BY j.job_title, m.final_rank;

-- Match level distribution
SELECT match_level, COUNT(*) AS count,
       ROUND(AVG(final_score),1) AS avg_score
FROM match_results
GROUP BY match_level ORDER BY avg_score DESC;

-- Experience group analysis
SELECT CASE WHEN c.experience_years=0 THEN 'Fresher'
            WHEN c.experience_years<=2 THEN '1-2 Years'
            WHEN c.experience_years<=4 THEN '3-4 Years'
            ELSE '5+ Years' END AS exp_group,
       COUNT(DISTINCT c.resume_id) AS candidates,
       ROUND(AVG(m.final_score),1) AS avg_score,
       SUM(m.is_shortlisted) AS shortlisted
FROM match_results m JOIN candidates c ON m.resume_id=c.resume_id
GROUP BY exp_group ORDER BY avg_score DESC;

-- Skill gap summary
SELECT skill, SUM(has_skill) AS have, SUM(gap) AS missing,
       ROUND(SUM(gap)*100.0/COUNT(*),1) AS gap_pct
FROM skill_gap GROUP BY skill ORDER BY gap_pct DESC;

-- Hiring funnel
SELECT match_level, COUNT(*) AS count,
       ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),1) AS pct
FROM match_results GROUP BY match_level ORDER BY count DESC;

-- Shortlisted candidates
SELECT c.candidate_name, j.job_title, j.company,
       c.experience_years, m.match_score, m.final_score
FROM match_results m
JOIN candidates c ON m.resume_id=c.resume_id
JOIN job_roles  j ON m.job_id=j.job_id
WHERE m.is_shortlisted=1
ORDER BY m.final_score DESC;
