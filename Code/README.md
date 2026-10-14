# Code

## Files
- `app.py`: Streamlit interface and review workflow.
- `review_engine.py`: Bandit/Ruff static analysis and finding formatting.
- `rag_pipeline.py`: guideline indexing, retrieval, and optional OpenAI explanation.
- `report_generator.py`: Markdown report generation.
- `index_guidelines.py`: helper to rebuild the local guideline index.
- `requirements.txt`: Python dependencies.
- `.env.example`: example environment configuration only; do not put real keys in it.

## Run from the submission root

```powershell
python -m pip install -r Code/requirements.txt
python -m streamlit run Code/app.py
```

Then click **Index guideline knowledge base** in the sidebar before the first review or after updating the guideline files.

**Important:** This package is assembled from the starter archive and the changes documented in this conversation. Run it in a clean environment before submission and replace it with the exact local version if your local project has additional edits.
