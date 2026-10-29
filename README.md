# RAG-Based Grounded Answer Generation

A Retrieval-Augmented Generation (RAG) project that combines document retrieval with an open-weight language model to generate answers grounded in supplied text sources. The generation API is deployed on Google Cloud Run.

## 1. Project Overview

Large language models can generate fluent answers but may also produce unsupported information when the required evidence is unavailable.

This project implements a RAG pipeline that retrieves relevant passages from a small collection of text documents and supplies them to a language model before generating an answer.

The project also compares responses generated with and without retrieval to observe how the retrieved context affects the output.

## 2. Objectives

- Build a document-based question-answering pipeline.
- Retrieve relevant text using TF-IDF and cosine similarity.
- Select the three most relevant text chunks for a question.
- Use an open-weight language model for answer generation.
- Deploy the generation API on Google Cloud Run.
- Compare answers with and without retrieved context.

## 3. System Architecture

The project follows this workflow:

1. **Document collection:** Load the available text files.
2. **Text chunking:** Split documents into chunks of 800 characters with 150 characters of overlap.
3. **Retrieval:** Use TF-IDF and cosine similarity to rank text chunks against the user's question.
4. **Context selection:** Select the top three chunks.
5. **Prompt construction:** Combine the question, retrieved passages, and instructions for evidence-based answering.
6. **Answer generation:** Send the prompt to the Qwen model through the generation API.
7. **Response:** Return the generated answer, with source filenames available in the comparison output.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| TF-IDF | Text representation and retrieval |
| Cosine similarity | Ranking relevant text chunks |
| Qwen2.5-0.5B-Instruct | Open-weight language model |
| GGUF Q4_K_M | Quantized model format |
| llama.cpp / llama-cpp-python | Local model inference runtime |
| FastAPI | API development |
| Docker | Application containerization |
| Google Artifact Registry | Container image storage |
| Google Cloud Build | Container image building |
| Google Cloud Run | Cloud deployment |

## 5. Knowledge Base

The project uses six text documents focused on mindfulness and stress-related information.

- `01_newspaper_article.txt`
- `02_nhs_mindfulness.txt`
- `03_nccih_evidence.txt`
- `04_who_stress.txt`
- `05_mindfulness_guide.txt`
- `06_mindfulness_synthesis.txt`

The synthesis document is a user-created summary of existing source material.

## 6. Project Structure

The main project components include:

```text
rag-retrieval-grounded-answers/
├── data/
│   └── documents/
│       ├── 01_newspaper_article.txt
│       ├── 02_nhs_mindfulness.txt
│       ├── 03_nccih_evidence.txt
│       ├── 04_who_stress.txt
│       ├── 05_mindfulness_guide.txt
│       └── 06_mindfulness_synthesis.txt
├── src/
│   └── generator.py
├── compare_rag.py
├── requirements.txt
└── README.md
```

This is a simplified view of the main components. Other files used for the API, model runtime, and deployment may also be present in the repository.

## 7. Running the Project

### Prerequisites

- Python installed on your system.
- Git installed if you are cloning the repository.
- Access to the deployed generation API, or a separately configured local model service.
- The project dependencies listed in `requirements.txt`.

### Step 1: Clone the repository

```bash
git clone https://github.com/SakshiVajrekar21/rag-retrieval-grounded-answers.git
cd rag-retrieval-grounded-answers
```

### Step 2: Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure the generation endpoint

The generator uses the `MODEL_ENDPOINT` environment variable to identify the generation API.

PowerShell:

```powershell
$env:MODEL_ENDPOINT="https://rag-model-api-609571231184.asia-south1.run.app/generate"
```

Set this variable to the appropriate endpoint before running the client. The deployed API must be accessible for requests to succeed.

### Step 5: Run the comparison

```bash
python compare_rag.py
```

The comparison script evaluates a question using responses with and without retrieved context. Its output can be used to inspect the differences between the two approaches.

**Note:** The commands above assume the repository contains the referenced files and that the comparison script is configured to use the endpoint as described. Check the current application configuration if running the project on another computer.

## 8. Cloud Deployment

The generation API was deployed using Google Cloud services.

| Configuration | Value |
|---|---|
| Google Cloud project | `gcp-ml-model-monitoring` |
| Region | `asia-south1` |
| Cloud Run service | `rag-model-api` |
| Health endpoint | `/health` |
| Generation endpoint | `/generate` |

Deployment workflow:

1. Package the application and its dependencies using Docker.
2. Build the container image using Google Cloud Build.
3. Store the image in Google Artifact Registry.
4. Deploy the service to Google Cloud Run.
5. Test the health and generation endpoints.

The deployed service was tested successfully using the health endpoint and generation endpoint.

### Test the health endpoint

Open this URL in a browser:

https://rag-model-api-609571231184.asia-south1.run.app/health

The expected successful response is:

```json
{
  "status": "ok"
}
```

## 9. Evaluation and Results

The project uses a targeted test question to check whether the model provides a specific statistic without supporting evidence.

**Test question:**

> What exact percentage of students in my college experienced reduced stress after mindfulness?

### Without RAG

The model responded:

> Based on general knowledge, approximately 20% of students in a typical college experience reduced stress after mindfulness practices.

This response introduced a specific percentage that was not supported by the supplied documents.

### With RAG

The model responded:

> I could not find enough information in the provided sources.

The RAG response recognized that the available sources did not establish the requested college-specific percentage.

### Retrieved source filenames

- `03_nccih_evidence.txt`
- `04_who_stress.txt`
- `03_nccih_evidence.txt`

### Observation

For this test question, the RAG version avoided giving an unsupported exact statistic and instead indicated insufficient evidence.

This is an initial qualitative observation, not proof that RAG always prevents hallucinations or that every generated answer is correct.

## 10. Limitations

- The knowledge base contains a small number of text documents.
- TF-IDF retrieval may miss semantically relevant passages that use different wording.
- Evaluation is limited to a small number of test cases.
- The language model may still generate incorrect or unsupported information.
- Retrieved source filenames do not independently guarantee that every claim in an answer is supported.

## 11. Future Improvements

- Evaluate the system with a larger collection of questions.
- Compare TF-IDF with semantic embedding-based retrieval.
- Improve chunking and document preprocessing.
- Provide passage-level citations for generated claims.
- Measure response latency, resource usage, and deployment cost.
- Test retrieval quality and answer correctness using defined evaluation metrics.

## 12. Conclusion

This project demonstrates an end-to-end RAG workflow that combines document retrieval, an open-weight language model, a FastAPI generation service, Docker-based packaging, and Google Cloud Run deployment.

The initial comparison illustrates how supplying relevant context and instructing the model to acknowledge missing evidence can improve its response to a particular unsupported question.

The results also highlight the need for broader evaluation before making general claims about reliability.

## Author

**Sakshi Ravindra Vajrekar**  
MSc Artificial Intelligence — Part II  
GitHub: https://github.com/SakshiVajrekar21/rag-retrieval-grounded-answers

**Prachi Kishor Gaonkar**  
MSc Artificial Intelligence — Part II 