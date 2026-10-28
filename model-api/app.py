
import os
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

app = FastAPI(title="RAG Assignment Model API")

MODEL_PATH = os.getenv("MODEL_PATH", "/app/model.gguf")
model = None


class QuestionRequest(BaseModel):
    question: str


@app.on_event("startup")
def load_model():
    global model

    if not Path(MODEL_PATH).exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    model = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=2,
        verbose=False
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(request: QuestionRequest):
    result = model.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer clearly and briefly. Use only the supplied "
                    "context when it is provided. If the context does "
                    "not contain the answer, say you could not find "
                    "enough information in the provided sources."
                )
            },
            {"role": "user", "content": request.question}
        ],
        max_tokens=250,
        temperature=0.2
    )

    answer = result["choices"][0]["message"]["content"]
    return {"answer": answer}
