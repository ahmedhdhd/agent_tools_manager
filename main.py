from agent import GeminiAgent
from tools import calculator, write_file

tools = {
    "calculator": calculator,
    "write_file": write_file
}

agent = GeminiAgent(tools)

goal = "calculate and save the result of one plus seven mines  19"
result = agent.run(goal)

print("Agent result:", result)
