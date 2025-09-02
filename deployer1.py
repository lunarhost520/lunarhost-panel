# deployer1.py
import nbformat as nbf
import argparse
import os

def create_base_notebook(user_id):
    notebook = nbf.v4.new_notebook()
    notebook.cells.append(nbf.v4.new_markdown_cell(
        f"# Welcome {user_id}\n"
        f"Your Minecraft server notebook will be populated automatically."
    ))

    notebook_path = f"{user_id}_base.ipynb"
    nbf.write(notebook, notebook_path)
    print(notebook_path)  # Output for GitHub Actions log
    return notebook_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True, help="User/server name")
    args = parser.parse_args()
    create_base_notebook(args.user)
