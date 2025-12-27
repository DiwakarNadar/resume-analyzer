# resume/utils/resume_quality.py

from .skill_extractor import extract_skills

ACTION_VERBS = [
    "developed", "designed", "implemented", "built",
    "created", "optimized", "improved", "managed",
    "led", "analyzed"
]

SECTIONS = {
    "experience": ["experience", "work experience", "professional experience"],
    "projects": ["projects", "personal projects"],
    "education": ["education", "academic"],
    "skills": ["skills", "technical skills"],
    "summary": ["summary", "profile", "objective"],
}


def calculate_resume_ats(resume_text: str) -> dict:
    text = resume_text.lower()

    # 1️⃣ Skills (40)
    skills = extract_skills(text)
    skill_score = min(len(skills) * 4, 40)

    # 2️⃣ Sections (30)
    section_matches = 0
    for _, keywords in SECTIONS.items():
        if any(keyword in text for keyword in keywords):
            section_matches += 1
    section_score = (section_matches / len(SECTIONS)) * 30

    # 3️⃣ Action verbs (20)
    verb_count = sum(text.count(v) for v in ACTION_VERBS)
    verb_score = min(verb_count * 2, 20)

    # 4️⃣ Length (10)
    word_count = len(text.split())
    if 300 <= word_count <= 800:
        length_score = 10
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        length_score = 5
    else:
        length_score = 0

    ats_score = round(skill_score + section_score + verb_score + length_score)

    suggestions = []
    if skill_score < 30:
        suggestions.append("Add more relevant technical skills.")
    if section_score < 25:
        suggestions.append("Ensure clear sections like Experience, Projects, and Skills.")
    if verb_score < 15:
        suggestions.append("Use more action verbs to describe your impact.")
    if length_score < 10:
        suggestions.append("Optimize resume length (300–800 words is ideal).")

    return {
        "ats_score": ats_score,
        "skills": skills,
        "mode": "resume_only",
        "suggestions": suggestions,
    }
