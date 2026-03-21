-- Equity disaggregation: Completion and employment rates by income_bracket, first_gen_status,
-- and race_ethnicity, with student counts and gap vs overall average.

WITH overall AS (
    SELECT
        AVG(CASE WHEN o.completed_program THEN 1.0 ELSE 0.0 END) AS avg_completion_rate,
        AVG(CASE WHEN o.employed_within_6mo THEN 1.0 ELSE 0.0 END) AS avg_employment_rate
    FROM outcomes o
),
grouped AS (
    SELECT
        s.income_bracket,
        s.first_gen_status,
        s.race_ethnicity,
        COUNT(*) AS student_count,
        AVG(CASE WHEN o.completed_program THEN 1.0 ELSE 0.0 END) AS completion_rate,
        AVG(CASE WHEN o.employed_within_6mo THEN 1.0 ELSE 0.0 END) AS employment_rate
    FROM students s
    INNER JOIN outcomes o ON o.student_id = s.student_id
    GROUP BY s.income_bracket, s.first_gen_status, s.race_ethnicity
)
SELECT
    g.income_bracket,
    g.first_gen_status,
    g.race_ethnicity,
    g.student_count,
    ROUND(100.0 * g.completion_rate, 2) AS completion_rate_pct,
    ROUND(100.0 * g.employment_rate, 2) AS employment_rate_pct,
    ROUND(100.0 * (g.completion_rate - ov.avg_completion_rate), 2) AS completion_rate_gap_vs_overall_pct,
    ROUND(100.0 * (g.employment_rate - ov.avg_employment_rate), 2) AS employment_rate_gap_vs_overall_pct
FROM grouped g
CROSS JOIN overall ov
ORDER BY g.income_bracket, g.first_gen_status, g.race_ethnicity;
