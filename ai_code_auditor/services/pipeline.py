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

    api_key = get_api_key()

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# MODEL NORMALIZER
# ============================================================

def normalize_model(model: str | None) -> str:

    selected_model = (
        model.strip()
        if isinstance(model, str) and model.strip()
        else DEFAULT_MODEL
    )

    selected_model = selected_model.replace(
        "models/",
        "",
    )

    # Old unavailable model
    if selected_model == "gemini-2.5-flash":

        return DEFAULT_MODEL

    return selected_model


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

    # Gemini 3.x models generally work best with
    # their default generation behavior. We only
    # pass temperature when it is useful and valid.

    try:

        response = client.models.generate_content(
            model=selected_model,
            contents=prompt,
        )

    except Exception as exc:

        error_text = str(exc)

        # Make the error easier to understand.
        if (
            "API key" in error_text
            or "api key" in error_text
            or "401" in error_text
            or "403" in error_text
        ):

            raise RuntimeError(
                "Gemini authentication failed. "
                "Please check GEMINI_API_KEY in .env."
            ) from exc

        if (
            "not found" in error_text.lower()
            or "404" in error_text
            or "no longer available" in error_text.lower()
        ):

            raise RuntimeError(
                f"Gemini model '{selected_model}' is not "
                "available for this API key."
            ) from exc

        raise RuntimeError(
            f"Gemini request failed: {error_text}"
        ) from exc

    text = getattr(
        response,
        "text",
        None,
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

    # Remove markdown code fences.
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

    try:

        return json.loads(cleaned)

    except json.JSONDecodeError:
        pass

    # Find first JSON object.
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

    # Find first JSON array.
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
# SCANNER AGENT
# ============================================================

def scanner_agent(
    state: PipelineState,
    client: genai.Client,
) -> PipelineState:

    source_code = state.get(
        "source_code",
        "",
    )

    model = state.get(
        "model",
        DEFAULT_MODEL,
    )

    prompt = f"""
You are the Scanner Agent of CodeGuard AI.

Your job is to perform a professional Python code audit.

Analyze the source code for:

1. Security vulnerabilities
2. SQL injection
3. Command injection
4. Unsafe input handling
5. Authentication or authorization issues
6. Hardcoded secrets
7. Bugs
8. Exception handling problems
9. Resource leaks
10. Code quality issues
11. Maintainability problems
12. Bad Python practices
13. PEP8 issues
14. Performance problems
15. Dangerous or deprecated patterns

Return ONLY valid JSON.

Required format:

{{
  "findings": [
    {{
      "title": "Short finding title",
      "severity": "High",
      "description": "Detailed explanation",
      "recommendation": "Specific recommendation"
    }}
  ]
}}

Severity must be exactly one of:

High
Medium
Low

If there are no issues, return:

{{
  "findings": []
}}

SOURCE CODE:

```python
{source_code}