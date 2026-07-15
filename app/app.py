from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AWS EC2 Flask App</h1>
    <p>Application is running behind NGINX reverse proxy.</p>
    """

@app.route("/health")
def health():
    return {"status": "healthy", "service": "flask-support-app"}, 200

@app.route("/skill")
def skill():
    return {"skills": "Technical Support Engineering", "service": "flask-support-app"}, 200
