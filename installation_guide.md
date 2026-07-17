# Installation Guide

This guide explains how to install, configure, and run the RAG Application on your local machine.

---

# System Requirements

Before installing the application, ensure your system meets the following requirements:

* Python 3.10 or later
* Git
* Internet connection (required to download AI models)
* Google Gemini API Key

---

# Step 1: Clone the Repository

Clone the project from GitHub.

```bash
git clone <repository-url>
cd <project-folder>
```

Or download the project as a ZIP file and extract it.

---

# Step 2: Create a Virtual Environment

Creating a virtual environment is recommended to isolate project dependencies.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal should display the virtual environment name.

---

# Step 3: Install Required Packages

Install all project dependencies using pip.

```bash
pip install -r requirements.txt
```

This installs Flask, LangChain, ChromaDB, Sentence Transformers, Google Gemini integration, and all other required libraries.

---

# Step 4: Configure Environment Variables

Create a file named `.env` in the project's root directory.

Add the following variables:

```env
GOOGLE_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

Replace:

* `your_gemini_api_key` with your Google Gemini API key.
* `your_secret_key` with any random secure string.

---

# Step 5: Run the Application

Start the Flask application by running:

```bash
python app.py
```

If the installation is successful, the application will start without errors.

Open your browser and navigate to:

```
http://localhost:5000
```

---

# Step 6: Login

The application includes demo accounts for testing.

| Username | Password | Role  |
| -------- | -------- | ----- |
| admin    | admin123 | Admin |
| demo     | demo123  | User  |

You may also create a new account using the registration page.

---

# Step 7: Upload Documents

After logging in:

1. Open the **Upload Documents** page.
2. Select one or more supported files.
3. Upload the documents.
4. Wait for processing to complete.

During processing, the application:

* Extracts document text
* Splits text into chunks
* Generates embeddings
* Stores embeddings in ChromaDB

---

# Step 8: Chat with Your Documents

Once processing is complete:

1. Open the **Chat** page.
2. Ask questions about the uploaded documents.
3. The application retrieves the most relevant document chunks.
4. Google Gemini generates a grounded response with citations.

---

# Running Tests

Run the project's test suite using:

```bash
pytest tests/ -v
```

---

# Supported File Formats

The application supports the following document types:

* PDF (.pdf)
* Microsoft Word (.docx)
* Text (.txt)
* Markdown (.md)

---

# Troubleshooting

### Missing Dependencies

If a package is missing, reinstall the dependencies:

```bash
pip install -r requirements.txt
```

### Invalid API Key

If Gemini requests fail, verify that your `GOOGLE_API_KEY` is correctly configured in the `.env` file.

### Model Download

The Sentence Transformer model is downloaded automatically during the first execution. Depending on your internet connection, this may take a few minutes.

### Port Already in Use

If port **5000** is occupied, stop the conflicting application or configure Flask to use a different port.

---

# Uninstall

To remove the application:

1. Delete the project folder.
2. Remove the virtual environment (`venv`).
3. Delete the local ChromaDB database if it is no longer needed.

No additional system configuration is required.
