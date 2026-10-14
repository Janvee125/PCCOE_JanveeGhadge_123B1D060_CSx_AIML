# AI and External Dependency Disclosure

- Static analysis tools: Bandit and Ruff.
- Retrieval/vector store: ChromaDB.
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (verify actual model revision/version used before submission).
- Optional LLM integration: OpenAI API, documented in configuration; it was **not configured in the recorded local tests**. Do not claim LLM-generated explanations were demonstrated.
- The embedding model may require internet access on first download. Enabling the optional OpenAI integration requires a valid API key and may send submitted source code to the provider.
- No API key or `.env` file should be included in the submission ZIP.

Replace or supplement this disclosure with the official institute format if required.

