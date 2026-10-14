import streamlit as st
from pathlib import Path
from review_engine import analyze_python, parse_code_upload, summarize_findings
from rag_pipeline import index_guidelines, retrieve_guidelines, generate_explanation
from report_generator import build_markdown_report

st.set_page_config(page_title="Secure Code Review Assistant", page_icon="🛡️", layout="wide")
st.title("🛡️ Secure Code Debugging and Review Assistant")
st.caption("Academic prototype • Static analysis + guideline retrieval + optional LLM explanations")
st.warning("Use synthetic/demo code only. Do not upload proprietary source code or secrets. Findings require human review.")

with st.sidebar:
    st.header("Configuration")
    st.write("Supported first version: Python source files (.py).")
    st.write("Static analysis uses Ruff and Bandit when installed.")
    st.write("RAG uses local guideline files in `Input_Data/guidelines/`.")
    st.write("LLM explanations are optional and require a configured provider.")
    if st.button("Index guideline knowledge base"):
        with st.spinner("Indexing local guideline files..."):
            result = index_guidelines()
        st.success(result)

uploaded = st.file_uploader("Upload a Python source file", type=["py", "txt"])
pasted = st.text_area("Or paste code here", height=220, placeholder="def example():\\n    ...")
filename = uploaded.name if uploaded else "pasted_code.py"
code = uploaded.getvalue().decode("utf-8", errors="replace") if uploaded else pasted

if st.button("Review code", type="primary", disabled=not bool(code.strip())):
    st.session_state["review_code"] = code
    st.session_state["review_filename"] = filename
    with st.spinner("Running static analysis..."):
        st.session_state["analysis"] = analyze_python(code, filename)
    with st.spinner("Retrieving relevant coding guidance..."):
        analysis = st.session_state["analysis"]
        findings = analysis.get("findings", [])
        finding_context = "\n".join(
            f"{item.get('rule_id', '')}: {item.get('issue', '')}. "
            f"Recommendation: {item.get('recommendation', '')}"
            for item in findings
        )
        retrieval_query = (
            "Secure coding guidance for these findings:\n"
            + finding_context
            + "\nRelevant source code:\n"
            + code[:2000]
        )
        st.session_state["guidance"] = retrieve_guidelines(
            retrieval_query, n_results=3, min_score=0.20
        )
    with st.spinner("Preparing explanation..."):
        st.session_state["explanation"] = generate_explanation(
            code, st.session_state["analysis"], st.session_state["guidance"]
        )

if "analysis" in st.session_state:
    analysis = st.session_state["analysis"]
    findings = analysis["findings"]
    guidance = st.session_state.get("guidance", [])
    explanation = st.session_state.get("explanation", "")
    c1, c2, c3 = st.columns(3)
    c1.metric("Findings", len(findings))
    c2.metric("Analyzers executed", len(analysis["tools_executed"]))
    c3.metric("Guideline passages retrieved", len(guidance))

    st.subheader("Source code")
    st.code(st.session_state["review_code"], language="python")

    st.subheader("Static-analysis findings")
    if findings:
        st.dataframe(findings, use_container_width=True, hide_index=True)
    else:
        st.info("No findings were returned by the configured analyzers. This does not prove the code is defect-free.")

    st.subheader("Guideline evidence")
    if guidance:
        for i, item in enumerate(guidance, 1):
            with st.expander(f"[{i}] {item['source']} — relevance {item['score']:.2f}"):
                st.write(item["text"])
    else:
        st.info("No guideline passages retrieved. Add .txt or .md files to data/guidelines and index them.")

    st.subheader("AI-assisted explanation")
    st.markdown(explanation)

    report = build_markdown_report(
        st.session_state["review_filename"], st.session_state["review_code"],
        analysis, guidance, explanation
    )
    st.download_button("Download review report (.md)", report,
                       file_name="code_review_report.md", mime="text/markdown")

    st.subheader("Evaluation / interpretation")
    st.write(summarize_findings(findings))
    st.caption("AI-generated explanations are advisory. Validate suggested changes with tests, static analysis, and human review.")
