
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCUMENTS_DIR = Path("data/documents")


def load_documents():
    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        if text:
            documents.append({
                "source": file_path.name,
                "text": text
            })

    return documents


def split_into_chunks(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def prepare_chunks():
    chunks = []

    for document in load_documents():
        for number, chunk in enumerate(
            split_into_chunks(document["text"]), start=1
        ):
            chunks.append({
                "source": document["source"],
                "chunk_id": number,
                "text": chunk
            })

    return chunks


def retrieve(query, top_k=3):
    chunks = prepare_chunks()

    if not chunks:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(
        [chunk["text"] for chunk in chunks]
    )

    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, document_vectors).flatten()

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        if scores[index] > 0:
            result = chunks[index].copy()
            result["score"] = round(float(scores[index]), 4)
            results.append(result)

    return results


if __name__ == "__main__":
    documents = load_documents()
    chunks = prepare_chunks()

    print(f"Documents loaded: {len(documents)}")
    print(f"Text chunks created: {len(chunks)}")

    question = "What is mindfulness?"
    print(f"\nQuestion: {question}")

    results = retrieve(question, top_k=5)

    for result in results:
        print(f"\nSource: {result['source']}")
        print(f"Chunk: {result['chunk_id']}")
        print(f"Relevance score: {result['score']}")
        print(f"Text:\n{result['text']}")
