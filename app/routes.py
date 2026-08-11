from flask import Blueprint, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cloud Support & Incident Intelligence Platform</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 50px 25px;
                line-height: 1.6;
                color: #1f2937;
                background-color: #f8fafc;
            }

            h1 {
                font-size: 2.4rem;
                margin-bottom: 10px;
            }

            h2 {
                margin-top: 35px;
                font-size: 1.4rem;
            }

            .subtitle {
                font-size: 1.15rem;
                color: #475569;
            }

            .card {
                background: white;
                padding: 22px;
                margin-top: 20px;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }

            .architecture {
                background: #0f172a;
                color: #e2e8f0;
                padding: 18px;
                border-radius: 8px;
                font-family: monospace;
                overflow-x: auto;
            }

            .endpoints a {
                display: block;
                margin: 8px 0;
                color: #2563eb;
                text-decoration: none;
            }

            .endpoints a:hover {
                text-decoration: underline;
            }

            .status {
                display: inline-block;
                padding: 5px 10px;
                background: #dcfce7;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: bold;
            }

            footer {
                margin-top: 45px;
                color: #64748b;
                font-size: 0.9rem;
            }
        </style>
    </head>

    <body>

        <span class="status">● Platform Online</span>

        <h1>Cloud Support & Incident Intelligence Platform</h1>

        <p class="subtitle">
            A production-style AWS cloud support engineering lab built to
            demonstrate deployment, monitoring, troubleshooting, incident
            response, root-cause analysis, and operational support of a
            customer-facing cloud service.
        </p>

        <div class="card">
            <h2>About the Project</h2>

            <p>
                This project simulates the type of environment a Cloud Support
                Engineer or Technical Support Engineer may be responsible for
                supporting in production.
            </p>

            <p>
                Rather than focusing only on application development, the
                platform is designed around diagnosing failures across multiple
                technical layers including AWS infrastructure, Linux, networking,
                NGINX, Gunicorn, Flask, application configuration, monitoring,
                and permissions.
            </p>
        </div>

        <div class="card">
            <h2>Architecture</h2>

            <div class="architecture">
Internet → HTTPS → NGINX → Gunicorn → Flask
                              ↓
                     Health & Readiness
                              ↓
                         CloudWatch
                              ↓
                 Monitoring / Incident Analysis
            </div>
        </div>

        <div class="card">
            <h2>Operational Capabilities</h2>

            <ul>
                <li>AWS infrastructure provisioned with Terraform</li>
                <li>Secure EC2 administration through AWS Systems Manager</li>
                <li>NGINX reverse proxy with HTTPS</li>
                <li>Gunicorn production-style WSGI deployment</li>
                <li>Application health and readiness monitoring</li>
                <li>CloudWatch logging, metrics, and alarms</li>
                <li>Production-style troubleshooting and root-cause analysis</li>
                <li>AI-assisted CloudWatch log investigation</li>
            </ul>
        </div>

        <div class="card endpoints">
            <h2>Operational Endpoints</h2>

            <a href="/healthz">
                /healthz — Application liveness
            </a>

            <a href="/readyz">
                /readyz — Application readiness
            </a>

            <a href="/api/v1/status">
                /api/v1/status — Detailed operational status
            </a>
        </div>

        <div class="card">
            <h2>Engineering Goal</h2>

            <p>
                The goal is to demonstrate an end-to-end support engineering
                workflow:
            </p>

            <div class="architecture">
Detect → Investigate → Isolate → Resolve → Validate → Monitor → Document
            </div>
        </div>

        <footer>
            Built by Edikan Ekong · Cloud Support / Technical Support Engineering Lab
        </footer>

    </body>
    </html>
    """


@main_bp.route("/skill")
def skill():
    return {
        "skills": "Technical Support Engineering",
        "service": current_app.config["APP_NAME"],
    }, 200