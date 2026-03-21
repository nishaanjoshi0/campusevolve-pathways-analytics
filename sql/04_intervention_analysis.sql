-- Intervention analysis: For at-risk students, compare next-semester outcomes (Enrolled / Withdrew / Graduated)
-- between those who completed at least one intervention vs those who received no intervention.
-- Shows distribution and lift in positive outcomes (Enrolled + Graduated).

WITH term_order AS (
    SELECT
        e.student_id,
        e.semester,
        e.withdrew,
        CASE split_part(e.semester, ' ', 1)
            WHEN 'Fall' THEN 2 * split_part(e.semester, ' ', 2)::int
            WHEN 'Spring' THEN 2 * split_part(e.semester, ' ', 2)::int - 1
        END AS term_seq
    FROM enrollments e
),
enroll_ranked AS (
    SELECT
        student_id,
        semester,
        withdrew,
        ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY term_seq, semester) AS rn
    FROM term_order
),
risk AS (
    SELECT
        s.student_id,
        (CASE WHEN EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id AND e.gpa_semester < 2.0) THEN 1 ELSE 0 END
            + CASE WHEN EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id AND e.withdrew = TRUE) THEN 1 ELSE 0 END
            + CASE WHEN EXISTS (SELECT 1 FROM financial_aid f WHERE f.student_id = s.student_id AND f.aid_gap_flag = TRUE) THEN 1 ELSE 0 END
            + CASE WHEN EXISTS (SELECT 1 FROM courses c WHERE c.student_id = s.student_id AND c.gateway_course = TRUE AND c.grade IN ('D', 'F')) THEN 1 ELSE 0 END
        ) AS risk_score
    FROM students s
),
at_risk AS (
    SELECT student_id
    FROM risk
    WHERE risk_score >= 2
),
int_sem AS (
    SELECT
        i.student_id,
        i.semester,
        i.outcome_next_semester,
        i.completed,
        CASE split_part(i.semester, ' ', 1)
            WHEN 'Fall' THEN 2 * split_part(i.semester, ' ', 2)::int
            WHEN 'Spring' THEN 2 * split_part(i.semester, ' ', 2)::int - 1
        END AS term_seq
    FROM interventions i
),
first_completed_intervention AS (
    SELECT DISTINCT ON (i.student_id)
        i.student_id,
        i.outcome_next_semester AS outcome
    FROM int_sem i
    INNER JOIN at_risk ar ON ar.student_id = i.student_id
    WHERE i.completed = TRUE
    ORDER BY i.student_id, i.term_seq, i.semester
),
no_intervention AS (
    SELECT ar.student_id
    FROM at_risk ar
    WHERE NOT EXISTS (SELECT 1 FROM interventions i WHERE i.student_id = ar.student_id)
),
first_enroll_next AS (
    SELECT
        e1.student_id,
        e2.withdrew AS next_withdrew,
        e2.rn AS next_rn
    FROM enroll_ranked e1
    LEFT JOIN enroll_ranked e2
        ON e2.student_id = e1.student_id
       AND e2.rn = e1.rn + 1
    WHERE e1.rn = 1
),
derived_no_int AS (
    SELECT
        n.student_id,
        CASE
            WHEN o.completed_program AND fen.next_rn IS NULL THEN 'Graduated'
            WHEN fen.next_withdrew = TRUE THEN 'Withdrew'
            WHEN fen.next_rn IS NOT NULL THEN 'Enrolled'
            WHEN NOT o.completed_program AND fen.next_rn IS NULL THEN 'Withdrew'
            ELSE 'Enrolled'
        END AS outcome
    FROM no_intervention n
    INNER JOIN first_enroll_next fen ON fen.student_id = n.student_id
    INNER JOIN outcomes o ON o.student_id = n.student_id
),
agg_completed AS (
    SELECT
        'completed_intervention'::text AS cohort,
        outcome,
        COUNT(*) AS outcome_count
    FROM first_completed_intervention
    GROUP BY outcome
),
agg_none AS (
    SELECT
        'no_intervention'::text AS cohort,
        outcome,
        COUNT(*) AS outcome_count
    FROM derived_no_int
    GROUP BY outcome
),
combined AS (
    SELECT * FROM agg_completed
    UNION ALL
    SELECT * FROM agg_none
),
cohort_sizes AS (
    SELECT cohort, SUM(outcome_count) AS cohort_total
    FROM combined
    GROUP BY cohort
),
positive_rates AS (
    SELECT
        c.cohort,
        SUM(c.outcome_count) FILTER (WHERE c.outcome IN ('Enrolled', 'Graduated'))::numeric
            / NULLIF(cs.cohort_total, 0) AS positive_rate
    FROM combined c
    INNER JOIN cohort_sizes cs ON cs.cohort = c.cohort
    GROUP BY c.cohort, cs.cohort_total
)
SELECT
    c.cohort,
    c.outcome,
    c.outcome_count,
    cs.cohort_total,
    ROUND(100.0 * c.outcome_count / NULLIF(cs.cohort_total, 0), 2) AS pct_of_cohort,
    ROUND(100.0 * pr.positive_rate, 2) AS cohort_positive_outcome_rate_pct,
    ROUND(
        100.0 * (
            (SELECT positive_rate FROM positive_rates WHERE cohort = 'completed_intervention')
            - (SELECT positive_rate FROM positive_rates WHERE cohort = 'no_intervention')
        ),
        2
    ) AS lift_positive_rate_pct_points
FROM combined c
INNER JOIN cohort_sizes cs ON cs.cohort = c.cohort
INNER JOIN positive_rates pr ON pr.cohort = c.cohort
ORDER BY c.cohort, c.outcome;
