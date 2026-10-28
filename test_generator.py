
from src.generator import generate_answer

question = "What is mindfulness?"
context = """
Mindfulness involves paying attention to the present moment
without judgment. It can be practised by observing thoughts,
feelings, and sensations.
"""

print("Testing deployed model with context...")
answer = generate_answer(question, context)
print("\nAnswer:")
print(answer)
