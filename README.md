
## Enterprise RAG & LLM Reliability Engineering Platform

The Relay is an enterprise-oriented Retrieval-Augmented Generation (RAG) and LLM reliability engineering platform designed to improve the accuracy, performance, scalability, and resilience of document-grounded AI applications.

Traditional RAG systems primarily focus on retrieving relevant document chunks and generating responses using large language models. However, operating reliable AI applications in real-world environments introduces additional engineering challenges:

- **Retrieval quality:** Relevant information may be incomplete, irrelevant, or missing from retrieved context.
- **LLM provider limitations:** API providers enforce request, token, concurrency, and daily usage limits.
- **Traffic management:** Sudden workload spikes can increase response latency and cause request failures.
- **Retry amplification:** Uncontrolled retries can increase traffic and worsen service instability.
- **Data freshness:** Document updates can leave previously generated embeddings outdated.
- **Answer reliability:** Unsupported responses and inaccurate citations can undermine trust.
- **Performance visibility:** Without systematic evaluation, retrieval quality and system reliability are difficult to measure.

The Relay extends a document-based RAG application with an engineering framework for retrieval optimization, grounded generation, LLM provider reliability, controlled load testing, and performance benchmarking.

It brings together document intelligence, semantic and hybrid retrieval, LLM orchestration, quota-aware request management, evaluation, and observability within a unified architecture.

**Core Objective:** Build a measurable and resilient RAG system that retrieves relevant evidence, generates grounded responses, manages provider constraints, and demonstrates its performance under different workload conditions.

---

## Architecture

### 1. Document Ingestion Pipeline

Documents are transformed into searchable knowledge through an ingestion pipeline.

```text
Document Upload
      |
Document Loading and Extraction
      |
Text Cleaning and Preprocessing
      |
Recursive Character Chunking
      |
Embedding Generation
      |
Vector Storage (ChromaDB)
      |
Document Metadata and Indexing
```

### 2. RAG Retrieval and Generation Pipeline

```text
User Question
      |
Query Embedding
      |
Semantic Similarity Search
      |
Top-K Document Chunks
      |
Context Construction
      |
Grounded Prompt + Source Metadata
      |
Google Gemini API
      |
Answer Generation
      |
Citation Validation
      |
Answer + Source Citations
```

### 3. LLM Reliability Engineering Pipeline

The extended architecture introduces a reliability layer between application requests and the LLM provider.

```text
Incoming Request
       |
Request Validation
       |
Rate and Token Limiting
       |
Concurrency Management
       |
Bounded Request Queue
       |
LLM Provider / Stand-in Provider
       |
Error Classification
       |
Retry and Backoff Management
       |
Response and Structured Logging
       |
Performance Metrics
```

The reliability pipeline is the target extension of the existing RAG application. Its individual components should be identified as implemented only after integration and testing.

---

## Retrieval Pipeline

The retrieval and generation workflow consists of the following stages:

1. **Query Submission:** The user submits a question through the document chat interface.
2. **Query Embedding:** The question is converted into a vector representation using `sentence-transformers/all-MiniLM-L6-v2`.
3. **Semantic Retrieval:** ChromaDB performs similarity search using cosine distance to retrieve relevant document chunks.
4. **Hybrid Retrieval:** An optional retrieval enhancement combines semantic similarity with keyword-based matching to improve candidate relevance.
5. **Context Construction:** Retrieved chunks are assembled with their associated source metadata.
6. **Grounded Prompt Generation:** LangChain's `ChatPromptTemplate` constructs a context-aware prompt and instructs Gemini to answer using the supplied evidence.
7. **Answer Generation:** Google Gemini generates the response based on the retrieved context.
8. **Citation Association:** Source information, including document name, page number, and chunk ID, is associated with the response.
9. **Conversation Update:** The answer and relevant source information are returned to the user while updating conversation history.

---

## Embeddings & ChromaDB

