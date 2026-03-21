-- Pathway funnel: Among all enrolled students, counts and rates for program completion,
-- employment within 6 months, and full pathway achievement, by program_type and institution_type.

SELECT
    s.program_type,
    s.institution_type,
    COUNT(*) AS total_students,
    SUM(CASE WHEN o.completed_program THEN 1 ELSE 0 END) AS completed_program_count,
    ROUND(100.0 * AVG(CASE WHEN o.completed_program THEN 1.0 ELSE 0.0 END), 2) AS completion_rate_pct,
    SUM(CASE WHEN o.employed_within_6mo THEN 1 ELSE 0 END) AS employed_within_6mo_count,
    ROUND(100.0 * AVG(CASE WHEN o.employed_within_6mo THEN 1.0 ELSE 0.0 END), 2) AS employment_rate_pct,
    SUM(CASE WHEN o.pathway_achieved THEN 1 ELSE 0 END) AS pathway_achieved_count,
    ROUND(100.0 * AVG(CASE WHEN o.pathway_achieved THEN 1.0 ELSE 0.0 END), 2) AS pathway_achievement_rate_pct
FROM students s
INNER JOIN outcomes o ON o.student_id = s.student_id
GROUP BY s.program_type, s.institution_type
ORDER BY s.program_type, s.institution_type;
