import json
import re
from llm import ask_gemini
from prompts import decision_prompt
from memory import load_memory, save_memory

class GeminiAgent:
    def __init__(self, tools: dict, max_steps=5):
        self.tools = tools
        self.memory = load_memory()
        self.max_steps = max_steps

    def think(self, goal: str):
        prompt = decision_prompt(goal, list(self.tools.keys()), self.memory)
        response = ask_gemini(prompt)

        print("🧠 Gemini:")
        print(response)

        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group())

        return {"tool": None, "input": None, "done": True}

    def act(self, decision: dict):
        tool = decision.get("tool")
        tool_input = decision.get("input")

        if tool in self.tools:
            return self.tools[tool](tool_input)

        return "No action"

    def remember(self, goal, tool, result):
        self.memory.append({
            "goal": goal,
            "tool": tool,
            "result": str(result)
        })
        save_memory(self.memory)
    def run(self, goal: str):
        print(f"🎯 Main Goal: {goal}")
        sub_goals = decompose_goal(goal)
        final_results = []

        for sub_goal in sub_goals:
            print(f"\n📌 Sub-goal: {sub_goal}")
            step = 0
            last_result = None

            while step < self.max_steps:
                print(f"🔁 Step {step + 1}")
                decision = self.think(sub_goal)

                if decision.get("done"):
                    print("✅ Sub-goal done.")
                    break

                result = self.act(decision)
                last_result = result
                self.remember(sub_goal, decision.get("tool"), result)
                step += 1

            final_results.append(last_result)

        return final_results

    def decompose_goal(goal: str):
        """
          Simple decomposition:
         - Split by 'and'
         - Can be replaced by Gemini for smarter decomposition
        """
        # Normalize input
        parts = [g.strip() for g in goal.lower().split("and")]
        return parts if parts else [goal]

