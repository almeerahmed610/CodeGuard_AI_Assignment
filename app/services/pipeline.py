# from __future__ import annotations
# import os
# from typing import Any,TypedDict
# from langgraph.graph import END,StateGraph
# from langchain_google_genai import ChatGoogleGenerativeAI
# from agents.scanner import scanner_agent
# from agents.refactor import refactor_agent
# from agents.docs import docs_agent

# class AuditState(TypedDict,total=False):
#     source_code:str
#     audit_report:str
#     findings:list[dict[str,Any]]
#     refactored_code:str
#     documentation:str
#     model:str
#     temperature:float

# def build_graph(llm):
#     graph=StateGraph(AuditState)
#     graph.add_node("scanner",lambda s:scanner_agent(s,llm))
#     graph.add_node("refactor",lambda s:refactor_agent(s,llm))
#     graph.add_node("docs",lambda s:docs_agent(s,llm))
#     graph.set_entry_point("scanner")
#     graph.add_edge("scanner","refactor")
#     graph.add_edge("refactor","docs")
#     graph.add_edge("docs",END)
#     return graph.compile()

# def run_pipeline(source_code:str,model:str,temperature:float):
#     key=os.getenv("GOOGLE_API_KEY")
#     if not key: raise RuntimeError("GOOGLE_API_KEY is missing. Add it to .env")
#     llm=ChatGoogleGenerativeAI(model=model,temperature=temperature,google_api_key=key)
#     return build_graph(llm).invoke({"source_code":source_code,"model":model,"temperature":temperature})

from __future__ import annotations

import json
import os
import re
from typing import Any, TypedDict

from dotenv import load_dotenv
from google import genai


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PIPELINE STATE
# ============================================================

class PipelineState(TypedDict, total=False):
    source_code: str
    model: str
    temperature: float

    findings: list[dict[str, Any]]
    refactored_code: str
    documentation: str

    scanner_output: str
    refactor_output: str
    docs_output: str


# ============================================================
# DEFAULT MODEL
# ============================================================

DEFAULT_MODEL = "gemini-3.6-flash"


# ============================================================
# API KEY
# ============================================================

def get_api_key() -> str:
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    if not api_key:
        raise RuntimeError(
            "Gemini API key not found. "
            "Please add GEMINI_API_KEY=your_api_key "
            "to your .env file."
        )

    return api_key.strip()


# ============================================================
# GEMINI CLIENT
# ============================================================

def create_client() -> genai.Client:
    return genai.Client(
        api_key=get_api_key()
    )


# ============================================================
# MODEL NORMALIZER
# ============================================================

def normalize_model(model: str | None) -> str:

    if isinstance(model, str) and model.strip():
        selected_model = model.strip()
    else:
        selected_model = DEFAULT_MODEL

    selected_model = selected_model.replace(
        "models/",
        ""
    )

    # Redirect old model to current default.
    if selected_model == "gemini-2.5-flash":
        selected_model = DEFAULT_MODEL

    return selected_model


# ============================================================
# TEMPERATURE NORMALIZER
# ============================================================

def normalize_temperature(
    temperature: float | int | None,
) -> float:

    try:
        value = float(temperature)
    except (TypeError, ValueError):
        value = 0.2

    return max(
        0.0,
        min(1.0, value)
    )


# ============================================================
# GEMINI CALL
# ============================================================

