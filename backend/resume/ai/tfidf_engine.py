from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_match(resume_text: str, jd_text: str | None):
    texts = [resume_text]

    if jd_text:
        texts.append(jd_text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=500
    )

    vectors = vectorizer.fit_transform(texts)

    if jd_text:
        score = cosine_similarity(vectors[0], vectors[1])[0][0]
        return {
            "mode": "resume_vs_jd",
            "semantic_score": round(float(score * 100), 2)
        }

    return {
        "mode": "resume_only",
        "semantic_score": round(float(vectors[0].nnz / 500 * 100), 2)
    }
