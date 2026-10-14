import ast
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

def parse_code_upload(filename: str, raw: bytes) -> str:
    return raw.decode("utf-8", errors="replace")


def _run_tool(command, source_path):
    try:
        tool_name = command[0]

        if tool_name in ("ruff", "bandit"):
            command = [
                sys.executable,
                "-m",
                tool_name,
                *command[1:]
            ]

        proc = subprocess.run(
            command + [str(source_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "tool": tool_name,
            "status": "executed",
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode
        }

    except Exception as exc:
        return {
            "tool": command[0],
            "status": "error",
            "error": str(exc)
        }


def analyze_python(code: str, filename: str = "uploaded.py") -> dict:
    findings = []
    tools_executed = []
    try:
        ast.parse(code)
    except SyntaxError as exc:
        findings.append({
            "tool": "Python parser", "rule_id": "SYNTAX", "severity": "High",
            "line": exc.lineno or 1, "issue": f"Syntax error: {exc.msg}",
            "evidence": (exc.text or "").strip(), "recommendation": "Correct the syntax before running analysis."
        })
        return {"findings": findings, "tools_executed": ["Python parser"], "raw": []}

    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / Path(filename).name
        if path.suffix.lower() != ".py":
            path = path.with_suffix(".py")
        path.write_text(code, encoding="utf-8")

        ruff = _run_tool(["ruff", "check", "--output-format", "json"], path)
        if ruff["status"] == "executed":
            tools_executed.append("Ruff")
            try:
                for item in json.loads(ruff.get("stdout", "[]") or "[]"):
                    findings.append({
                        "tool": "Ruff", "rule_id": item.get("code", "RUFF"),
                        "severity": "Low" if str(item.get("code", "")).startswith(("E", "F")) else "Medium",
                        "line": (item.get("location") or {}).get("row", 1),
                        "issue": item.get("message", "Code quality finding"),
                        "evidence": item.get("fix", {}).get("message") or "",
                        "recommendation": "Review the reported rule and apply a suitable fix."
                    })
            except Exception:
                pass

        bandit = _run_tool(["bandit", "-f", "json", "-q"], path)
        if bandit["status"] == "executed":
            tools_executed.append("Bandit")
            try:
                payload = json.loads(bandit.get("stdout", "{}") or "{}")
                for item in payload.get("results", []):
                    findings.append({
                        "tool": "Bandit", "rule_id": item.get("test_id", "BANDIT"),
                        "severity": item.get("issue_severity", "MEDIUM").title(),
                        "line": item.get("line_number", 1),
                        "issue": item.get("issue_text", "Potential security issue"),
                        "evidence": item.get("code", ""),
                        "recommendation": "Inspect the evidence and follow the tool's remediation guidance."
                    })
            except Exception:
                pass

    # De-duplicate findings with a stable key.
    unique = {}
    for f in findings:
        key = (f["tool"], f["rule_id"], f["line"], f["issue"])
        unique[key] = f
    return {"findings": list(unique.values()), "tools_executed": tools_executed, "raw": []}

def summarize_findings(findings):
    if not findings:
        return "No configured analyzer findings were returned. This is not proof that the code is secure or bug-free."
    by_severity = {}
    for item in findings:
        by_severity[item["severity"]] = by_severity.get(item["severity"], 0) + 1
    return "Findings by reported severity: " + ", ".join(f"{k}: {v}" for k, v in sorted(by_severity.items()))
