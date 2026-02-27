# knowledge_base.py

HIGHEST_DEGREE_OPTIONS = [
    "Doctoral Degree (Ph.D., D.B.A., Ed.D.)",
    "Professional Degree (J.D., M.D., Pharm.D.)",
    "Master’s Degree (M.A., M.S., M.B.A.)",
    "Bachelor’s Degree (B.A., B.S., B.F.A.)",
    "Associate Degree (A.A., A.S.)",
    "High School Diploma or GED",
]

DEGREE_FIELD_OPTIONS = [
    "Computer Science",
    "Software Engineering/Applications",
    "Information Technology",
    "Cybersecurity/Information Assurance",
    "Data Science/Data Processing",
    "Computer Engineering",
    "Management Information Systems",
    "Other",
]

# Actual course names
STEM_COURSE_OPTIONS = [
    # Computer Science and Programming
    "Introduction to Computer Science",
    "Data Structures and Algorithms",
    "Object-Oriented Programming",
    "Python Programming",
    "Java Programming",
    "C/C++ Programming",
    "Web Development",
    "Mobile App Development",
    "Database Management Systems",
    "Operating Systems",
    "Computer Networks",
    "Software Engineering",
    "Agile Software Development",
    "Scrum Master Fundamentals",
    "DevOps Principles",
    "Cloud Computing",
    "Machine Learning",
    "Artificial Intelligence",
    "Expert Systems",

    # Mathematics
    "Calculus I",
    "Calculus II",
    "Linear Algebra",
    "Discrete Mathematics",
    "Probability and Statistics",
    "Numerical Methods",

    # Data Science and Data Engineering
    "Data Science Fundamentals",
    "Big Data Analytics",
    "Data Visualization",
    "Data Architecture",
    "Data Engineering",

    # Other STEM
    "Physics I",
    "Physics II",
    "Chemistry I",
    "Biology I",
    "Environmental Science",

    "Other",
]

CERT_OPTIONS = [
    "PMI Lean Project Management Certification",
    "Certified Scrum Master (CSM)",
    "AWS Certified Developer",
    "Microsoft Certified: Azure Developer",
    "Google Professional Data Engineer",
    "Certified Information Systems Security Professional (CISSP)",
    "Project Management Professional (PMP)",
    "Other",
]

_LEVEL_RANK = {
    "High School Diploma or GED": 0,
    "Associate Degree (A.A., A.S.)": 1,
    "Bachelor’s Degree (B.A., B.S., B.F.A.)": 2,
    "Master’s Degree (M.A., M.S., M.B.A.)": 3,
    "Professional Degree (J.D., M.D., Pharm.D.)": 3,
    "Doctoral Degree (Ph.D., D.B.A., Ed.D.)": 4,
}

COURSE_WORK_EXAMPLES = {
    "python_coursework": [
        "Python Programming",
        "Introduction to Computer Science",
        "Data Structures and Algorithms",
        "Object-Oriented Programming",
    ],
    "se_coursework": [
        "Software Engineering",
        "Object-Oriented Programming",
        "DevOps Principles",
    ],
    "agile_coursework": [
        "Agile Software Development",
        "Scrum Master Fundamentals",
        "DevOps Principles",
    ],
}

def normalize_educations(educations):
    highest_rank = -1
    highest_level = None
    has_bachelors_cs = False
    has_masters_cs = False

    for edu in educations:
        level = edu.get("highest_degree")
        field = edu.get("degree_field")

        rank = _LEVEL_RANK.get(level, -1)
        if rank > highest_rank:
            highest_rank = rank
            highest_level = level

        if field == "Computer Science":
            if rank >= _LEVEL_RANK["Bachelor’s Degree (B.A., B.S., B.F.A.)"]:
                has_bachelors_cs = True
            if rank >= _LEVEL_RANK["Master’s Degree (M.A., M.S., M.B.A.)"]:
                has_masters_cs = True

    return {
        "educations": educations,
        "highest_degree_obtained": highest_level,
        "has_bachelors_cs": has_bachelors_cs,
        "has_masters_cs": has_masters_cs,
    }


