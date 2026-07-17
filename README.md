# RAG Application

A production-style Retrieval-Augmented Generation (RAG) application that allows users to upload documents (PDF, TXT, Markdown, and DOCX) and chat with their own knowledge base. The system retrieves relevant information from uploaded documents and generates grounded, cited responses using Google Gemini.

---

## Architecture

```
Upload → Load & Clean → Chunk → Embed → Store (ChromaDB)
                                              │
User Question → Embed Question → Similarity Search (cosine) → Top-K Chunks
                                              │
                          Build Grounded Prompt (context + citations)
                                              │
                                     Gemini API
                                              │
                          Answer + Citations (doc, page, chunk id)
```



## Retrieval Pipeline

1. The user submits a question through the chat interface.
2. The question is converted into an embedding using the `sentence-transformers/all-MiniLM-L6-v2` model.
3. ChromaDB performs a cosine similarity search to retrieve the most relevant document chunks.
4. Retrieved results are optionally re-ranked using a lightweight hybrid search approach based on semantic similarity and keyword overlap.
5. Citations are generated, including the document name, page number, and chunk ID.
6. A grounded prompt is constructed and sent to Google Gemini. The model is instructed to answer only using the provided context and to return *"I don't know based on the provided documents."* whenever the required information is unavailable.
7. The final response, along with citations, is returned to the user while updating the conversation memory.

## Embeddings & ChromaDB

The application uses Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` model to generate 384-dimensional embeddings. All vectors are normalized before storage to ensure consistent cosine similarity calculations. Embeddings, document chunks, and metadata (document ID, document name, page number, chunk ID, and chunk index) are stored in a local ChromaDB collection located in `database/chroma_db/`.

## LangChain & Gemini Integration

* LangChain's `PyPDFLoader`, `TextLoader`, and document loaders are used to extract text from supported file formats.
* Documents are split using `RecursiveCharacterTextSplitter`.
* Google Gemini is integrated through `langchain-google-genai` using `ChatGoogleGenerativeAI`.
* Prompt generation is managed with `ChatPromptTemplate` to enforce grounded responses, proper citations, and reduce hallucinations.

---

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create or edit the `.env` file and add your Google Gemini API key.

```env
GOOGLE_API_KEY=your_actual_gemini_api_key
SECRET_KEY=your_random_secret_key
```

### 3. Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://localhost:5000
```


### 4. Run Tests

```bash
pytest tests/ -v
```

---

## Features

### Core Features

* Multi-file upload (PDF, TXT, Markdown, DOCX)
* Automatic text extraction and preprocessing
* Intelligent document chunking
* Sentence Transformer embeddings
* ChromaDB vector storage
* Semantic Top-K document retrieval
* Source citations (document, page, chunk)
* Conversation memory
* Responsive chat interface
* Document management (upload, delete, refresh embeddings)

### Additional Features

* DOCX support
* Automatic document summaries
* Suggested follow-up questions
* Metadata-based document filtering
* Hybrid semantic + keyword search
* Dark mode
* Chat export in JSON format
* Token usage and cost estimation dashboard
* Session-based user authentication

## User Authentication

The application includes a lightweight session-based authentication system.

* Passwords are securely hashed using Werkzeug.
* Demo accounts are created automatically.
* New users can register through the web interface.
* Protected routes require authentication.
* Chat history is stored separately for each logged-in user.
* The navigation bar displays the current user's information and provides a logout option.

This authentication system is intended for demonstration purposes and can easily be replaced with a production-ready database or identity provider.

