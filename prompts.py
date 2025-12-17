def decision_prompt(goal: str, tools: list, memory: list) -> str:
    memory_text = (
        "No previous memory."
        if not memory
        else "\n".join(
            f"- Goal: {m['goal']}, Tool: {m['tool']}, Result: {m['result']}"
            for m in memory[-5:]  # last 5 entries
        )
    )

    return f"""
You are an AI agent.

Previous memory:
{memory_text}

Current goal:
{goal}

Available tools:
{", ".join(tools)}

STRICT RULES:
- Respond ONLY with valid JSON
- Choose ONE tool
- No explanations

JSON:
{{
  "tool": "<tool name>",
  "input": "<input for tool>"
}}
"""
