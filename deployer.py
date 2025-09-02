import nbformat as nbf
import urllib.parse
import os

def create_user_colab(version, software, user_id):
    notebook = nbf.v4.new_notebook()

    # Cell 1: Instructions
    notebook.cells.append(nbf.v4.new_markdown_cell(
        f"# Welcome {user_id}\n"
        f"## Minecraft {software} {version} Server Setup\n"
        f"Press **play** on each cell to setup your server."
    ))

    # Cell 2: Install dependencies
    install_cmds = [
        "apt-get update -y",
        "apt-get install -y openjdk-21-jdk wget screen unzip curl"
    ]
    notebook.cells.append(nbf.v4.new_code_cell("\n".join(f"!{c}" for c in install_cmds)))

    # Cell 3: Create server folder
    server_dir = f"/content/{user_id}_mc_{software}_{version.replace('.','_')}"
    notebook.cells.append(nbf.v4.new_code_cell(f"""
import os
server_dir = "{server_dir}"
os.makedirs(server_dir, exist_ok=True)
print("Server directory created:", server_dir)
"""))

    # Cell 4: Download server jar
    jar_urls = {
        "spigot": f"https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar",
        "paper": f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/latest/downloads/paper-{version}-latest.jar",
        "vanilla": "<VANILLA_SERVER_URL>",
        # Add others...
    }
    url = jar_urls.get(software.lower(), jar_urls["vanilla"])
    notebook.cells.append(nbf.v4.new_code_cell(f"""
import requests
jar_file = "{server_dir}/{software}-{version}.jar"
r = requests.get("{url}")
with open(jar_file,"wb") as f: f.write(r.content)
print("Downloaded server jar to", jar_file)
"""))

    # Cell 5: Accept EULA
    notebook.cells.append(nbf.v4.new_code_cell(f"""
with open("{server_dir}/eula.txt","w") as f:
    f.write("eula=true\\n")
print("EULA accepted")
"""))

    # Cell 6: Start server
    notebook.cells.append(nbf.v4.new_code_cell(f"""
!cd "{server_dir}" && java -Xmx1024M -Xms1024M -jar {software}-{version}.jar nogui
"""))

    # Save notebook
    notebook_path = f"{user_id}_{software}_{version}.ipynb"
    nbf.write(notebook, notebook_path)
    print("Notebook created:", notebook_path)

    # Generate Colab link
    colab_url = f"https://colab.research.google.com/drive/{urllib.parse.quote(notebook_path)}"
    return colab_url

# Example usage
link = create_user_colab("1.20.1", "paper", "user123")
print("Open this link in browser:", link)
