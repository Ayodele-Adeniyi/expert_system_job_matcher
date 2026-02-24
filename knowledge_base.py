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

# Actual course names, not departments
STEM_COURSE_OPTIONS = [
    # Computer Science / Programming
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
    
    # Data Science
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

    # Check for Python-related courses
    python_courses = ["Python Programming", "Introduction to Computer Science", 
                     "Data Structures and Algorithms", "Object-Oriented Programming"]
    python_coursework = any(course in selected for course in python_courses) or "python" in text
    
    # Check for Software Engineering courses
    se_courses = ["Software Engineering", "Object-Oriented Programming", 
                 "Agile Software Development", "DevOps Principles"]
    se_coursework = any(course in selected for course in se_courses) or "software engineering" in text
    
    # Check for Agile/Scrum courses
    agile_courses = ["Agile Software Development", "Scrum Master Fundamentals", 
                    "DevOps Principles"]
    agile_coursework = any(course in selected for course in agile_courses) or any(term in text for term in ["agile", "scrum", "kanban"])
    
    # Check for Expert Systems courses
    expert_systems_courses = ["Expert Systems", "Artificial Intelligence", "Machine Learning"]
    expert_systems_coursework = any(course in selected for course in expert_systems_courses)
    
    # Check for Data courses
    data_courses = ["Data Science Fundamentals", "Big Data Analytics", "Data Visualization",
                   "Data Architecture", "Data Engineering", "Database Management Systems"]
    data_coursework = any(course in selected for course in data_courses)
    
    # Git might be covered in various courses, but we'll let the experience toggle handle it
    # since Git is typically learned through practice rather than dedicated courses

    return {
        "courses_selected": selected,
        "python_coursework": python_coursework,
        "se_coursework": se_coursework,
        "agile_coursework": agile_coursework,
        "expert_systems_coursework": expert_systems_coursework,
        "data_coursework": data_coursework,
    }


def normalize_certs(selected, other_text):
    """Normalize certification data."""
    text = (other_text or "").lower()
    
    return {
        "has_pmi_lean": "PMI Lean Project Management Certification" in selected or "pmi lean" in text,
        "has_csm": "Certified Scrum Master (CSM)" in selected or "scrum master" in text,
        "has_aws": "AWS Certified Developer" in selected,
        "has_azure": "Microsoft Certified: Azure Developer" in selected,
        "has_gcp": "Google Professional Data Engineer" in selected,
        "has_cissp": "Certified Information Systems Security Professional (CISSP)" in selected,
        "has_pmp": "Project Management Professional (PMP)" in selected,
    }


# Complete positions list with all requirements from the spec
POSITIONS = [
    {
        "name": "Entry-Level Python Engineer",
        "required": [
            ("python_coursework", "bool", True, "Python programming course is required"),
            ("se_coursework", "bool", True, "Software Engineering course is required"),
            ("agile_coursework", "bool", True, "Agile/Scrum course is required"),
            ("has_bachelors_cs", "bool", True, "Bachelor's degree in Computer Science is required"),
        ],
        "desired": []  # No desired skills listed for this position
    },
    {
        "name": "Python Engineer",
        "required": [
            ("python_years", "min", 3, "At least 3 years of Python development experience is required"),
            ("data_years", "min", 1, "At least 1 year of data development experience is required"),
            ("has_bachelors_cs", "bool", True, "Bachelor's degree in Computer Science is required"),
        ],
        "desired": [
            ("agile_years", "min", 1, "Experience in Agile projects is desired"),
            ("has_git", "bool", True, "Git version control experience is desired"),
            ("data_coursework", "bool", True, "Data-related coursework is desired"),
        ]
    },
    {
        "name": "Project Manager",
        "required": [
            ("project_mgmt_years", "min", 3, "At least 3 years of software project management experience is required"),
            ("agile_years", "min", 2, "At least 2 years of experience in Agile projects is required"),
        ],
        "desired": [
            ("has_pmi_lean", "bool", True, "PMI Lean Project Management Certification is desired"),
            ("has_pmp", "bool", True, "PMP certification is desired"),
            ("has_csm", "bool", True, "Certified Scrum Master certification is desired"),
        ]
    },
    {
        "name": "Senior Knowledge Engineer",
        "required": [
            ("python_years", "min", 4, "At least 4 years of Python development experience is required"),
            ("expert_systems_years", "min", 2, "At least 2 years of Expert Systems development experience is required"),
            ("data_architecture_years", "min", 2, "At least 2 years of data architecture experience is required"),
            ("has_masters_cs", "bool", True, "Master's degree in Computer Science is required"),
        ],
        "desired": [
            ("expert_systems_coursework", "bool", True, "Expert Systems or AI coursework is desired"),
            ("data_coursework", "bool", True, "Advanced data architecture coursework is desired"),
        ]
    },
]