from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def similarity_search(resume_chunks, jd_chunks, top_k=5):
    resume_vectors = np.array([c["embedding"] for c in resume_chunks])
    jd_vectors = np.array([c["embedding"] for c in jd_chunks])

    scores = cosine_similarity(resume_vectors, jd_vectors)

    results = []
    for i, row in enumerate(scores):
        results.append({
            "resume_text": resume_chunks[i]["text"][:200],
            "score": round(float(row.max()), 3),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