def call_gemini(
    *,
    client: genai.Client,
    model: str,
    prompt: str,
    temperature: float = 0.2,
) -> str:

    selected_model = normalize_model(model)

    # Normalize temperature so the UI value is safely handled.
    normalize_temperature(temperature)

    try:

        response = client.models.generate_content(
            model=selected_model,
            contents=prompt,
        )

    except Exception as exc:

        error_text = str(exc)
        error_lower = error_text.lower()

        if (
            "api key" in error_lower
            or "401" in error_text
            or "403" in error_text
            or "authentication" in error_lower
        ):
            raise RuntimeError(
                "Gemini authentication failed. "
                "Please check GEMINI_API_KEY in .env."
            ) from exc

        if (
            "404" in error_text
            or "not found" in error_lower
            or "no longer available" in error_lower
        ):
            raise RuntimeError(
                f"Gemini model '{selected_model}' "
                "is not available for this API key."
            ) from exc

        if (
            "429" in error_text
            or "quota" in error_lower
            or "resource exhausted" in error_lower
        ):
            raise RuntimeError(
                "Gemini API quota/rate limit reached. "
                "Please try again later."
            ) from exc

        raise RuntimeError(
            f"Gemini request failed: {error_text}"
        ) from exc

    text = getattr(
        response,
        "text",
        None
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


# ============================================================
# JSON EXTRACTION
# ============================================================

def extract_json(text: str) -> Any:

    if not text:
        return None

    cleaned = text.strip()

    # Remove markdown JSON fences.
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    cleaned = cleaned.strip()

    # Try complete JSON first.
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try JSON object.
    object_match = re.search(
        r"\{.*\}",
        cleaned,
        flags=re.DOTALL,
    )

    if object_match:

        try:
            return json.loads(
                object_match.group(0)
            )
        except json.JSONDecodeError:
            pass

    # Try JSON array.
    array_match = re.search(
        r"\[.*\]",
        cleaned,
        flags=re.DOTALL,
    )

    if array_match:

        try:
            return json.loads(
                array_match.group(0)
            )
        except json.JSONDecodeError:
            pass

    return None


# ============================================================
# FINDINGS SANITIZER
# ============================================================

def sanitize_findings(
    data: Any,
) -> list[dict[str, Any]]:

    if isinstance(data, dict):
        findings = data.get(
            "findings",
            []
        )

    elif isinstance(data, list):
        findings = data

    else:
        findings = []

    if not isinstance(findings, list):
        return []

    result: list[dict[str, Any]] = []

    for item in findings:

        if not isinstance(item, dict):
            continue

        title = str(
            item.get(
                "title",
                "Untitled Finding"
            )
        ).strip()

        severity = str(
            item.get(
                "severity",
                "Low"
            )
        ).strip().title()

        if severity not in {
            "High",
            "Medium",
            "Low",
        }:
            severity = "Low"

        description = str(
            item.get(
                "description",
                "No description provided."
            )
        ).strip()

        recommendation = str(
            item.get(
                "recommendation",
                "No recommendation provided."
            )
        ).strip()

        result.append(
            {
                "title": title,
                "severity": severity,
                "description": description,
                "recommendation": recommendation,
            }
        )

    return result


# ============================================================
# SCANNER AGENT
# ============================================================

def scanner_agent(
    state: PipelineState,
    client: genai.Client,
) -> PipelineState:

    source_code = state.get(
        "source_code",
        ""
    )

    model = state.get(
        "model",
        DEFAULT_MODEL
    )

    temperature = state.get(
        "temperature",
        0.2
    )

    scanner_prompt = (
        "You are the Scanner Agent of CodeGuard AI.\n\n"

        "Perform a focused professional audit of this Python code.\n\n"

        "Check for important issues in:\n"
        "- Security vulnerabilities\n"
        "- SQL injection\n"
        "- Command injection\n"
        "- Unsafe input handling\n"
        "- Hardcoded secrets\n"
        "- Authentication and authorization\n"
        "- Bugs\n"
        "- Exception handling\n"
        "- Resource leaks\n"
        "- Performance\n"
        "- Bad Python practices\n"
        "- Important PEP8 and maintainability problems\n\n"

        "Do NOT report trivial style problems.\n"
        "Focus on real and useful findings.\n\n"

        "Return ONLY valid JSON.\n\n"

        "Required JSON format:\n"
        "{\n"
        '  "findings": [\n'
        "    {\n"
        '      "title": "Short finding title",\n'
        '      "severity": "High",\n'
        '      "description": "Clear explanation",\n'
        '      "recommendation": "Specific recommendation"\n'
        "    }\n"
        "  ]\n"
        "}\n\n"

        "Severity must be exactly one of:\n"
        "High\n"
        "Medium\n"
        "Low\n\n"

        "If there are no important issues, return:\n"
        '{"findings": []}\n\n'

        "SOURCE CODE:\n"
        "```python\n"
        + source_code
        + "\n```\n"
    )

    scanner_output = call_gemini(
        client=client,
        model=model,
        prompt=scanner_prompt,
        temperature=temperature,
    )

    parsed = extract_json(
        scanner_output
    )

    findings = sanitize_findings(
        parsed
    )

    return {
        **state,
        "findings": findings,
        "scanner_output": scanner_output,
    }


# ============================================================
# REFACTOR AGENT
# ============================================================

def refactor_agent(
    state: PipelineState,
    client: genai.Client,
) -> PipelineState:

    source_code = state.get(
        "source_code",
        ""
    )

    findings = state.get(
        "findings",
        []
    )

    model = state.get(
        "model",
        DEFAULT_MODEL
    )

    temperature = state.get(
        "temperature",
        0.2
    )

    findings_json = json.dumps(
        findings,
        indent=2,
        ensure_ascii=False,
    )

    refactor_prompt = (
        "You are the Refactor Agent of CodeGuard AI.\n\n"

        "Improve the Python source code using the scanner findings.\n\n"

        "Requirements:\n"
        "- Fix identified security vulnerabilities.\n"
        "- Fix identified bugs.\n"
        "- Improve exception handling.\n"
        "- Improve readability.\n"
        "- Improve maintainability.\n"
        "- Preserve the original functionality.\n"
        "- Do not add unrelated features.\n"
        "- Do not explain the changes.\n"
        "- Return ONLY Python source code.\n"
        "- Do not use Markdown code fences.\n\n"

        "SCANNER FINDINGS:\n"
        + findings_json
        + "\n\n"

        "ORIGINAL SOURCE CODE:\n"
        + source_code
        + "\n"
    )

    refactor_output = call_gemini(
        client=client,
        model=model,
        prompt=refactor_prompt,
        temperature=temperature,
    )

    refactored_code = refactor_output.strip()

    # Remove accidental Markdown fences.
    refactored_code = re.sub(
        r"^```(?:python)?\s*",
        "",
        refactored_code,
        flags=re.IGNORECASE,
    )

    refactored_code = re.sub(
        r"\s*```$",
        "",
        refactored_code,
    )

    refactored_code = refactored_code.strip()

    return {
        **state,
        "refactored_code": refactored_code,
        "refactor_output": refactor_output,
    }


# ============================================================
# DOCUMENTATION AGENT
# ============================================================

def documentation_agent(
    state: PipelineState,
    client: genai.Client,
) -> PipelineState:

    refactored_code = state.get(
        "refactored_code",
        ""
    )

    model = state.get(
        "model",
        DEFAULT_MODEL
    )

    temperature = state.get(
        "temperature",
        0.2
    )

    documentation_prompt = (
        "You are the Documentation Agent of CodeGuard AI.\n\n"

        "Create concise professional Markdown documentation "
        "for the following Python project.\n\n"

        "Include these sections:\n"
        "# Project Overview\n"
        "# Features\n"
        "# Installation\n"
        "# Usage\n"
        "# Code Structure\n"
        "# Security Notes\n\n"

        "Keep the documentation practical and concise.\n"
        "Return ONLY Markdown.\n\n"

        "PYTHON CODE:\n"
        "```python\n"
        + refactored_code
        + "\n```\n"
    )

    docs_output = call_gemini(
        client=client,
        model=model,
        prompt=documentation_prompt,
        temperature=temperature,
    )

    documentation = docs_output.strip()

    return {
        **state,
        "documentation": documentation,
        "docs_output": docs_output,
    }


# ============================================================
# RUN PIPELINE
# ============================================================

def run_pipeline(
    *,
    source_code: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> dict[str, Any]:

    if not source_code or not source_code.strip():
        raise ValueError(
            "Source code cannot be empty."
        )

    normalized_model = normalize_model(
        model
    )

    normalized_temperature = normalize_temperature(
        temperature
    )

    client = create_client()

    state: PipelineState = {
        "source_code": source_code,
        "model": normalized_model,
        "temperature": normalized_temperature,
        "findings": [],
        "refactored_code": "",
        "documentation": "",
    }

    # ========================================================
    # STEP 1 — SCANNER
    # ========================================================

    state = scanner_agent(
        state,
        client,
    )

    # ========================================================
    # STEP 2 — REFACTOR
    # ========================================================

    state = refactor_agent(
        state,
        client,
    )

    # ========================================================
    # STEP 3 — DOCUMENTATION
    # ========================================================

    state = documentation_agent(
        state,
        client,
    )

    return {
        "findings": state.get(
            "findings",
            []
        ),

        "refactored_code": state.get(
            "refactored_code",
            ""
        ),

        "documentation": state.get(
            "documentation",
            ""
        ),

        "scanner_output": state.get(
            "scanner_output",
            ""
        ),

        "refactor_output": state.get(
            "refactor_output",
            ""
        ),

        "docs_output": state.get(
            "docs_output",
            ""
        ),

        "model": normalized_model,

        "temperature": normalized_temperature,
    }