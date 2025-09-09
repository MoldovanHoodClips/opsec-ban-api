from flask import Flask, jsonify

app = Flask(__name__)

# -----------------------
# Ban list (just machine IDs)
# -----------------------
# Example: Replace these with actual machine IDs you want to ban
bans = [
    "machine_id_1",
    "machine_id_2",
    "machine_id_3"
]

# -----------------------
# Routes
# -----------------------
@app.route("/bans.json")
def get_bans():
    """
    Returns the ban list as JSON.
    Example response:
    ["machine_id_1", "machine_id_2"]
    """
    return jsonify(bans)

@app.route("/")
def home():
    return "OPSEC Ban API is running!"

# -----------------------
# Run server
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
