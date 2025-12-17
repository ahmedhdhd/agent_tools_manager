import os

def write_test(module_name: str, content: str):
    os.makedirs("tests", exist_ok=True)
    path = f"tests/test_{module_name}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Created {path}"
