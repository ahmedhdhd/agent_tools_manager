def calculator(input_text: str):
    # very simple example
    expression = input_text.replace("calculate", "").strip()
    try:
        return eval(expression)
    except:
        return "Invalid calculation"


def write_file(input_text: str):
    with open("output.txt", "w") as f:
        f.write(input_text)
    return "Text saved to output.txt"