def normalize_courses(selected, other_text):
    text = (other_text or "").lower()

    python_courses = {
        "Python Programming",
        "Introduction to Computer Science",
        "Data Structures and Algorithms",
        "Object-Oriented Programming",
    }
    se_courses = {
        "Software Engineering",
        "Object-Oriented Programming",
        "DevOps Principles",
    }
    agile_courses = {
        "Agile Software Development",
        "Scrum Master Fundamentals",
        "DevOps Principles",
    }
    expert_systems_courses = {
        "Expert Systems",
        "Artificial Intelligence",
        "Machine Learning",
    }
    data_courses = {
        "Data Science Fundamentals",
        "Big Data Analytics",
        "Data Visualization",
        "Data Architecture",
        "Data Engineering",
        "Database Management Systems",
    }

    python_coursework = any(c in python_courses for c in selected) or ("python" in text)
    se_coursework = any(c in se_courses for c in selected) or ("software engineering" in text)
    agile_coursework = any(c in agile_courses for c in selected) or any(t in text for t in ["agile", "scrum", "kanban"])
    expert_systems_coursework = any(c in expert_systems_courses for c in selected) or ("expert system" in text) or ("artificial intelligence" in text)
    data_coursework = any(c in data_courses for c in selected) or ("data engineering" in text) or ("data architecture" in text)

    return {
        "courses_selected": selected,
        "courses_other": other_text,
        "python_coursework": python_coursework,
        "se_coursework": se_coursework,
        "agile_coursework": agile_coursework,
        "expert_systems_coursework": expert_systems_coursework,
        "data_coursework": data_coursework,
    }


def normalize_certs(selected, other_text):
    text = (other_text or "").lower()

    return {
        "certs_selected": selected,
        "certs_other": other_text,
        "has_pmi_lean": ("PMI Lean Project Management Certification" in selected) or ("pmi lean" in text),
        "has_csm": ("Certified Scrum Master (CSM)" in selected) or ("scrum master" in text),
        "has_pmp": ("Project Management Professional (PMP)" in selected) or ("pmp" in text),
        "has_aws": "AWS Certified Developer" in selected,
        "has_azure": "Microsoft Certified: Azure Developer" in selected,
        "has_gcp": "Google Professional Data Engineer" in selected,
        "has_cissp": "Certified Information Systems Security Professional (CISSP)" in selected,
    }


# Spec aligned positions
# Spec aligned positions (matches the screenshot exactly)
POSITIONS = [
    {
        "name": "Entry-Level Python Engineer",
        "required": [
            ("python_coursework", "bool", True, "Python course work is required"),
            ("se_coursework", "bool", True, "Software Engineering course work is required"),
            ("has_bachelors_cs", "bool", True, "Bachelor in CS is required"),
        ],
        "desired": [
            ("agile_coursework", "bool", True, "Agile course is desired"),
        ],
    },
    {
        "name": "Python Engineer",
        "required": [
            ("python_years", "min", 3, "At least 3 years Python development is required"),
            ("data_years", "min", 1, "At least 1 year data development is required"),
            ("agile_projects", "bool", True, "Experience in Agile projects is required"),
            ("has_bachelors_cs", "bool", True, "Bachelor in CS is required"),
        ],
        "desired": [
            ("has_git", "bool", True, "Git experience is desired"),
        ],
    },
    {
        "name": "Project Manager",
        "required": [
            ("project_mgmt_years", "min", 3, "At least 3 years managing software projects is required"),
            ("agile_years", "min", 2, "At least 2 years experience in Agile projects is required"),
            ("has_pmi_lean", "bool", True, "PMI Lean Project Management Certification is required"),
        ],
        "desired": [],
    },
    {
        "name": "Senior Knowledge Engineer",
        "required": [
            ("python_years", "min", 4, "At least 4 years using Python to develop is required"),
            ("expert_systems_years", "min", 2, "At least 2 years developing Expert Systems is required"),
            ("data_architecture_years", "min", 2, "At least 2 years data architecture and data development is required"),
            ("has_masters_cs", "bool", True, "Masters in CS is required"),
        ],
        "desired": [],
    },
]