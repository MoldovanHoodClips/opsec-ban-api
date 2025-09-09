from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Path to the bans.json file
BANS_FILE = os.path.join(os.path.dirname(__file__), "bans.json")

@app.route("/bans.json")
def get_bans():
    """
    Returns the current ban list as JSON.
    This reads the file each time, so updates are live without restarting.
    """
    try:
        with open(BANS_FILE, "r") as f:
            bans = json.load(f)
        return jsonify(bans)
    except FileNotFoundError:
        return jsonify({"error": "bans.json not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "bans.json is invalid"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "OPSEC Ban API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
