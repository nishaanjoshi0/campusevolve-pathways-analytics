-- At-risk flags: Per student, count risk signals (low GPA, withdrawal, aid gap, gateway failure),
-- output risk_score (0-4) and risk_tier (Low / Medium / High).

WITH signals AS (
    SELECT
        s.student_id,
        CASE WHEN EXISTS (
            SELECT 1
            FROM enrollments e
            WHERE e.student_id = s.student_id
              AND e.gpa_semester < 2.0
        ) THEN 1 ELSE 0 END AS gpa_below_2,
        CASE WHEN EXISTS (
            SELECT 1
            FROM enrollments e
            WHERE e.student_id = s.student_id
              AND e.withdrew = TRUE
        ) THEN 1 ELSE 0 END AS any_withdrawal,
        CASE WHEN EXISTS (
            SELECT 1
            FROM financial_aid f
            WHERE f.student_id = s.student_id
              AND f.aid_gap_flag = TRUE
        ) THEN 1 ELSE 0 END AS any_aid_gap,
        CASE WHEN EXISTS (
            SELECT 1
            FROM courses c
            WHERE c.student_id = s.student_id
              AND c.gateway_course = TRUE
              AND c.grade IN ('D', 'F')
        ) THEN 1 ELSE 0 END AS gateway_failure
    FROM students s
)
SELECT
    student_id,
    gpa_below_2,
    any_withdrawal,
    any_aid_gap,
    gateway_failure,
    (gpa_below_2 + any_withdrawal + any_aid_gap + gateway_failure) AS risk_score,
    CASE
        WHEN (gpa_below_2 + any_withdrawal + any_aid_gap + gateway_failure) <= 1 THEN 'Low'
        WHEN (gpa_below_2 + any_withdrawal + any_aid_gap + gateway_failure) = 2 THEN 'Medium'
        ELSE 'High'
    END AS risk_tier
FROM signals
ORDER BY student_id;
