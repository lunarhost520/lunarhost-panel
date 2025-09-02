!pip install flask-ngrok psutil
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import subprocess, psutil, os, requests

app = Flask(__name__)
run_with_ngrok(app)

SERVER_DIR = "/content/mc_spigot_server"  # default, adjust dynamically if needed

@app.route("/run", methods=["POST"])
def run_server():
    data = request.json
    version = data.get("version")
    software = data.get("software")
    global SERVER_DIR
    SERVER_DIR = f"/content/mc_{software}_{version.replace('.','_')}"
    os.makedirs(SERVER_DIR, exist_ok=True)
    process = subprocess.Popen(
        ["python3","deployer_colab.py",version,software],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    def generate():
        for line in process.stdout:
            yield line.decode()
    return app.response_class(generate(), mimetype="text/plain")

@app.route("/status")
def status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    return jsonify({"cpu":cpu,"ramUsed":ram.used//1024//1024,"ramTotal":ram.total//1024//1024})

@app.route("/files")
def files():
    try:
        files = os.listdir(SERVER_DIR)
        return jsonify(files)
    except:
        return jsonify([])

@app.route("/install-plugin", methods=["POST"])
def install_plugin():
    data = request.json
    url = data.get("url")
    plugin_name = url.split("/")[-1]
    plugin_path = os.path.join(SERVER_DIR,"plugins",plugin_name)
    os.makedirs(os.path.join(SERVER_DIR,"plugins"), exist_ok=True)
    try:
        r = requests.get(url)
        with open(plugin_path,"wb") as f:
            f.write(r.content)
        return f"Plugin {plugin_name} installed successfully!"
    except Exception as e:
        return f"Failed to install plugin: {str(e)}"

app.run()
