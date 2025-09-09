from flask import Flask, jsonify
import requests
import os, base64, json

app = Flask(__name__)

# PAT stored as environment variable (secure)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "MoldovanHoodClips/bans"
FILE_PATH = "bans.json"

@app.route("/")
def home():
    return "✅ Ban API is running"

@app.route("/banlist")
def get_banlist():
    try:
        url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

        content = base64.b64decode(data["content"]).decode()
        bans = json.loads(content)
        return jsonify(bans)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
