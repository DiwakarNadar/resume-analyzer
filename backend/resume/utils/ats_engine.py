# resume/utils/ats_engine.py

from .skill_extractor import extract_skills


def calculate_jd_ats(resume_text: str, jd_text: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))

    if not jd_skills:
        return {
            "ats_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "mode": "resume_vs_jd",
            "suggestions": ["Job description contains no recognizable skills."]
        }

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    ats_score = round((len(matched) / len(jd_skills)) * 100)

    return {
        "ats_score": ats_score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "mode": "resume_vs_jd",
        "suggestions": (
            [f"Add these skills to improve match: {', '.join(sorted(missing))}"]
            if missing else
            ["Excellent match with the job description."]
        )
    }
