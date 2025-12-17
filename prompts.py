def decision_prompt(goal: str, tools: list, memory: list) -> str:
    memory_text = (
        "No memory yet."
        if not memory
        else "\n".join(
            f"- Goal: {m['goal']}, Tool: {m['tool']}, Result: {m['result']}"
            for m in memory[-5:]
        )
    )

    return f"""
You are an autonomous AI agent.

Goal:
{goal}

Memory + tool feedback:
{memory_text}

Available tools:
{", ".join(tools)}

Instructions:
- Decide the next action
- Use previous tool results to inform your choice
- Respond ONLY with JSON
- Format:
{{
  "tool": "<tool name or null>",
  "input": "<input for tool>",
  "done": true or false
}}
"""
