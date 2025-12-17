from llm import ask_llm 
from tools.repo_reader import clone_repo
from tools.file_reader import read_file
from tools.test_writer import write_test
from prompts import understand_code_prompt, generate_tests_prompt
import os

class RepoTestAgent:
    def run(self, repo_url):
        files = clone_repo(repo_url)

        for file_path in files:
            print(f"Analyzing {file_path}")

            code = read_file(file_path)
            analysis = ask_llm(understand_code_prompt(code))

            tests = ask_llm(generate_tests_prompt(code, analysis))

            module_name = os.path.basename(file_path).replace(".py", "")
            write_test(module_name, tests)

        print("Test generation completed")
