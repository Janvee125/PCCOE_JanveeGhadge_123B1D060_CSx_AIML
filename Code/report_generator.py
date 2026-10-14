from datetime import datetime

def build_markdown_report(filename, code, analysis, guidance, explanation):
    lines = [
        "# Secure Code Review Report", "",
        f"- **File:** {filename}",
        f"- **Generated (UTC):** {datetime.utcnow().isoformat(timespec='seconds')}",
        f"- **Tools executed:** {', '.join(analysis.get('tools_executed', [])) or 'None'}",
        f"- **Finding count:** {len(analysis.get('findings', []))}", "",
        "## Findings", ""
    ]
    if not analysis.get("findings"):
        lines.append("No findings returned by configured analyzers. This is not proof of defect-free or secure code.")
    for f in analysis.get("findings", []):
        lines += [
            f"### {f['severity']} — {f['issue']}",
            f"- Tool/rule: {f['tool']} / {f['rule_id']}",
            f"- Line: {f['line']}",
            f"- Evidence: `{f.get('evidence', '')}`",
            f"- Recommendation: {f.get('recommendation', '')}", ""
        ]
    lines += ["## Retrieved guideline evidence", ""]
    if guidance:
        for i, g in enumerate(guidance, 1):
            lines += [f"### [{i}] {g['source']}", g["text"], ""]
    else:
        lines.append("No guideline passages retrieved.")
    lines += ["## AI-assisted explanation", "", explanation, "",
              "## Limitations", "",
              "This report is advisory. Analyzer coverage is incomplete; AI output may be wrong. "
              "Validate fixes with tests, static analysis, and qualified human review.", "",
              "## Reviewed code (submitted input)", "", "```python", code, "```", ""]
    return "\\n".join(lines)
