
from src.retrieval import retrieve
from src.generator import generate_answer

question = "How can mindfulness help manage stress?"

results = retrieve(question, top_k=3)

context = "\n\n".join(
    result["text"] for result in results
)

print("Retrieved document context:")
print(context)

print("\nGenerated answer:")
answer = generate_answer(question, context)
print(answer)
