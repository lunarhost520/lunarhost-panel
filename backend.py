!pip install flask-ngrok psutil
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import subprocess, psutil

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/run", methods=["POST"])
def run_server():
    data = request.json
    version = data.get("version")
    software = data.get("software")
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

app.run()
