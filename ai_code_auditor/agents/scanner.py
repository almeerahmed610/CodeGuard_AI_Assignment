import json

def scanner_agent(state,llm):
    code=state["source_code"]
    prompt=f"""You are the Scanner Agent in a sequential AI code-auditing pipeline.
Audit this Python code for security vulnerabilities, bugs, bad practices, maintainability,
PEP8/style issues and unnecessary complexity.
Return ONLY valid JSON:
{{"audit_report":"brief report","findings":[{{"severity":"High|Medium|Low","title":"short title","description":"what is wrong","recommendation":"how to fix"}}]}}
CODE:
{code}"""
    response=llm.invoke(prompt)
    text=response.content if isinstance(response.content,str) else str(response.content)
    try: data=json.loads(text)
    except json.JSONDecodeError:
        a,b=text.find("{"),text.rfind("}")
        data=json.loads(text[a:b+1]) if a>=0 and b>a else {"audit_report":text,"findings":[]}
    return {**state,**data}
