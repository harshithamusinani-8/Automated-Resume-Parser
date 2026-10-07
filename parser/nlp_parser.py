import re


SKILLS = [
    "HTML", "CSS", "JavaScript", "C", "C++", "Java", "Python",
    "React", "Angular", "Node.js", "Flask", "Django", "FastAPI",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Git", "GitHub",
    "VS Code", "Power BI", "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "NLP", "Docker", "AWS", "Azure",
    "TypeScript", "REST API"
]

SOFT_SKILLS = [
    "Problem Solving", "Analytical Thinking", "Communication Skills",
    "Teamwork", "Time Management", "Adaptability", "Quick Learning",
    "Leadership", "Communication", "Creativity"
]

JOB_ROLES = {
    "Frontend Developer": {
        "skills": [
            "HTML", "CSS", "JavaScript", "React",
            "TypeScript", "Git", "REST API"
        ]
    },
    "Python Developer": {
        "skills": [
            "Python", "SQL", "Git", "FastAPI", "Django", "REST API"
        ]
    },
    "Java Developer": {
        "skills": [
            "Java", "SQL", "Git", "Spring", "REST API"
        ]
    },
    "Data Analyst": {
        "skills": [
            "Python", "SQL", "Power BI", "Excel"
        ]
    },
    "AI / ML Engineer": {
        "skills": [
            "Python", "Machine Learning",
            "Deep Learning", "Artificial Intelligence", "NLP"
        ]
    }
}


def extract_email(text: str):
    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )
    return match.group() if match else None


def extract_phone(text: str):
    matches = re.findall(
        r'(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)',
        text
    )
    return matches[0] if matches else None


def extract_name(text: str):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:12]:
        clean = re.sub(r'[^A-Za-z .]', '', line).strip()

        if (
            2 <= len(clean.split()) <= 8
            and "@" not in line
            and not re.search(r'\d', line)
            and clean.upper() == clean
        ):
            return clean.title()

    return lines[0] if lines else None


def extract_skills(text: str):
    found = []

    for skill in SKILLS:
        if re.search(
            r'(?<!\w)' + re.escape(skill) + r'(?!\w)',
            text,
            re.IGNORECASE
        ):
            found.append(skill)

    return found


def extract_soft_skills(text: str):
    found = []

    for skill in SOFT_SKILLS:
        if re.search(
            r'(?<!\w)' + re.escape(skill) + r'(?!\w)',
            text,
            re.IGNORECASE
        ):
            found.append(skill)

    return found


def get_section(text: str, headings):
    lines = text.splitlines()
    result = []
    active = False

    heading_pattern = re.compile(
        r'^\s*(?:' +
        "|".join(re.escape(h) for h in headings) +
        r')\s*:?\s*$',
        re.IGNORECASE
    )

    all_headings = [
        "CAREER OBJECTIVE", "SUMMARY", "PROFILE",
        "EDUCATION", "TECHNICAL SKILLS", "SKILLS",
        "PROJECTS", "CERTIFICATIONS", "ACHIEVEMENTS",
        "ACHIEVEMENTS & ACTIVITIES", "EXPERIENCE",
        "WORK EXPERIENCE", "SOFT SKILLS", "DECLARATION"
    ]

    stop_pattern = re.compile(
        r'^\s*(?:' +
        "|".join(re.escape(h) for h in all_headings) +
        r')\s*:?\s*$',
        re.IGNORECASE
    )

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if heading_pattern.match(stripped):
            active = True
            continue

        if active and stop_pattern.match(stripped):
            break

        if active:
            result.append(stripped)

    return result


