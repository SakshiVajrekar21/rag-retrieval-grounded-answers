
import os
import requests


def generate_answer(question, context=None):
    endpoint = os.getenv("MODEL_ENDPOINT")

    if not endpoint:
        raise ValueError(
            "Set the MODEL_ENDPOINT environment variable first."
        )

    if context:
        prompt = f"""
Answer the question using only the context below.
If the context does not contain the answer, say:
"I could not find enough information in the provided sources."

Context:
{context}

Question: {question}
"""
    else:
        prompt = f"""
Answer this question using your general knowledge.

Question: {question}
"""

    response = requests.post(
        endpoint,
        json={"question": prompt},
        timeout=120
    )
    response.raise_for_status()

    data = response.json()
    return data["answer"]
