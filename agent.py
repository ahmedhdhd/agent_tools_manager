import json
import re
from llm import ask_gemini
from prompts import decision_prompt

class GeminiAgent:
    def __init__(self, tools: dict):
        self.tools = tools

    def think(self, goal: str):
        prompt = decision_prompt(goal, list(self.tools.keys()))
        response = ask_gemini(prompt)

        print("🔍 Gemini raw response:")
        print(response)

        # Try direct JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from text
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return {"tool": None, "input": None}

    def act(self, decision: dict):
        tool_name = decision.get("tool")
        tool_input = decision.get("input")

        if tool_name in self.tools:
            return self.tools[tool_name](tool_input)

        return "No valid tool selected"

    def run(self, goal: str):
        decision = self.think(goal)
        return self.act(decision)
