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

STEM_COURSE_OPTIONS = [
    "Astronomy and Astrophysics",
    "Atmospheric Sciences and Meteorology",
    "Biochemistry and Biophysics",
    "Biology/Biological Sciences",
    "Chemistry",
    "Earth Sciences/Geological Sciences",
    "Marine Biology and Oceanography",
    "Neuroscience and Biopsychology",
    "Physics",
    "Pharmacology and Toxicology",
    "Computer Science",
    "Information Technology",
    "Cybersecurity/Information Assurance",
    "Data Science/Data Processing",
    "Software Engineering/Applications",
    "Computer Engineering",
    "Applied Mathematics",
    "Mathematics, General",
    "Statistics",
    "Biostatistics",
    "Actuarial Science",
    "Environmental Science/Studies",
    "Other",
]

CERT_OPTIONS = [
    "PMI Lean Project Management Certification",
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


def normalize_educations(educations):
    """Normalize education data and extract key qualifications."""
    highest_rank = -1
    highest_level = None
    has_bachelors_cs = False
    has_masters_cs = False

    for edu in educations:
        level = edu["highest_degree"]
        field = edu["degree_field"]

        rank = _LEVEL_RANK.get(level, -1)

        if rank > highest_rank:
            highest_rank = rank
            highest_level = level

        if field == "Computer Science":
            if rank >= 2:  # Bachelor's or higher
                has_bachelors_cs = True
            if rank >= 3:  # Master's or higher
                has_masters_cs = True

    return {
        "educations": educations,
        "highest_degree_obtained": highest_level,
        "has_bachelors_cs": has_bachelors_cs,
        "has_masters_cs": has_masters_cs,
    }


def normalize_courses(selected, other_text):
    """Normalize course data and extract relevant coursework."""
    text = (other_text or "").lower()

    python_coursework = "Computer Science" in selected or "python" in text or "programming" in text
    se_coursework = "Software Engineering/Applications" in selected or "software engineering" in text
    agile_coursework = "agile" in text or "scrum" in text or "kanban" in text

    return {
        "courses_selected": selected,
        "python_coursework": python_coursework,
        "se_coursework": se_coursework,
        "agile_coursework": agile_coursework,
    }


def normalize_certs(selected, other_text):
    """Normalize certification data."""
    text = (other_text or "").lower()
    
    return {
        "has_pmi_lean": "PMI Lean Project Management Certification" in selected or "pmi" in text,
    }


# Complete positions list with all requirements from the spec
POSITIONS = [
    {
        "name": "Entry-Level Python Engineer",
        "required": [
            ("python_coursework", "bool", True, "Python course work is required"),
            ("se_coursework", "bool", True, "Software Engineering course work is required"),
            ("agile_coursework", "bool", True, "Agile course is required"),
            ("has_bachelors_cs", "bool", True, "Bachelor in CS is required"),
        ],
        "desired": []  # No desired skills listed for this position
    },
    {
        "name": "Python Engineer",
        "required": [
            ("python_years", "min", 3, "At least 3 years Python development is required"),
            ("data_years", "min", 1, "At least 1 year data development is required"),
            ("has_bachelors_cs", "bool", True, "Bachelor in CS is required"),
        ],
        "desired": [
            ("agile_years", "min", 1, "Experience in Agile projects is desired"),
            ("has_git", "bool", True, "Git experience is desired"),
        ]
    },
    {
        "name": "Project Manager",
        "required": [
            ("project_mgmt_years", "min", 3, "At least 3 years managing software projects is required"),
            ("agile_years", "min", 2, "At least 2 years experience in Agile projects is required"),
        ],
        "desired": [
            ("has_pmi_lean", "bool", True, "PMI Lean Project Management Certification is desired"),
        ]
    },
    {
        "name": "Senior Knowledge Engineer",
        "required": [
            ("python_years", "min", 4, "At least 4 years using Python to develop is required"),
            ("expert_systems_years", "min", 2, "At least 2 years developing Expert Systems is required"),
            ("data_architecture_years", "min", 2, "At least 2 years data architecture and data development is required"),
            ("has_masters_cs", "bool", True, "Master's in CS is required"),
        ],
        "desired": []  # No desired skills listed for this position
    },
]