"""
Synthetic CampusEvolve pathway dataset generator.
Writes six CSVs under data/raw/: students, enrollments, financial_aid, courses, interventions, outcomes.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

SEED = 42
rng = np.random.default_rng(SEED)
fake = Faker("en_US")
Faker.seed(SEED)

OUT_DIR = Path(__file__).resolve().parent / "data" / "raw"
N_STUDENTS = 50000

GENDERS = ["Male", "Female", "Non-binary"]
GENDER_P = [0.46, 0.50, 0.04]

RACES = ["White", "Black", "Hispanic", "Asian", "Other"]
RACE_P = [0.52, 0.12, 0.20, 0.08, 0.08]

INCOME_BRACKETS = ["Low", "Middle", "High"]
INCOME_P = [0.32, 0.48, 0.20]

PROGRAM_TYPES = ["Associate", "Bachelor", "Certificate", "Bootcamp"]
PROGRAM_P = [0.28, 0.42, 0.18, 0.12]

INSTITUTION_TYPES = [
    "Community College",
    "4-Year Public",
    "4-Year Private",
    "Workforce Program",
]
INST_P = [0.35, 0.30, 0.22, 0.13]

PROGRAM_SEMESTERS_FT = {
    "Associate": 4,
    "Bachelor": 8,
    "Certificate": 2,
    "Bootcamp": 2,
}

INTERVENTION_TYPES = [
    "Advising",
    "Tutoring",
    "Financial Aid Counseling",
    "Peer Mentoring",
    "AI Guide",
]
TRIGGER_REASONS = ["GPA drop", "withdrawal risk", "aid gap", "gateway course failure"]


def _build_course_catalog() -> list[dict[str, object]]:
    """Shared institutional catalog (~150 courses); sampled per student-semester."""
    rows: list[dict[str, object]] = []

    def add_block(area: str, specs: list[tuple[str, str, bool]]) -> None:
        for course_id, course_name, gateway_course in specs:
            rows.append(
                {
                    "course_id": course_id,
                    "course_name": course_name,
                    "subject_area": area,
                    "gateway_course": gateway_course,
                }
            )

    add_block(
        "STEM",
        [
            ("MATH101", "MATH 101 - College Algebra", True),
            ("MATH102", "MATH 102 - Trigonometry", False),
            ("MATH151", "MATH 151 - Calculus I", False),
            ("MATH152", "MATH 152 - Calculus II", False),
            ("STAT200", "STAT 200 - Introduction to Statistics", False),
            ("CS101", "CS 101 - Introduction to Programming", True),
            ("CS201", "CS 201 - Data Structures", False),
            ("CS220", "CS 220 - Database Systems", False),
            ("CS301", "CS 301 - Algorithms", False),
            ("CS340", "CS 340 - Operating Systems", False),
            ("PHYS101", "PHYS 101 - General Physics I", True),
            ("PHYS102", "PHYS 102 - General Physics II", False),
            ("PHYS201", "PHYS 201 - Modern Physics", False),
            ("CHEM101", "CHEM 101 - General Chemistry I", True),
            ("CHEM102", "CHEM 102 - General Chemistry II", False),
            ("CHEM201", "CHEM 201 - Organic Chemistry I", False),
            ("CHEM210", "CHEM 210 - Biochemistry", False),
            ("BIOL101", "BIOL 101 - Biology I", True),
            ("BIOL102", "BIOL 102 - Biology II", False),
            ("BIOL201", "BIOL 201 - Genetics", False),
            ("BIOL210", "BIOL 210 - Microbiology", False),
            ("MATH201", "MATH 201 - Linear Algebra", False),
            ("MATH215", "MATH 215 - Differential Equations", False),
            ("STAT350", "STAT 350 - Applied Regression", False),
            ("CS250", "CS 250 - Discrete Mathematics", False),
        ],
    )
    add_block(
        "Humanities",
        [
            ("ENG101", "ENG 101 - Composition I", True),
            ("ENG102", "ENG 102 - Composition II", True),
            ("ENG201", "ENG 201 - Technical Writing", False),
            ("ENG210", "ENG 210 - Literature Survey", False),
            ("ENG215", "ENG 215 - Creative Writing", False),
            ("ENG240", "ENG 240 - Public Speaking", False),
            ("ENG255", "ENG 255 - Literature and Culture", False),
            ("ENG301", "ENG 301 - Advanced Composition", False),
            ("HIST101", "HIST 101 - U.S. History I", True),
            ("HIST102", "HIST 102 - U.S. History II", False),
            ("HIST110", "HIST 110 - World Civilizations", False),
            ("HIST210", "HIST 210 - Modern Europe", False),
            ("HIST215", "HIST 215 - African American History", False),
            ("HIST240", "HIST 240 - Latin American History", False),
            ("HIST255", "HIST 255 - Ancient History", False),
            ("HIST301", "HIST 301 - American Government", False),
            ("PHIL101", "PHIL 101 - Introduction to Philosophy", True),
            ("PHIL150", "PHIL 150 - Bioethics", False),
            ("PHIL200", "PHIL 200 - Logic", False),
            ("PHIL220", "PHIL 220 - Ethics", False),
            ("PHIL310", "PHIL 310 - Political Philosophy", False),
            ("LANG101", "LANG 101 - Spanish I", False),
            ("LANG102", "LANG 102 - Spanish II", False),
            ("LANG150", "LANG 150 - French I", False),
            ("LANG201", "LANG 201 - Spanish III", False),
        ],
    )
    add_block(
        "Business",
        [
            ("BUS101", "BUS 101 - Introduction to Business", True),
            ("ACCT101", "ACCT 101 - Financial Accounting", True),
            ("ACCT102", "ACCT 102 - Managerial Accounting", False),
            ("ACCT301", "ACCT 301 - Intermediate Accounting", False),
            ("ACCT350", "ACCT 350 - Taxation", False),
            ("ECON101", "ECON 101 - Microeconomics", True),
            ("ECON102", "ECON 102 - Macroeconomics", False),
            ("ECON301", "ECON 301 - Econometrics", False),
            ("ECON310", "ECON 310 - Labor Economics", False),
            ("MKTG101", "MKTG 101 - Principles of Marketing", False),
            ("MKTG220", "MKTG 220 - Consumer Behavior", False),
            ("MKTG310", "MKTG 310 - Digital Marketing", False),
            ("MGMT101", "MGMT 101 - Organizational Behavior", False),
            ("MGMT301", "MGMT 301 - Operations Management", False),
            ("MGMT340", "MGMT 340 - Human Resources", False),
            ("MGMT360", "MGMT 360 - Strategic Management", False),
            ("FIN301", "FIN 301 - Corporate Finance", False),
            ("FIN320", "FIN 320 - Financial Modeling", False),
            ("FIN350", "FIN 350 - Investments", False),
            ("BUS210", "BUS 210 - Business Law", False),
            ("BUS220", "BUS 220 - Business Statistics", False),
            ("BUS240", "BUS 240 - Entrepreneurship", False),
            ("BUS250", "BUS 250 - International Business", False),
            ("BUS310", "BUS 310 - Supply Chain Management", False),
            ("BUS330", "BUS 330 - Business Analytics", False),
        ],
    )
    add_block(
        "Healthcare",
        [
            ("NURS110", "NURS 110 - Foundations of Nursing", True),
            ("NURS150", "NURS 150 - Health Assessment", False),
            ("NURS210", "NURS 210 - Medical-Surgical Nursing", False),
            ("NURS220", "NURS 220 - Pharmacology for Nurses", False),
            ("NURS230", "NURS 230 - Pediatric Nursing", False),
            ("NURS240", "NURS 240 - Obstetric Nursing", False),
            ("NURS260", "NURS 260 - Gerontology Nursing", False),
            ("NURS310", "NURS 310 - Critical Care Nursing", False),
            ("NURS320", "NURS 320 - Mental Health Nursing", False),
            ("HLTH101", "HLTH 101 - Introduction to Public Health", True),
            ("HLTH150", "HLTH 150 - Epidemiology", False),
            ("HLTH210", "HLTH 210 - Health Policy", False),
            ("HLTH220", "HLTH 220 - Nutrition", False),
            ("HLTH230", "HLTH 230 - Community Health", False),
            ("HLTH240", "HLTH 240 - Global Health", False),
            ("HLTH301", "HLTH 301 - Health Informatics", False),
            ("HLTH310", "HLTH 310 - Healthcare Ethics", False),
            ("ANAT101", "ANAT 101 - Anatomy and Physiology I", True),
            ("ANAT102", "ANAT 102 - Anatomy and Physiology II", False),
            ("ANAT150", "ANAT 150 - Medical Terminology", False),
            ("ANAT200", "ANAT 200 - Pathophysiology", False),
            ("ANAT301", "ANAT 301 - Advanced Anatomy", False),
            ("PHAR110", "PHAR 110 - Introduction to Pharmacology", False),
            ("PHAR220", "PHAR 220 - Drug Interactions", False),
            ("PHAR301", "PHAR 301 - Clinical Pharmacology", False),
        ],
    )
    add_block(
        "Social Science",
        [
            ("PSYC101", "PSYC 101 - Introduction to Psychology", True),
            ("PSYC210", "PSYC 210 - Developmental Psychology", False),
            ("PSYC220", "PSYC 220 - Abnormal Psychology", False),
            ("PSYC240", "PSYC 240 - Social Psychology", False),
            ("PSYC260", "PSYC 260 - Organizational Psychology", False),
            ("PSYC301", "PSYC 301 - Statistics for Psychology", False),
            ("PSYC310", "PSYC 310 - Cognitive Psychology", False),
            ("PSYC350", "PSYC 350 - Counseling Psychology", False),
            ("SOC101", "SOC 101 - Introduction to Sociology", True),
            ("SOC210", "SOC 210 - Social Problems", False),
            ("SOC240", "SOC 240 - Research Methods", False),
            ("SOC260", "SOC 260 - Social Inequality", False),
            ("SOC301", "SOC 301 - Urban Sociology", False),
            ("SOC310", "SOC 310 - Sociology of Education", False),
            ("SOC350", "SOC 350 - Criminology", False),
            ("POLI101", "POLI 101 - American Government", True),
            ("POLI210", "POLI 210 - Comparative Politics", False),
            ("POLI220", "POLI 220 - Public Administration", False),
            ("POLI240", "POLI 240 - Voting and Elections", False),
            ("POLI301", "POLI 301 - Political Theory", False),
            ("POLI310", "POLI 310 - International Relations", False),
            ("ANTH101", "ANTH 101 - Cultural Anthropology", False),
            ("ANTH210", "ANTH 210 - Archaeology", False),
            ("ANTH250", "ANTH 250 - Medical Anthropology", False),
            ("ANTH301", "ANTH 301 - Linguistic Anthropology", False),
        ],
    )
    add_block(
        "Arts",
        [
            ("ART101", "ART 101 - Drawing I", True),
            ("ART150", "ART 150 - Art History I", False),
            ("ART210", "ART 210 - Painting", False),
            ("ART250", "ART 250 - Photography", False),
            ("ART301", "ART 301 - Sculpture", False),
            ("ART310", "ART 310 - Printmaking", False),
            ("MUS101", "MUS 101 - Music Theory I", True),
            ("MUS150", "MUS 150 - Voice Technique", False),
            ("MUS210", "MUS 210 - Music History", False),
            ("MUS250", "MUS 250 - Composition", False),
            ("MUS301", "MUS 301 - Ensemble Performance", False),
            ("MUS310", "MUS 310 - Music Technology", False),
            ("THEA101", "THEA 101 - Introduction to Theatre", True),
            ("THEA150", "THEA 150 - Improvisation", False),
            ("THEA210", "THEA 210 - Acting I", False),
            ("THEA250", "THEA 250 - Directing", False),
            ("THEA301", "THEA 301 - Stage Production", False),
            ("THEA310", "THEA 310 - Script Analysis", False),
            ("DSGN101", "DSGN 101 - Graphic Design Foundations", True),
            ("DSGN150", "DSGN 150 - Web Design", False),
            ("DSGN210", "DSGN 210 - User Experience Design", False),
            ("DSGN220", "DSGN 220 - Typography", False),
            ("DSGN301", "DSGN 301 - Motion Graphics", False),
            ("DSGN310", "DSGN 310 - Portfolio Workshop", False),
            ("ART220", "ART 220 - Digital Media", False),
        ],
    )
    return rows


COURSE_CATALOG = _build_course_catalog()


def semester_to_aid_year(semester: str) -> int:
    season, y = semester.split()
    y = int(y)
    return y if season == "Fall" else y - 1


def iter_semesters(start_year: int, n: int) -> list[str]:
    out = []
    y = start_year
    season = "Fall"
    for _ in range(n):
        out.append(f"{season} {y}")
        if season == "Fall":
            season = "Spring"
        else:
            season = "Fall"
            y += 1
    return out


def grade_from_gpa(gpa: float, rng: np.random.Generator) -> str:
    if gpa >= 3.7:
        pool = ["A"] * 7 + ["B"] * 3
    elif gpa >= 3.0:
        pool = ["A"] * 2 + ["B"] * 6 + ["C"] * 2
    elif gpa >= 2.3:
        pool = ["B"] * 2 + ["C"] * 6 + ["D"] * 2
    elif gpa >= 1.7:
        pool = ["C"] * 3 + ["D"] * 5 + ["F"] * 2
    else:
        pool = ["D"] * 3 + ["F"] * 5 + ["C"] * 2
    return str(rng.choice(pool))


def build_aid_template_for_student(
    enrollment_year: int,
    income: str,
) -> dict[int, dict]:
    """Pre-generate aid packages by academic year (Fall year = aid_year)."""
    aid_by_year: dict[int, dict] = {}
    for ay in range(enrollment_year - 1, enrollment_year + 12):
        if income == "Low":
            pell = float(rng.uniform(3500, 6495))
            loans = float(rng.uniform(0, 9500))
            schol = float(rng.uniform(0, 4000))
            unmet = float(rng.uniform(2500, 12000))
        elif income == "Middle":
            pell = float(rng.uniform(0, 3500))
            loans = float(rng.uniform(2000, 12500))
            schol = float(rng.uniform(500, 6000))
            unmet = float(rng.uniform(800, 7500))
        else:
            pell = 0.0
            loans = float(rng.uniform(0, 8000))
            schol = float(rng.uniform(1000, 10000))
            unmet = float(rng.uniform(0, 4000))

        unmet = round(unmet, 2)
        aid_gap_flag = unmet > 3000
        aid_by_year[ay] = {
            "pell_grant": round(pell, 2),
            "loans": round(loans, 2),
            "scholarships": round(schol, 2),
            "unmet_need": unmet,
            "aid_gap_flag": aid_gap_flag,
        }
    return aid_by_year


def next_semester_outcome(
    sem_list: list[str],
    enroll_by_sem: dict[str, dict],
    intervention_sem: str,
    completed_program: bool,
) -> str:
    if intervention_sem not in sem_list:
        return "Withdrew" if not completed_program else "Graduated"
    j = sem_list.index(intervention_sem)
    if j + 1 >= len(sem_list):
        return "Graduated" if completed_program else "Withdrew"
    nxt = sem_list[j + 1]
    rec = enroll_by_sem[nxt]
    if rec["withdrew"]:
        return "Withdrew"
    return "Enrolled"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows_students = []
    for i in range(N_STUDENTS):
        sid = f"STU{i+1:06d}"
        age = int(rng.integers(17, 33))
        gender = rng.choice(GENDERS, p=GENDER_P)
        race = rng.choice(RACES, p=RACE_P)
        first_gen = bool(rng.random() < 0.41)
        income = rng.choice(INCOME_BRACKETS, p=INCOME_P)
        state = fake.state_abbr()
        enrollment_year = int(rng.integers(2018, 2023))
        program = rng.choice(PROGRAM_TYPES, p=PROGRAM_P)
        inst = rng.choice(INSTITUTION_TYPES, p=INST_P)

        rows_students.append(
            {
                "student_id": sid,
                "age_at_enrollment": age,
                "gender": gender,
                "race_ethnicity": race,
                "first_gen_status": first_gen,
                "income_bracket": income,
                "state": state,
                "enrollment_year": enrollment_year,
                "program_type": program,
                "institution_type": inst,
            }
        )

    students_df = pd.DataFrame(rows_students)

    income_score = students_df["income_bracket"].map({"Low": 1.0, "Middle": 0.45, "High": 0.0})
    first_gen_score = students_df["first_gen_status"].astype(float)
    program_base = students_df["program_type"].map(
        {"Certificate": 0.72, "Bootcamp": 0.78, "Associate": 0.48, "Bachelor": 0.58}
    )
    noise = rng.normal(0, 0.10, N_STUDENTS)
    logit_complete = (
        np.log(program_base / (1 - program_base))
        - 0.28 * income_score
        - 0.20 * first_gen_score
        - 0.08 * (income_score * first_gen_score)
        + noise
    )
    p_complete = 1 / (1 + np.exp(-logit_complete))
    completed_program = rng.random(N_STUDENTS) < p_complete

    p_pt = 0.12 + 0.22 * income_score + 0.08 * (students_df["program_type"] == "Certificate")
    is_part_time = rng.random(N_STUDENTS) < p_pt

    enroll_rows: list[dict] = []
    course_rows: list[dict] = []
    aid_rows: list[dict] = []
    intervention_rows: list[dict] = []
    outcome_rows: list[dict] = []

    enr_i = aid_i = int_i = 0
    out_i = 0

    for idx, s in students_df.iterrows():
        sid = s["student_id"]
        enrollment_year = int(s["enrollment_year"])
        program = s["program_type"]
        income = s["income_bracket"]
        first_gen = s["first_gen_status"]
        complete = bool(completed_program[idx])
        part_time = bool(is_part_time[idx])

        base_semesters = PROGRAM_SEMESTERS_FT[program]
        n_semesters_need = int(np.ceil(base_semesters * (1.55 if part_time else 1.0)))
        n_semesters_need = max(n_semesters_need, 2)

        gpa_mean = 2.85
        if income == "Low":
            gpa_mean -= 0.22
        elif income == "High":
            gpa_mean += 0.12
        if first_gen:
            gpa_mean -= 0.08

        aid_by_year = build_aid_template_for_student(enrollment_year, income)

        sems = iter_semesters(enrollment_year, n_semesters_need + 8)
        cum_points = 0.0
        cum_credits = 0
        prev_gpa = float(rng.uniform(2.4, 3.5))
        withdrew_before = False
        gateway_failed = False
        any_aid_gap = False
        low_gpa_sem = False

        stop_idx = (n_semesters_need - 1) if complete else int(rng.integers(1, max(2, n_semesters_need)))

        student_enroll: list[dict] = []
        student_sem_order: list[str] = []

        for si, semester in enumerate(sems):
            if si > stop_idx:
                break

            credits_attempted = int(rng.integers(6, 10)) if part_time else int(rng.integers(12, 16))
            ay = semester_to_aid_year(semester)
            aid = aid_by_year.get(ay)
            if aid is None:
                aid = aid_by_year[enrollment_year]

            shock = rng.normal(0, 0.42)
            gpa_sem = float(np.clip(rng.normal(gpa_mean + shock, 0.38), 0.5, 4.0))
            if prev_gpa < 2.0 or aid["aid_gap_flag"]:
                gpa_sem -= rng.uniform(0, 0.35)
            gpa_sem = float(np.clip(gpa_sem, 0.5, 4.0))
            prev_gpa = gpa_sem

            if gpa_sem < 2.0:
                low_gpa_sem = True

            p_wd = 0.035
            if aid["aid_gap_flag"]:
                p_wd += 0.11 + min(0.12, aid["unmet_need"] / 80000)
                any_aid_gap = True
            if gpa_sem < 2.0:
                p_wd += 0.09
            if income == "Low":
                p_wd += 0.025
            if first_gen:
                p_wd += 0.02

            is_last_dropout = (not complete) and (si == stop_idx)
            withdrew = (is_last_dropout and rng.random() < 0.78) or (
                not is_last_dropout and rng.random() < p_wd
            )
            if withdrew:
                withdrew_before = True

            credits_completed = 0 if withdrew else credits_attempted
            if not withdrew:
                cum_points += gpa_sem * credits_attempted
                cum_credits += credits_attempted
            gpa_cumulative = round(cum_points / cum_credits, 3) if cum_credits > 0 else np.nan

            enr_i += 1
            rec = {
                "enrollment_id": f"ENR{enr_i:07d}",
                "student_id": sid,
                "semester": semester,
                "credits_attempted": credits_attempted,
                "credits_completed": credits_completed,
                "gpa_semester": round(gpa_sem, 3),
                "gpa_cumulative": gpa_cumulative,
                "enrollment_status": "Part-time" if part_time else "Full-time",
                "withdrew": withdrew,
            }
            enroll_rows.append(rec)
            student_enroll.append(rec)
            student_sem_order.append(semester)

            n_courses = max(3, min(6, credits_attempted // 3))
            picked = rng.choice(len(COURSE_CATALOG), size=n_courses, replace=False)
            for catalog_idx in picked:
                course = COURSE_CATALOG[int(catalog_idx)]
                cname = str(course["course_name"])
                subj = str(course["subject_area"])
                is_gateway = bool(course["gateway_course"])
                cid = str(course["course_id"])
                if withdrew:
                    grade = "W"
                    passed = False
                else:
                    grade = grade_from_gpa(gpa_sem + rng.normal(0, 0.25), rng)
                    passed = grade in ("A", "B", "C")
                    if is_gateway and grade in ("D", "F"):
                        gateway_failed = True

                course_rows.append(
                    {
                        "course_id": cid,
                        "student_id": sid,
                        "semester": semester,
                        "course_name": cname,
                        "subject_area": subj,
                        "grade": grade,
                        "passed": passed,
                        "gateway_course": is_gateway,
                    }
                )

            if withdrew and (not complete):
                break

        used_years = sorted({semester_to_aid_year(e["semester"]) for e in student_enroll})
        seen_aid: set[int] = set()
        for ay in used_years:
            if ay in seen_aid:
                continue
            seen_aid.add(ay)
            a = aid_by_year[ay]
            aid_i += 1
            aid_rows.append(
                {
                    "aid_id": f"AID{aid_i:07d}",
                    "student_id": sid,
                    "aid_year": ay,
                    "pell_grant": a["pell_grant"],
                    "loans": a["loans"],
                    "scholarships": a["scholarships"],
                    "unmet_need": a["unmet_need"],
                    "aid_gap_flag": a["aid_gap_flag"],
                }
            )

        enroll_by_sem = {e["semester"]: e for e in student_enroll}
        at_risk = low_gpa_sem or withdrew_before or any_aid_gap or gateway_failed or (not complete)

        if at_risk and rng.random() < 0.42:
            n_int = int(rng.integers(1, 4))
            for _ in range(n_int):
                sem = str(rng.choice(student_sem_order))
                trig = str(rng.choice(TRIGGER_REASONS))
                int_completed = bool(rng.random() < 0.78)
                next_out = next_semester_outcome(
                    student_sem_order, enroll_by_sem, sem, complete
                )
                int_i += 1
                intervention_rows.append(
                    {
                        "intervention_id": f"INT{int_i:07d}",
                        "student_id": sid,
                        "intervention_type": str(rng.choice(INTERVENTION_TYPES)),
                        "semester": sem,
                        "triggered_by": trig,
                        "completed": int_completed,
                        "outcome_next_semester": next_out,
                    }
                )

        last_sem = student_sem_order[-1] if student_sem_order else f"Fall {enrollment_year}"
        completion_year = None
        ttc = np.nan
        if complete:
            end_y = int(last_sem.split()[1])
            completion_year = end_y if rng.random() < 0.85 else end_y + 1
            ttc = round(float(rng.uniform(1.5, 5.5)), 2)

        employed = bool(complete and rng.random() < (0.62 + 0.15 * (income == "High")))
        if not complete:
            employed = bool(rng.random() < 0.35)

        if complete:
            if income == "High":
                sal = str(rng.choice(["$30K-$60K", "$60K-$100K", ">$100K"], p=[0.25, 0.45, 0.30]))
            elif income == "Middle":
                sal = str(
                    rng.choice(
                        ["<$30K", "$30K-$60K", "$60K-$100K", ">$100K"],
                        p=[0.15, 0.45, 0.35, 0.05],
                    )
                )
            else:
                sal = str(rng.choice(["<$30K", "$30K-$60K", "$60K-$100K"], p=[0.45, 0.45, 0.10]))
        else:
            sal = str(rng.choice(["<$30K", "$30K-$60K"], p=[0.7, 0.3]))

        pathway = bool(complete and employed)

        out_i += 1
        outcome_rows.append(
            {
                "outcome_id": f"OUT{out_i:07d}",
                "student_id": sid,
                "completed_program": complete,
                "completion_year": completion_year,
                "time_to_completion": ttc,
                "employed_within_6mo": employed,
                "salary_range": sal,
                "pathway_achieved": pathway,
            }
        )

    pd.DataFrame(rows_students).to_csv(OUT_DIR / "students.csv", index=False)
    pd.DataFrame(enroll_rows).to_csv(OUT_DIR / "enrollments.csv", index=False)
    pd.DataFrame(aid_rows).to_csv(OUT_DIR / "financial_aid.csv", index=False)
    pd.DataFrame(course_rows).to_csv(OUT_DIR / "courses.csv", index=False)
    pd.DataFrame(intervention_rows).to_csv(OUT_DIR / "interventions.csv", index=False)

    outcomes_df = pd.DataFrame(outcome_rows)
    outcomes_df.to_csv(OUT_DIR / "outcomes.csv", index=False)

    print(f"Wrote {N_STUDENTS} students and related tables to {OUT_DIR}")


if __name__ == "__main__":
    main()
