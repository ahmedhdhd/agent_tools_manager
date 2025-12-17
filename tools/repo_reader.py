import subprocess
import os

def clone_repo(repo_url: str, dest="repo"):
    if not os.path.exists(dest):
        subprocess.run(["git", "clone", repo_url, dest], check=True)
    return list_files(dest)

def list_files(path):
    files = []
    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(".py") and "test" not in f.lower():
                files.append(os.path.join(root, f))
    return files
