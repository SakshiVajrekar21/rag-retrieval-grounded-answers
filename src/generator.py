
import os
import requests


def generate_answer(question, context=None):
    endpoint = os.getenv("MODEL_ENDPOINT")

    if not endpoint:
        raise ValueError("Please set the MODEL_ENDPOINT environment variable.")

    if context:
        prompt = f"""
Answer the question using only the context provided.
If the answer is not in the context, say:
"I could not find enough information in the provided sources."

Context:
{context}

Question: {question}
"""
    else:
        prompt = f"""
Answer the question using your general knowledge.

Question: {question}
"""

    response = requests.post(
        endpoint,
        json={"question": prompt},
        timeout=120
    )

    response.raise_for_status()
    return response.json()["answer"]
