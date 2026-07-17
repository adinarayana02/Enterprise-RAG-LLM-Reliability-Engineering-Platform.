"""
config.py
---------
Centralized application configuration.

Loads all secrets and tunables from the .env file so that no credentials
or environment-specific values are ever hard-coded in the source tree.
Every other module should import settings from here rather than calling
os.getenv() directly, so we have a single source of truth.
"""

import os
from dotenv import load_dotenv

# Load variables from .env into the process environment as early as possible.
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Application-wide configuration values."""

    # --- Flask ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH_MB", "25")) * 1024 * 1024

    # --- Gemini LLM ---
    HF_API_KEY = os.getenv("HF_API_KEY")

    HF_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"

    # --- Embeddings ---
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # --- Storage ---
    UPLOAD_FOLDER: str = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "documents/uploaded_files"))
    CHROMA_PERSIST_DIR: str = os.path.join(BASE_DIR, os.getenv("CHROMA_PERSIST_DIR", "database/chroma_db"))
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "enterprise_rag_docs")

    # --- RAG tuning ---
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    TOP_K: int = int(os.getenv("TOP_K", "4"))

    # --- Uploads ---
    ALLOWED_EXTENSIONS = {"pdf", "txt", "md", "markdown", "docx"}

    @staticmethod
    def ensure_directories() -> None:
        """Create required runtime directories if they don't already exist."""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.CHROMA_PERSIST_DIR, exist_ok=True)


def validate_config() -> list:
    """
    Validate critical configuration at startup.

    Returns a list of human-readable warning strings (empty if everything
    looks fine). We warn instead of raising so the dashboard can still load
    and show the user a clear "add your API key" message.
    """
    warnings = []
    if not Config.HF_API_KEY or Config.HF_API_KEY == "your_hf_api_key_here":
        warnings.append(
            "HF_API_KEY is not set. Add your Gemini API key to the .env file "
            "before sending chat messages."
        )
    return warnings
