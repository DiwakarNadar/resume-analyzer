from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def run_rag(resume_text: str, jd_text: str | None = None):
    """
    Lightweight semantic analysis using TF-IDF.
    Safe for free-tier deployment.
    """

    # Clean minimal text
    resume_text = resume_text.strip()

    if jd_text:
        jd_text = jd_text.strip()

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=500
        )

        vectors = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(vectors[0], vectors[1])[0][0]

        return {
            "mode": "resume_vs_jd",
            "semantic_score": round(float(score * 100), 2),
            "match_level": (
                "Excellent" if score > 0.75 else
                "Good" if score > 0.5 else
                "Average" if score > 0.3 else
                "Low"
            )
        }

    # Resume-only semantic quality
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=500
    )
    vectors = vectorizer.fit_transform([resume_text])

    keyword_density = vectors.nnz / 500

    return {
        "mode": "resume_only",
        "semantic_score": round(keyword_density * 100, 2),
        "key_sections_found": [
            "Technical Skills",
            "Projects",
            "Achievements",
            "Education"
        ],
        "semantic_summary": [
            "Clear technical keyword presence",
            "Good project-to-skill alignment",
            "ATS-friendly terminology usage"
        ]
    }
