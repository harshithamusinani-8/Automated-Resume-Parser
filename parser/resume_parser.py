import re

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "fastapi",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git"
]


def extract_email(text):

    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    result = re.findall(pattern, text)

    return result[0] if result else None


def extract_phone(text):

    pattern = r'\+?\d[\d\s-]{8,}\d'

    result = re.findall(pattern, text)

    return result[0] if result else None


def extract_skills(text):

    text_lower = text.lower()

    found = []

    for skill in SKILLS:

        if skill in text_lower:
            found.append(skill)

    return found