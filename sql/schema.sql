DROP TABLE IF EXISTS outcomes CASCADE;
DROP TABLE IF EXISTS interventions CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS financial_aid CASCADE;
DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students (
    student_id VARCHAR PRIMARY KEY,
    age_at_enrollment INTEGER NOT NULL,
    gender VARCHAR NOT NULL,
    race_ethnicity VARCHAR NOT NULL,
    first_gen_status BOOLEAN NOT NULL,
    income_bracket VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    enrollment_year SMALLINT NOT NULL,
    program_type VARCHAR NOT NULL,
    institution_type VARCHAR NOT NULL
);

CREATE INDEX idx_students_income_bracket ON students (income_bracket);
CREATE INDEX idx_students_first_gen_status ON students (first_gen_status);

CREATE TABLE enrollments (
    enrollment_id VARCHAR PRIMARY KEY,
    student_id VARCHAR NOT NULL REFERENCES students (student_id),
    semester VARCHAR NOT NULL,
    credits_attempted INTEGER NOT NULL,
    credits_completed INTEGER NOT NULL,
    gpa_semester NUMERIC(10, 2),
    gpa_cumulative NUMERIC(10, 2),
    enrollment_status VARCHAR NOT NULL,
    withdrew BOOLEAN NOT NULL
);

CREATE INDEX idx_enrollments_student_id ON enrollments (student_id);
CREATE INDEX idx_enrollments_semester ON enrollments (semester);

CREATE TABLE financial_aid (
    aid_id VARCHAR PRIMARY KEY,
    student_id VARCHAR NOT NULL REFERENCES students (student_id),
    aid_year SMALLINT NOT NULL,
    pell_grant NUMERIC(10, 2) NOT NULL,
    loans NUMERIC(10, 2) NOT NULL,
    scholarships NUMERIC(10, 2) NOT NULL,
    unmet_need NUMERIC(10, 2) NOT NULL,
    aid_gap_flag BOOLEAN NOT NULL
);

CREATE INDEX idx_financial_aid_student_id ON financial_aid (student_id);
CREATE INDEX idx_financial_aid_aid_gap_flag ON financial_aid (aid_gap_flag);

CREATE TABLE courses (
    course_id VARCHAR NOT NULL,
    student_id VARCHAR NOT NULL REFERENCES students (student_id),
    semester VARCHAR NOT NULL,
    course_name VARCHAR NOT NULL,
    subject_area VARCHAR NOT NULL,
    grade VARCHAR NOT NULL,
    passed BOOLEAN NOT NULL,
    gateway_course BOOLEAN NOT NULL,
    PRIMARY KEY (course_id, student_id, semester)
);

CREATE INDEX idx_courses_student_id ON courses (student_id);
CREATE INDEX idx_courses_semester ON courses (semester);
CREATE INDEX idx_courses_gateway_course ON courses (gateway_course);
CREATE INDEX idx_courses_passed ON courses (passed);

CREATE TABLE interventions (
    intervention_id VARCHAR PRIMARY KEY,
    student_id VARCHAR NOT NULL REFERENCES students (student_id),
    intervention_type VARCHAR NOT NULL,
    semester VARCHAR NOT NULL,
    triggered_by VARCHAR NOT NULL,
    completed BOOLEAN NOT NULL,
    outcome_next_semester VARCHAR NOT NULL
);

CREATE INDEX idx_interventions_student_id ON interventions (student_id);
CREATE INDEX idx_interventions_semester ON interventions (semester);

CREATE TABLE outcomes (
    outcome_id VARCHAR PRIMARY KEY,
    student_id VARCHAR NOT NULL REFERENCES students (student_id),
    completed_program BOOLEAN NOT NULL,
    completion_year SMALLINT,
    time_to_completion NUMERIC(10, 2),
    employed_within_6mo BOOLEAN NOT NULL,
    salary_range VARCHAR NOT NULL,
    pathway_achieved BOOLEAN NOT NULL
);

CREATE INDEX idx_outcomes_student_id ON outcomes (student_id);