The application uses Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` model to generate semantic embeddings.

**Embedding configuration:**

| Property | Configuration |
|---|---|
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Embedding Dimensions | 384 |
| Vector Database | ChromaDB |
| Similarity Metric | Cosine similarity |
| Vector Normalization | L2 normalization |
| Storage | Persistent local ChromaDB collection |
| Database Location | `database/chroma_db/` |

All embeddings are normalized before storage to support consistent cosine similarity calculations.

Document chunks and associated metadata are stored in ChromaDB, including:

- Document ID
- Document name
- Page number
- Chunk ID
- Chunk index

This metadata enables source tracking and citation association during retrieval and response generation.

---

## LangChain & Gemini Integration

The application uses LangChain to coordinate document processing, retrieval, prompt construction, and LLM interaction.

- **Document Loading:** LangChain's `PyPDFLoader`, `TextLoader`, and supported document loaders extract text from uploaded files.
- **Text Splitting:** `RecursiveCharacterTextSplitter` divides documents into manageable chunks while preserving contextual continuity.
- **Embeddings:** Sentence Transformers generates vector representations for document chunks and user queries.
- **Vector Storage:** ChromaDB stores embeddings, document chunks, and metadata.
- **LLM Integration:** Google Gemini is integrated through `langchain-google-genai` using `ChatGoogleGenerativeAI`.
- **Prompt Engineering:** `ChatPromptTemplate` constructs grounded prompts to constrain responses to the supplied context.
- **Conversation Management:** Conversation history maintains context across user interactions.

The generation pipeline is designed to reduce unsupported responses by explicitly instructing the model to rely on retrieved evidence.

---

## LLM Reliability Engineering

Beyond conventional RAG functionality, The Relay is designed to investigate the operational reliability of LLM-powered applications.

### Reliability Components

| Component | Engineering Responsibility |
|---|---|
| Rate Limiter | Controls application-level request throughput |
| Token Limiter | Tracks and manages token consumption |
| Concurrency Controller | Limits simultaneous provider requests |
| Bounded Queue | Controls pending workload |
| Backpressure | Handles excess incoming requests |
| Retry Manager | Implements bounded retries for transient failures |
| Exponential Backoff | Reduces repeated request pressure |
| Circuit Breaker | Prevents repeated calls to an unhealthy provider |
| Request Logger | Records latency, retries, token usage, and status |

### Failure Handling Strategy

- Respect provider-supplied `Retry-After` information.
- Apply exponential backoff with jitter.
- Set a maximum retry count.
- Avoid retrying permanent authentication and validation errors.
- Stop retries when a daily quota or budget is exhausted.
- Record the final outcome of each logical request.

Application-level limits are designed to control outgoing traffic; they do not override provider-enforced quotas.

### Stand-in Provider

A configurable stand-in provider can be used to simulate:

- Rate-limit responses.
- Token consumption limits.
- Request latency.
- Concurrency restrictions.
- Temporary service failures.
- Daily quota exhaustion.

This enables repeatable reliability experiments without deliberately exhausting real provider quotas.

Real and simulated benchmark measurements must remain clearly separated.

---

## Retrieval Evaluation & Benchmarking

The Relay introduces a structured evaluation framework to measure retrieval quality, answer reliability, and system performance.

### Retrieval Configurations

Initial experimental configurations:

| Configuration | Chunk Size | Top-K | Reranking |
|---|---:|---:|---|
| Baseline | 500 | 3 | No |
| Balanced | 800 | 5 | Yes |
| Advanced | 1200 | 8 | Yes |

These values are starting points for experimentation rather than proven optimal configurations.

### Evaluation Metrics

**Retrieval and answer quality**
- Correct and cited answer percentage.
- Incorrect answer percentage.
- Correct refusal percentage.
- Incorrect refusal percentage.
- Citation accuracy.
- Retrieval relevance.

**Performance and reliability**
- First-token latency: p50, p95, p99.
- Total response latency: p50, p95, p99.
- Requests per minute.
- Success rate.
- Rate-limited request percentage.
- Timeout percentage.
- Average retries per request.
- Peak queue length.
- Tokens per answer.
- Estimated cost per 1,000 answers.

### Required Benchmark Scenarios

| Scenario | Purpose |
|---|---|
| Steady Load | Establish baseline system performance |
| Burst Load | Evaluate sudden increases in request volume |
| Sustained Overload | Measure behavior under sustained excess demand |
| Reduced RPM | Evaluate application behavior with a reduced request limit |
| Daily Budget Exhaustion | Validate quota-exhaustion handling using simulation |

### Benchmark Data

Raw measurements are recorded in `results.csv`, with one row per logical request.

```csv
request_id,scenario,source,start_time,first_token_ms,total_ms,status,retries,tokens_in,tokens_out,retrieval_setting,answer_grade
```

Allowed values:

- `source`: `real` or `stand-in`
- `status`: `ok`, `rate_limited`, `timeout`, `error`
- `answer_grade`: `correct`, `wrong`, `refused_correctly`, `refused_wrongly`

The benchmark data supports reproducible latency, reliability, token usage, and retrieval-quality analysis.

---

## Setup

### Prerequisites

- Python 3.11 or compatible version
- Git
- Google Gemini API key
- Internet connectivity

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd THE-RELAY
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your Google Gemini API key.

```env
GOOGLE_API_KEY=your_actual_gemini_api_key
SECRET_KEY=your_random_secret_key
```

**Security:** Never commit your `.env` file or expose API credentials in source code.

### 5. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://localhost:5000
```

