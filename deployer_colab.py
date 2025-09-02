import os, subprocess, sys, requests, psutil

version = sys.argv[1]
software = sys.argv[2]

server_dir = f"/content/mc_{software}_{version.replace('.','_')}"
os.makedirs(server_dir, exist_ok=True)
os.chdir(server_dir)

# Install Java + packages
subprocess.run(["apt-get","update","-y"])
subprocess.run(["apt-get","install","-y","wget","curl","screen","unzip","openjdk-21-jdk"])

# Install Playit.gg CLI
if not os.path.exists("playit-cli-linux-amd64"):
    subprocess.run(["wget","https://github.com/playit-cloud/playit-agent/releases/latest/download/playit-cli-linux-amd64"])
    subprocess.run(["chmod","+x","playit-cli-linux-amd64"])

# Download server jar
download_urls = {
    "spigot": "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar",
    "paper": f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/latest/downloads/paper-{version}-latest.jar",
    "purpur": f"https://api.purpurmc.org/download/{version}/purpur-{version}.jar",
    "vanilla": f"https://launcher.mojang.com/v1/objects/.../server.jar", # replace with actual
    # add other software urls...
}
jar_file = f"{software}-{version}.jar"
r = requests.get(download_urls[software.lower()])
with open(jar_file,"wb") as f: f.write(r.content)

# Accept EULA
with open("eula.txt","w") as f: f.write("eula=true\n")

# Start server
subprocess.run(["java","-Xmx1024M","-Xms1024M","-jar",jar_file,"nogui"])
