import threading
import time
import requests
import json
import base64
from flask import Flask, jsonify

# === CONFIG ===
BANS_REPO = "MoldovanHoodClips/bans"
BANS_FILE = "bans.json"
GITHUB_TOKEN = "YOUR_GITHUB_PAT"  # Replace with your GitHub PAT
UPDATE_INTERVAL = 15  # seconds

banlist = []

# === FETCH BANLIST FUNCTION ===
def fetch_banlist():
    global banlist
    url = f"https://api.github.com/repos/{BANS_REPO}/contents/{BANS_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        banlist = json.loads(content).get("banned_ids", [])
        print(f"✅ Ban list updated! {len(banlist)} entries.")
    except Exception as e:
        print(f"⚠️ Could not fetch ban list: {e}")

# === BACKGROUND UPDATER ===
def start_banlist_updater():
    def loop():
        while True:
            fetch_banlist()
            time.sleep(UPDATE_INTERVAL)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

# === FLASK APP ===
app = Flask(__name__)

@app.route("/")
def home():
    return "OPSEC Ban API is running!"

@app.route("/banlist")
def get_banlist():
    return jsonify({"banned_ids": banlist})

@app.route("/check/<machine_id>")
def check_machine(machine_id):
    banned = machine_id in banlist
    return jsonify({"machine_id": machine_id, "banned": banned})

# === MAIN ===
if __name__ == "__main__":
    print("Starting OPSEC Ban API Server...")
    start_banlist_updater()
    # Run Flask on all interfaces (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000)
