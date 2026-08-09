from flask import Blueprint, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return """
    <h1>AWS EC2 Flask App</h1>
    <p>Application is running behind NGINX reverse proxy.</p>
    """


@main_bp.route("/skill")
def skill():
    return {
        "skills": "Technical Support Engineering",
        "service": current_app.config["APP_NAME"],
    }, 200