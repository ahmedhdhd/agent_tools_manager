from agent import GeminiAgent
from tools import calculator, write_file

tools = {
    "calculator": calculator,
    "write_file": write_file
}

agent = GeminiAgent(tools)

goal = "calculate 25 * 4"
result = agent.run(goal)

print("Agent result:", result)
