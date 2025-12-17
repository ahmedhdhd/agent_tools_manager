def decision_prompt(goal: str, tools: list) -> str:
    return f"""
You are an AI agent.

Goal:
{goal}

Available tools:
{", ".join(tools)}

Rules:
- Choose ONE tool
- Respond ONLY in JSON
- No explanation

JSON format:
{{
  "tool": "tool_name",
  "input": "text passed to the tool"
}}
"""