def extract_education(text: str):
    lines = get_section(text, ["EDUCATION"])
    education = []

    for line in lines:
        if "—" not in line and "-" not in line:
            continue

        parts = re.split(r'\s*[—-]\s*', line, maxsplit=1)

        degree = parts[0].strip()
        remaining = parts[1].strip() if len(parts) > 1 else ""

        details = [x.strip() for x in remaining.split("|")]

        institution = details[0] if details else None
        year = None
        score = None
        status = None

        for detail in details[1:]:
            year_match = re.search(r'\b(19|20)\d{2}\b', detail)

            if year_match:
                year = year_match.group()

            if "cgpa" in detail.lower() or "%" in detail:
                score = detail.strip()
            elif (
                "pursuing" in detail.lower()
                or "year" in detail.lower()
            ):
                status = detail.strip()

        education.append({
            "degree": degree,
            "institution": institution,
            "year": year,
            "score": score,
            "status": status
        })

    return education


def extract_projects(text: str):
    lines = get_section(text, ["PROJECTS"])
    projects = []
    current = None

    for line in lines:
        clean = re.sub(r'^[•●▪◦\-]\s*', '', line).strip()

        if not clean:
            continue

        if (
            current is None
            or (
                not line.startswith(("•", "●", "▪", "◦", "-", "*"))
                and "Technologies Used:" not in clean
            )
        ):
            if current:
                projects.append(current)

            current = {
                "title": clean,
                "technologies": None,
                "description": []
            }

        elif "Technologies Used:" in clean:
            current["technologies"] = clean.split(
                "Technologies Used:", 1
            )[1].strip()

        else:
            current["description"].append(clean)

    if current:
        projects.append(current)

    return projects


def extract_certifications(text: str):
    lines = get_section(text, ["CERTIFICATIONS"])
    return [
        re.sub(r'^[•●▪◦\-]\s*', '', line).strip()
        for line in lines
        if line.strip()
    ]


def extract_achievements(text: str):
    lines = get_section(
        text,
        ["ACHIEVEMENTS", "ACHIEVEMENTS & ACTIVITIES"]
    )

    return [
        re.sub(r'^[•●▪◦\-]\s*', '', line).strip()
        for line in lines
        if line.strip()
    ]


def extract_summary(text: str):
    lines = get_section(
        text,
        ["CAREER OBJECTIVE", "SUMMARY", "PROFILE"]
    )
    return " ".join(lines).strip() if lines else None


def extract_linkedin(text: str):
    match = re.search(
        r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9._/-]+',
        text,
        re.IGNORECASE
    )
    return match.group().rstrip(".,)") if match else None


def extract_github(text: str):
    match = re.search(
        r'(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9._/-]+',
        text,
        re.IGNORECASE
    )
    return match.group().rstrip(".,)") if match else None


def calculate_resume_score(data):
    breakdown = {}

    personal = 0
    if data.get("name"):
        personal += 4
    if data.get("email"):
        personal += 4
    if data.get("phone"):
        personal += 4
    if data.get("linkedin") or data.get("github"):
        personal += 3
    breakdown["Personal Information"] = personal

    breakdown["Career Objective"] = 10 if data.get("summary") else 0

    skills_count = len(data.get("skills", []))
    if skills_count >= 8:
        skill_score = 20
    elif skills_count >= 5:
        skill_score = 15
    elif skills_count >= 3:
        skill_score = 10
    elif skills_count:
        skill_score = 5
    else:
        skill_score = 0
    breakdown["Technical Skills"] = skill_score

    education_count = len(data.get("education", []))
    breakdown["Education"] = (
        15 if education_count >= 2
        else 10 if education_count == 1
        else 0
    )

    project_count = len(data.get("projects", []))
    breakdown["Projects"] = (
        15 if project_count >= 2
        else 10 if project_count == 1
        else 0
    )

    certification_count = len(data.get("certifications", []))
    breakdown["Certifications"] = (
        10 if certification_count >= 3
        else 6 if certification_count >= 1
        else 0
    )

    breakdown["Achievements"] = 5 if data.get("achievements") else 0

    score = min(sum(breakdown.values()), 100)

    if score >= 85:
        rating = "Excellent"
    elif score >= 70:
        rating = "Good"
    elif score >= 50:
        rating = "Average"
    else:
        rating = "Needs Improvement"

    return {
        "score": score,
        "rating": rating,
        "breakdown": breakdown
    }