### 6. Run Tests

```bash
pytest tests/ -v
```

---

## Features

### Core RAG Features

- Multi-file document upload (PDF, TXT, Markdown, DOCX).
- Automatic text extraction and preprocessing.
- Configurable document chunking.
- Sentence Transformer embeddings.
- Persistent ChromaDB vector storage.
- Semantic Top-K document retrieval.
- Source citations (document, page, chunk).
- Context-aware grounded answer generation.
- Conversation history and memory.
- Responsive document chat interface.
- Document management (upload, delete, refresh embeddings).

### Additional Application Features

- DOCX document support.
- Automatic document summaries.
- Suggested follow-up questions.
- Metadata-based document filtering.
- Hybrid semantic and keyword search.
- Dark mode.
- JSON chat export.
- Token usage and cost estimation dashboard.
- Session-based user authentication.

### Advanced Reliability and Evaluation Roadmap

- Configurable retrieval experiments.
- Dense and BM25 hybrid retrieval.
- Reciprocal Rank Fusion.
- Optional Cross-Encoder reranking.
- Retrieval and answer-quality evaluation.
- Citation validation.
- LLM provider abstraction.
- Request and token rate limiting.
- Concurrency management.
- Bounded queues and backpressure.
- Exponential backoff and controlled retries.
- Circuit-breaker behavior.
- Stand-in provider for simulated failures.
- Controlled load testing.
- CSV-based benchmark reporting.
- Latency and reliability analysis.
- Document versioning and freshness validation.

Advanced capabilities should be marked as implemented only after they have been integrated and validated in the repository.

---

## User Authentication

The application includes a lightweight session-based authentication system.

- Passwords are hashed using Werkzeug.
- Demo accounts are created automatically.
- New users can register through the web interface.
- Protected routes require authentication.
- Chat history is maintained separately for each logged-in user.
- The navigation bar displays the current user's information and provides a logout option.

This authentication system is intended for demonstration purposes. It can be extended with production-ready database-backed identity management, stronger authorization, and multi-tenant access controls.

---

## Project Engineering Principles

The Relay follows a set of engineering principles for building reliable LLM-powered applications:

1. **Evidence over assumptions:** Responses should be grounded in retrieved source material.
2. **Measurable retrieval:** Retrieval configurations should be evaluated against a consistent question set.
3. **Controlled resource usage:** Requests, tokens, and concurrency should be managed explicitly.
4. **Bounded failure handling:** Retries and queues should have well-defined limits.
5. **Data freshness:** Updated documents should be reindexed and validated safely.
6. **Reproducible experiments:** Benchmark results should be traceable to raw request-level data.
7. **Responsible provider usage:** Real API tests should respect account quotas and provider policies.
8. **Observability:** Latency, failures, token usage, and answer quality should be measurable.

---

## Future Enhancements

- Multi-provider LLM routing and fallback.
- Cost-aware model selection.
- Adaptive retrieval configuration.
- Semantic response caching with document-version invalidation.
- Advanced citation and faithfulness verification.
- Multi-tenant document isolation.
- Distributed request scheduling.
- Redis-backed rate limiting.
- OpenTelemetry integration.
- Langfuse-based observability.
- Automated document freshness monitoring.
- Kubernetes-based deployment and scaling.

---

