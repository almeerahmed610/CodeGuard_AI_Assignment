def docs_agent(state,llm):
    code=state.get("refactored_code",state.get("source_code",""))
    prompt=f"""You are the Docs Agent.
Create professional README.md documentation for the cleaned Python code.
Include title, overview, key improvements, installation, usage,
security/quality notes and documentation guidance.
Return ONLY Markdown.

CLEANED CODE:
{code}"""
    response=llm.invoke(prompt)
    text=response.content if isinstance(response.content,str) else str(response.content)
    return {**state,"documentation":text.strip()}
