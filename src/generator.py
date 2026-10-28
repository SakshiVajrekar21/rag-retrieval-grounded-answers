
import os
import requests


def generate_answer(question, context=None):
    endpoint = os.getenv("MODEL_ENDPOINT")

    if not endpoint:
        raise ValueError(
            "Please set the MODEL_ENDPOINT environment variable."
        )

    if context:
        prompt = f"""
Answer the question using only information explicitly stated
in the context below.

Rules:
1. Do not invent statistics, percentages, or facts.
2. A study's sample size is not the number of people who
   experienced an outcome.
3. If the context does not explicitly answer the question, reply:
   "I could not find enough information in the provided sources."
4. Keep the answer brief.

Context:
{context}

Question: {question}

Answer:
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
