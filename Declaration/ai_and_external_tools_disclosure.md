# AI and External Tools Disclosure

**Project:** Secure Code Debugging and Review Assistant

## Tools and components
- Python and Streamlit for the application.
- Bandit and Ruff for static analysis.
- Python AST parsing for syntax validation.
- ChromaDB for vector storage and retrieval.
- `sentence-transformers/all-MiniLM-L6-v2` as the intended embedding model; verify against the final configuration.
- An optional OpenAI-based explanation feature is documented, but it was **not configured during the demonstrated tests**.

## AI assistance
AI assistance was used during development for guidance, troubleshooting, documentation drafting, and explanation of implementation steps. Edit this disclosure to accurately describe the assistance actually used and meet institute-specific requirements.

## Evaluation statement
The demonstrated tests used synthetic Python examples. Observed results include vulnerable-code findings, a clean-code example with no findings, syntax-error detection, safer subprocess analysis, and input-validation testing. These results do not prove that all vulnerabilities will be detected or that code with zero findings is secure.

## External dependencies and privacy
If the optional OpenAI feature is enabled, source code or related prompts may be sent to the configured external provider. Do not submit real secrets, credentials, or confidential source code to an external service without authorization. Store API keys in environment variables or an approved secrets manager; never commit them to the repository.

**Student Name:** Janvee Ghadge  
**PRN:** 123B1D060

