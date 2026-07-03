from flask import Flask, jsonify, request
import os
import socket
from datetime import datetime

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "dev")
HOSTNAME = socket.gethostname()


@app.route("/")
def index():
    return jsonify(
        {
            "service": "ecs-test",
            "version": VERSION,
            "hostname": HOSTNAME,
            "time": datetime.utcnow().isoformat() + "Z",
        }
    )


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"received": data, "from": HOSTNAME})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
