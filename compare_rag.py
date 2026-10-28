
from src.retrieval import retrieve
from src.generator import generate_answer

question = "What exact percentage of students in my college experienced reduced stress after mindfulness?"

# Without RAG: no document context
print("=" * 50)
print("WITHOUT RAG")
print("=" * 50)
answer_without_rag = generate_answer(question)
print(answer_without_rag)

# With RAG: retrieve context from documents
results = retrieve(question, top_k=3)
context = "\n\n".join(result["text"] for result in results)

print("\n" + "=" * 50)
print("WITH RAG")
print("=" * 50)
answer_with_rag = generate_answer(question, context)
print(answer_with_rag)

print("\n" + "=" * 50)
print("RETRIEVED SOURCES")
print("=" * 50)
for result in results:
    print(result.get("source", "Source name unavailable"))
