# Student Pathway Completion Risk & Early Intervention Analytics
### A Data Science Framework for CampusEvolve's Pathways AI & Analytics

**Built by:** Ishan Joshi | [linkedin.com/in/ishannjoshi](https://linkedin.com/in/ishannjoshi) | nishaanjoshi0@gmail.com

**Repository:** [github.com/nishaanjoshi0/campusevolve-pathways-analytics](https://github.com/nishaanjoshi0/campusevolve-pathways-analytics)

---

## What This Project Is

CampusEvolve exists to simplify every learner's path to economic mobility. Their AI Guide provides personalized, natural-language guidance to help students navigate education-to-career pathways. But the AI Guide is only as good as the analytics infrastructure behind it.

This project answers a fundamental question: **what does a Founding Data Scientist at CampusEvolve need to build in their first 60-90 days to make the mission measurable, actionable, and equitable?**

The answer is a full analytics stack. From raw data to SQL queries to machine learning to executive dashboards, that tells you who is at risk, why they drop off, whether interventions are working, and who is being left behind.

---

## Why I Built This

Before building anything, I started with four business questions directly derived from CampusEvolve's mission:

1. Are students actually achieving economic mobility through education?
2. Who is falling off the pathway and why?
3. Are interventions reaching the students who need them most?
4. Are certain student groups being systematically left behind?

These four questions became the research framework for everything you see in this project.

---

## Key Findings

**Finding 1: Program type is the strongest structural predictor of completion**
Bootcamp (72%) and Certificate (67%) programs have the highest completion rates. Associate programs have the highest dropout risk at 42%. Institution type shows almost no variation, all four types cluster around 58-59%, meaning what you study matters far more than where you study.

**Finding 2: 44% of students are at High risk and over half receive no intervention**
Students are flagged as at-risk based on four early warning signals: GPA below 2.0, mid-semester withdrawal, financial aid gap, and gateway course failure. Counterintuitively, High risk students complete at 62% while Medium risk students only complete at 40%, because High risk students are receiving more interventions. Medium risk students are the most underserved segment.

**Finding 3: Pathway achievement has been flat at 38% for 4 years**
Only 38% of students complete their program AND find employment within 6 months. The 2022 cohort shows a dip but this is a data artifact as recent enrollees haven't had enough time to complete yet. The real opportunity is converting the 42% who complete their program but don't find employment within 6 months.

**Finding 4: Income and first-generation status drive the largest equity gaps**
Low income students complete at 50% vs 59% for high income students, a 9 point gap. First-generation students complete at 51% vs 57% for continuing-generation students. Race alone shows almost no completion gap once income and first-gen status are accounted for, meaning these are the true underlying drivers of inequity.

**Finding 5: A machine learning model can predict dropout with 96.8% AUC**
An XGBoost model trained on student-level features achieves 0.968 AUC on the test set, meaning it can reliably identify at-risk students 1-2 semesters before they drop out. The top three dropout risk drivers are total withdrawals, credits attempted, and program type.

---

## Recommendations

1. Invest more support resources in Associate and Bachelor programs where dropout risk is highest
2. Rebalance intervention targeting toward Medium risk students who are currently falling through the gaps
3. Scale intervention coverage before optimizing intervention type. More than half of at-risk students receive no intervention at all
4. Introduce proactive financial aid counseling and early advising for low-income and first-gen students in their very first semester, before risk signals appear
5. Deploy the dropout risk model as an early warning system that scores every student in real time

---

## What Was Built

This project delivers five interconnected components:

### 1. Synthetic Dataset (50,000 Students)
A fully synthetic dataset modeled on real IPEDS and NCES public education data. The data reflects real-world patterns: low-income and first-gen students have higher dropout rates, aid gaps correlate with withdrawals, and GPA follows a realistic distribution. The dataset spans 5 enrollment years (2018-2022) and generates over 1.2 million records across 6 tables.

### 2. Relational Database Schema (SQL)
A production-quality PostgreSQL schema with 6 tables, primary keys, foreign keys, and indexes on the most commonly queried columns. Five analytical SQL queries answer the core business questions.

### 3. Python Analysis Notebook
A full Jupyter notebook covering exploratory data analysis, equity disaggregation with statistical significance testing, feature engineering, dropout risk modeling, SHAP interpretability analysis, and Power BI export generation.

### 4. Power BI Dashboards
Three interactive dashboards built in CampusEvolve's brand colors (teal #00B5C8) for non-technical stakeholders:
- Pathway Completion Overview
- At-Risk Student Monitor
- Equity Outcomes

### 5. Executive Presentation
A 12-slide deck walking through the business questions, findings, model results, and next steps, designed for a CEO audience.

---

## Dashboard Preview

Built in Power BI using CampusEvolve's brand colors (teal #00B5C8). All 3 dashboard pages are available in the PDF below.

📊 **[View Full Dashboard PDF](assets/CampusEvolve%20Dashboards.pdf)**

**Page 1 - Pathway Completion Overview:** Completion rates by program type and institution, pathway achievement trend, and KPI cards showing 58.53% completion, 52.14% employment, and 38.04% pathway achievement.

**Page 2 - At-Risk Student Monitor:** Risk tier distribution across 50,000 students, intervention coverage by tier, and completion rates showing Medium risk students are the most underserved segment.

**Page 3 - Equity Outcomes:** Completion gaps by income bracket, race/ethnicity, first-generation status, and a waterfall chart showing income is the strongest driver of inequity.

---

## Schema Design

The dataset follows a **star schema** with `students` as the central fact table. All five child tables connect to students via `student_id`.

```
                    ┌─────────────┐
                    │  enrollments │
                    │  (219K rows) │
                    └──────┬──────┘
                           │
┌──────────────┐    ┌──────┴──────┐    ┌──────────────┐
│ financial_aid │────│   students  │────│    courses   │
│  (162K rows)  │    │ (50K rows)  │    │  (841K rows) │
└──────────────┘    └──────┬──────┘    └──────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
    ┌─────────┴──────┐       ┌──────────┴──────┐
    │  interventions  │       │    outcomes      │
    │   (41K rows)    │       │   (50K rows)     │
    └────────────────┘       └─────────────────┘
```

### Table Definitions

#### `students` — Core demographic table. One row per student.

| Column | Type | Description |
|---|---|---|
| student_id | VARCHAR (PK) | Unique student identifier |
| age_at_enrollment | INTEGER | Age when first enrolled |
| gender | VARCHAR | Male / Female / Non-binary |
| race_ethnicity | VARCHAR | White, Black, Hispanic, Asian, Other |
| first_gen_status | BOOLEAN | True if first in family to attend college |
| income_bracket | VARCHAR | Low (<$30K), Middle ($30K-$75K), High (>$75K) |
| state | VARCHAR | US state of residence |
| enrollment_year | SMALLINT | Year of first enrollment (2018-2022) |
| program_type | VARCHAR | Associate, Bachelor, Certificate, Bootcamp |
| institution_type | VARCHAR | Community College, 4-Year Public, 4-Year Private, Workforce Program |

#### `enrollments` — Semester-level records. One row per student per semester.

| Column | Type | Description |
|---|---|---|
| enrollment_id | VARCHAR (PK) | Unique identifier |
| student_id | VARCHAR (FK) | References students |
| semester | VARCHAR | e.g. Fall 2020, Spring 2021 |
| credits_attempted | INTEGER | Credits registered for |
| credits_completed | INTEGER | Credits actually completed |
| gpa_semester | NUMERIC(10,2) | GPA for that semester |
| gpa_cumulative | NUMERIC(10,2) | Cumulative GPA |
| enrollment_status | VARCHAR | Full-time / Part-time |
| withdrew | BOOLEAN | True if withdrew mid-semester |

#### `financial_aid` — Aid records per student per academic year.

| Column | Type | Description |
|---|---|---|
| aid_id | VARCHAR (PK) | Unique identifier |
| student_id | VARCHAR (FK) | References students |
| aid_year | SMALLINT | Academic year |
| pell_grant | NUMERIC(10,2) | Pell grant amount received |
| loans | NUMERIC(10,2) | Loan amount taken |
| scholarships | NUMERIC(10,2) | Scholarship amount |
| unmet_need | NUMERIC(10,2) | Remaining financial gap after aid |
| aid_gap_flag | BOOLEAN | True if unmet_need > $3,000 |

#### `courses` — Course-level completion data. One row per student per course per semester.

| Column | Type | Description |
|---|---|---|
| course_id | VARCHAR | Catalog course ID (shared across students) |
| student_id | VARCHAR (FK) | References students |
| semester | VARCHAR | Semester taken |
| course_name | VARCHAR | Course name from shared catalog (150 courses) |
| subject_area | VARCHAR | STEM, Humanities, Business, Healthcare, Social Science, Arts |
| grade | VARCHAR | A, B, C, D, F, W (withdrawn) |
| passed | BOOLEAN | True if grade is A, B, or C |
| gateway_course | BOOLEAN | True if this is a gateway/gatekeeper course |

#### `interventions` — Support interventions for at-risk students.

| Column | Type | Description |
|---|---|---|
| intervention_id | VARCHAR (PK) | Unique identifier |
| student_id | VARCHAR (FK) | References students |
| intervention_type | VARCHAR | Advising, Tutoring, Financial Aid Counseling, Peer Mentoring, AI Guide |
| semester | VARCHAR | When the intervention occurred |
| triggered_by | VARCHAR | GPA drop, withdrawal risk, aid gap, gateway course failure |
| completed | BOOLEAN | Whether the student engaged with the intervention |
| outcome_next_semester | VARCHAR | Enrolled / Withdrew / Graduated |

#### `outcomes` — Final outcome per student. One row per student.

| Column | Type | Description |
|---|---|---|
| outcome_id | VARCHAR (PK) | Unique identifier |
| student_id | VARCHAR (FK) | References students |
| completed_program | BOOLEAN | True if student completed their program |
| completion_year | SMALLINT | Year of completion (null if not completed) |
| time_to_completion | NUMERIC(10,2) | Years taken to complete |
| employed_within_6mo | BOOLEAN | True if employed within 6 months of completion |
| salary_range | VARCHAR | <$30K, $30K-$60K, $60K-$100K, >$100K |
| pathway_achieved | BOOLEAN | True if both completed AND employed |

---

## SQL Analytical Queries

Five production-quality SQL queries answer the core business questions:

| Query | Business Question |
|---|---|
| `01_cohort_retention.sql` | For each enrollment year cohort, how many students persisted after semester 1, 2, 3, and 4? |
| `02_atrisk_flags.sql` | Which students show early warning signals? Generate a risk score (0-4) and risk tier (Low/Medium/High). |
| `03_equity_disaggregation.sql` | How do completion and employment rates differ by income, first-gen status, and race/ethnicity? |
| `04_intervention_analysis.sql` | Do students who completed interventions have better next-semester outcomes than those who received none? |
| `05_pathway_funnel.sql` | Of all enrolled students, how many completed, got employed, and achieved the full pathway by program type? |

---

## Machine Learning Model

**Target variable:** `completed_program`

**Features:**
- Cumulative GPA mean
- Total withdrawals
- Total credits attempted
- Financial aid gap flag (ever)
- Gateway course failure flag (ever)
- Intervention engagement score
- Income bracket (encoded)
- Program type (encoded)
- First-generation status

**Results:**

| Model | AUC-ROC |
|---|---|
| Logistic Regression (baseline) | 0.9337 |
| XGBoost | 0.968 |

**Top 3 dropout risk drivers (SHAP):**
1. Total withdrawals
2. Credits attempted total
3. Program type: Bachelor

---

## Equity and Fairness Lens

All outputs are intentionally disaggregated by demographic dimensions. Key equity questions surfaced:

- Does the dropout risk model perform equally well across demographic groups?
- Are certain groups systematically less likely to receive interventions despite equal risk scores?
- Where are the largest completion and employment gaps and what drives them?

The analysis finds that income and first-generation status are the strongest drivers of inequity, not race independently. This has direct implications for how intervention resources should be targeted.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data generation | Python (Faker, NumPy, Pandas) |
| Relational schema | SQL (PostgreSQL-compatible) |
| Analysis | Python (Pandas, Scikit-learn, XGBoost, SHAP, Matplotlib, Seaborn, SciPy) |
| Visualization | Power BI Web (fed by CSV exports) |
| Version control | Git / GitHub |

---

## Project Structure

```
campusevolve-pathways-analytics/
│
├── data/
│   ├── raw/                           # Synthetic CSVs generated by generate_data.py
│   │   ├── students.csv               # 50,000 rows
│   │   ├── enrollments.csv            # ~219,000 rows
│   │   ├── financial_aid.csv          # ~162,000 rows
│   │   ├── courses.csv                # ~841,000 rows
│   │   ├── interventions.csv          # ~41,000 rows
│   │   └── outcomes.csv               # 50,000 rows
│   └── processed/
│       └── powerbi_exports/           # Aggregated flat files for Power BI
│           ├── dashboard_completion.csv
│           ├── dashboard_atrisk.csv
│           ├── dashboard_equity.csv
│           └── dashboard_interventions.csv
│
├── sql/
│   ├── schema.sql                     # Full DDL: tables, PKs, FKs, indexes
│   ├── 01_cohort_retention.sql
│   ├── 02_atrisk_flags.sql
│   ├── 03_equity_disaggregation.sql
│   ├── 04_intervention_analysis.sql
│   └── 05_pathway_funnel.sql
│
├── notebooks/
│   └── pathway_risk_analysis.ipynb    # Full Python analysis (7 sections)
│
├── presentation/
│   └── CampusEvolve_DS_Analysis.pptx  # 12-slide executive presentation
│
├── generate_data.py                   # Synthetic data generator
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## A Note on the Data

This project uses a fully synthetic dataset. No real student data was used. The data is modeled on publicly available IPEDS and NCES patterns to ensure realistic distributions, but all student records are algorithmically generated.

In a real Founding DS role, the data engineering work would be significantly more complex: integrating across Student Information Systems (Banner, Peoplesoft), financial aid databases, LMS platforms, and partner institution exports, each with different schemas, formats, and data quality issues. This project demonstrates the analytical and modeling capabilities that would be applied to that real data.

---

*Built by Ishan Joshi as part of the application for Founding Data Scientist, Pathways AI & Analytics at CampusEvolve.*

*"Unlocking Potential | Empowering Minds" - CampusEvolve*
