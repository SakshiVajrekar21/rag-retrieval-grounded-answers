
import os
import re
import requests

MODEL_ENDPOINT = os.getenv("MODEL_ENDPOINT")

REFUSAL = "I could not find enough information in the provided sources."


def generate_answer(question, context=None):
    if not MODEL_ENDPOINT:
        raise ValueError("Please set the MODEL_ENDPOINT environment variable.")

    if context:
        # Basic relevance check using meaningful words.
        question_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", question.lower())
        )
        context_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", context.lower())
        )

        meaningful_words = question_words - {
            "what", "when", "where", "who", "why", "how",
            "the", "and", "for", "was", "were", "are",
            "does", "did", "can", "could", "from"
        }

        overlap = meaningful_words & context_words

        if not meaningful_words or len(overlap) / len(meaningful_words) < 0.5:
            return REFUSAL

        prompt = f"""
Answer ONLY using facts explicitly supported by the context.
Do not use general knowledge or guess.
If the answer is not supported by the context, reply exactly:
{REFUSAL}

Context:
{context}

Question:
{question}

Answer:
"""
    else:
        prompt = f"Answer this question using general knowledge:\n{question}"

    response = requests.post(
        MODEL_ENDPOINT,
        json={"question": prompt},
        timeout=120
    )
    response.raise_for_status()

    data = response.json()
    answer = (
        data.get("answer")
        or data.get("response")
        or data.get("generated_text")
    )

    if not answer:
        raise ValueError(f"Unexpected response format: {data}")

    return answer.strip()