def calculate_ats_score(data):
    score = 0
    checks = []

    if data.get("name"):
        score += 10
        checks.append({"label": "Name detected", "status": "pass"})
    else:
        checks.append({"label": "Name missing", "status": "warning"})

    if data.get("email") and data.get("phone"):
        score += 15
        checks.append({"label": "Contact information complete", "status": "pass"})
    else:
        checks.append({"label": "Complete contact information", "status": "warning"})

    if data.get("skills"):
        score += 15
        checks.append({"label": "Skills section detected", "status": "pass"})
    else:
        checks.append({"label": "Skills section missing", "status": "warning"})

    if data.get("education"):
        score += 15
        checks.append({"label": "Education detected", "status": "pass"})
    else:
        checks.append({"label": "Education section missing", "status": "warning"})

    if data.get("projects"):
        score += 15
        checks.append({"label": "Projects detected", "status": "pass"})
    else:
        checks.append({"label": "Projects section missing", "status": "warning"})

    if data.get("certifications"):
        score += 10
        checks.append({"label": "Certifications detected", "status": "pass"})

    if data.get("summary"):
        score += 10
        checks.append({"label": "Career objective detected", "status": "pass"})

    if data.get("linkedin") or data.get("github"):
        score += 10
        checks.append({"label": "Professional profile link found", "status": "pass"})

    return {
        "score": min(score, 100),
        "checks": checks
    }


def calculate_job_match(data, role):
    role_data = JOB_ROLES.get(role)

    if not role_data:
        return {
            "role": role,
            "match": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    resume_skills = {
        skill.lower()
        for skill in data.get("skills", [])
    }

    required = role_data["skills"]

    matched = [
        skill for skill in required
        if skill.lower() in resume_skills
    ]

    missing = [
        skill for skill in required
        if skill.lower() not in resume_skills
    ]

    match = round(
        (len(matched) / len(required)) * 100
    ) if required else 0

    return {
        "role": role,
        "match": match,
        "matched_skills": matched,
        "missing_skills": missing
    }


def generate_suggestions(data, job_match):
    suggestions = []

    if not data.get("summary"):
        suggestions.append(
            "Add a short career objective or professional summary."
        )

    if len(data.get("skills", [])) < 5:
        suggestions.append(
            "Add more relevant technical skills to improve keyword coverage."
        )

    if not data.get("projects"):
        suggestions.append(
            "Add at least one project with technologies and measurable results."
        )

    elif len(data.get("projects", [])) == 1:
        suggestions.append(
            "Consider adding another project relevant to your target role."
        )

    if not data.get("linkedin") and not data.get("github"):
        suggestions.append(
            "Add a LinkedIn or GitHub profile link."
        )

    if job_match.get("missing_skills"):
        missing = ", ".join(job_match["missing_skills"][:4])
        suggestions.append(
            f"Consider adding or learning these target-role skills: {missing}."
        )

    if not data.get("achievements"):
        suggestions.append(
            "Add measurable achievements, hackathons, awards or activities."
        )

    if not suggestions:
        suggestions.append(
            "Your resume is well structured. Keep tailoring keywords to each job description."
        )

    return suggestions


def analyze_resume(data, target_role="Frontend Developer"):
    resume_score = calculate_resume_score(data)
    ats_score = calculate_ats_score(data)
    job_match = calculate_job_match(data, target_role)
    suggestions = generate_suggestions(data, job_match)

    return {
        "resume_score": resume_score,
        "ats_score": ats_score,
        "job_match": job_match,
        "suggestions": suggestions
    }


def parse_resume(text: str):
    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": extract_linkedin(text),
        "github": extract_github(text),
        "summary": extract_summary(text),
        "skills": extract_skills(text),
        "soft_skills": extract_soft_skills(text),
        "education": extract_education(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text),
        "achievements": extract_achievements(text)
    }

    data.update(
        analyze_resume(
            data,
            "Frontend Developer"
        )
    )

    return data
