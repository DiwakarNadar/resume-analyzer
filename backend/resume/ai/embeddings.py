from sentence_transformers import SentenceTransformer

# Load once (important for performance)
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    """
    Split text into chunks and generate embeddings.
    """
    chunks = [
        text[i:i + 500]
        for i in range(0, len(text), 500)
        if text[i:i + 500].strip()
    ]

    embeddings = _model.encode(chunks).tolist()

    return [
        {"text": chunk, "embedding": emb}
        for chunk, emb in zip(chunks, embeddings)
    ]
