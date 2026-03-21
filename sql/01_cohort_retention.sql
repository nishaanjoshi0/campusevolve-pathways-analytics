-- Cohort retention: For each enrollment_year cohort, how many students were still enrolled
-- after semester 1, 2, 3, and 4? Shows drop-off counts and retention rates at each stage.

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
        term_seq,
        ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY term_seq, semester) AS semester_index
    FROM term_order
),
per_student AS (
    SELECT
        s.student_id,
        s.enrollment_year,
        MAX(er.semester_index) AS max_semester_index
    FROM students s
    INNER JOIN enroll_ranked er ON er.student_id = s.student_id
    GROUP BY s.student_id, s.enrollment_year
),
cohort_stats AS (
    SELECT
        enrollment_year,
        COUNT(*) AS cohort_size,
        COUNT(*) FILTER (WHERE max_semester_index >= 2) AS retained_after_semester_1,
        COUNT(*) FILTER (WHERE max_semester_index >= 3) AS retained_after_semester_2,
        COUNT(*) FILTER (WHERE max_semester_index >= 4) AS retained_after_semester_3,
        COUNT(*) FILTER (WHERE max_semester_index >= 5) AS retained_after_semester_4
    FROM per_student
    GROUP BY enrollment_year
)
SELECT
    enrollment_year,
    cohort_size,
    retained_after_semester_1,
    cohort_size - retained_after_semester_1 AS drop_off_after_semester_1,
    ROUND(100.0 * retained_after_semester_1 / NULLIF(cohort_size, 0), 2) AS retention_rate_after_semester_1_pct,
    retained_after_semester_2,
    retained_after_semester_1 - retained_after_semester_2 AS drop_off_after_semester_2,
    ROUND(100.0 * retained_after_semester_2 / NULLIF(cohort_size, 0), 2) AS retention_rate_after_semester_2_pct,
    retained_after_semester_3,
    retained_after_semester_2 - retained_after_semester_3 AS drop_off_after_semester_3,
    ROUND(100.0 * retained_after_semester_3 / NULLIF(cohort_size, 0), 2) AS retention_rate_after_semester_3_pct,
    retained_after_semester_4,
    retained_after_semester_3 - retained_after_semester_4 AS drop_off_after_semester_4,
    ROUND(100.0 * retained_after_semester_4 / NULLIF(cohort_size, 0), 2) AS retention_rate_after_semester_4_pct
FROM cohort_stats
ORDER BY enrollment_year;
