
from src.retrieval import retrieve
from src.generator import generate_answer

question = "How can mindfulness help manage stress?"

# Without RAG: no document context
print("=" * 50)
print("WITHOUT RAG")
print("=" * 50)
answer_without_rag = generate_answer(question)
print(answer_without_rag)

# With RAG: retrieve context from documents

results = retrieve(question, top_k=3)

print("\n" + "=" * 50)
print("WITH RAG")
print("=" * 50)

if not results:
    answer_with_rag = (
        "I could not find enough information in the provided sources."
    )
else:
    context = "\n\n".join(
        result["text"] for result in results
    )
    answer_with_rag = generate_answer(question, context)

print(answer_with_rag)

print("\n" + "=" * 50)
print("RETRIEVED SOURCES")
print("=" * 50)

if not results:
    print("No relevant sources found.")
else:
    for result in results:
        print(
            f"{result['source']} "
            f"(score: {result['score']})"
        )

