def generate_tests_prompt(code: str, analysis: str):
    return f"""
You are a senior QA engineer.

Given this code and analysis, generate pytest tests.
Rules:
- Use pytest
- Test normal and edge cases
- No explanation, only code

Code:
{code}

Analysis:
{analysis}
"""


def understand_code_prompt(code: str):
    return f"""
You are a senior Python developer.

Analyze this code and explain:
- What it does
- What functions/classes should be tested
- Important edge cases

Code:
{code}
"""
