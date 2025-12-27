# resume/utils/skill_extractor.py

SKILL_ALIASES = {
    "python": ["python"],
    "django": ["django", "django rest framework", "drf"],
    "sql": ["sql", "mysql", "postgres", "postgresql"],
    "javascript": ["javascript", "js"],
    "react": ["react", "react.js"],
    "node": ["node", "node.js"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "git": ["git", "github"],
    "rest api": ["rest api", "restful api", "rest"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
}


def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found = set()

    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in text:
                found.add(canonical)
                break

    return sorted(found)
