from flask import Flask, jsonify, request, render_template_string
import os
import socket
from datetime import datetime

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "dev")
HOSTNAME = socket.gethostname()

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ecs-test — Flask on ECS</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0e0;
            min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
        }
        .card {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 48px;
            max-width: 520px;
            width: 90%;
            text-align: center;
            backdrop-filter: blur(12px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }
        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 6px 16px;
            border-radius: 20px;
            margin-bottom: 24px;
        }
        h1 {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #667eea, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        p.subtitle {
            color: #a0a0b8;
            font-size: 15px;
            margin-bottom: 32px;
            line-height: 1.5;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 32px;
        }
        .stat {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 14px 10px;
        }
        .stat-label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888;
            margin-bottom: 4px;
        }
        .stat-value {
            font-size: 14px;
            font-weight: 600;
            color: #c4b5fd;
            word-break: break-all;
        }
        .endpoints {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .endpoint {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 13px;
            font-family: "SF Mono", "Fira Code", monospace;
            color: #a78bfa;
        }
        .footer {
            margin-top: 32px;
            font-size: 11px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">Fargate + Terraform</div>
        <h1>ecs-test</h1>
        <p class="subtitle">
            Flask demo app running on <strong>AWS ECS</strong> behind an Application Load Balancer.
            Deployed automatically via GitHub Actions on every push to main.
        </p>

        <div class="grid">
            <div class="stat">
                <div class="stat-label">Version</div>
                <div class="stat-value">{{ version }}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Hostname</div>
                <div class="stat-value">{{ hostname }}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Region</div>
                <div class="stat-value">eu-west-1</div>
            </div>
            <div class="stat">
                <div class="stat-label">Time</div>
                <div class="stat-value" id="time">{{ time }}</div>
            </div>
        </div>

        <div class="endpoints">
            <span class="endpoint">GET /</span>
            <span class="endpoint">GET /health</span>
            <span class="endpoint">POST /echo</span>
        </div>

        <div class="footer">ECS Fargate • Terraform • GitHub Actions</div>
    </div>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(
        INDEX_HTML,
        version=VERSION,
        hostname=HOSTNAME,
        time=datetime.utcnow().isoformat() + "Z",
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
