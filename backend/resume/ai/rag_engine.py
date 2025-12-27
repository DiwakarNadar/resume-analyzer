from resume.ai.embeddings import embed_text
from resume.ai.vector_store import similarity_search

def run_rag(resume_text: str, jd_text=None):
    resume_chunks = embed_text(resume_text)

    if jd_text:
        jd_chunks = embed_text(jd_text)
        matches = similarity_search(resume_chunks, jd_chunks)
        return {
            "mode": "resume_vs_jd",
            "top_matches": matches
        }

    return {
        "mode": "resume_only",
        "key_sections_found": [
            "Technical Skills",
            "Projects",
            "Achievements",
            "Education"
        ],
        "semantic_summary": [
            "Strong ML-focused project experience",
            "Backend and data skill alignment",
            "Good ATS keyword density"
        ]
    }
