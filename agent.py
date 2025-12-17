import json
import re
from llm import ask_gemini
from prompts import decision_prompt
from memory import load_memory, save_memory

class GeminiAgent:
    def __init__(self, tools: dict):
        self.tools = tools
        self.memory = load_memory()

    def think(self, goal: str):
        prompt = decision_prompt(goal, list(self.tools.keys()), self.memory)
        response = ask_gemini(prompt)

        print("🧠 Gemini response:")
        print(response)

        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group())

        return {"tool": None, "input": None}

    def act(self, decision: dict):
        tool = decision.get("tool")
        tool_input = decision.get("input")

        if tool in self.tools:
            result = self.tools[tool](tool_input)
            return tool, result

        return None, "No valid tool"

    def remember(self, goal, tool, result):
        self.memory.append({
            "goal": goal,
            "tool": tool,
            "result": str(result)
        })
        save_memory(self.memory)

    def run(self, goal: str):
        decision = self.think(goal)
        tool, result = self.act(decision)
        self.remember(goal, tool, result)
        return result
