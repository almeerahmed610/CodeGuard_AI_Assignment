def refactor_agent(state,llm):
    prompt=f"""You are the Refactor Agent.
Improve the Python code using the Scanner Agent findings.
Fix security/correctness problems, use parameterized SQL when needed,
improve readability and PEP8 compliance, preserve intended behavior,
and return ONLY complete Python code without markdown fences.

AUDIT:
{state.get("audit_report","")}
FINDINGS:
{state.get("findings",[])}
ORIGINAL CODE:
{state["source_code"]}"""
    response=llm.invoke(prompt)
    text=response.content if isinstance(response.content,str) else str(response.content)
    if "```" in text:
        parts=text.split("```"); text=parts[1] if len(parts)>1 else text
        if text.lstrip().startswith("python"): text=text.lstrip()[6:]
    return {**state,"refactored_code":text.strip()}
