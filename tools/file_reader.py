def read_file(path: str, max_lines=200):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return "".join(lines[:max_lines])
