"""Application factory for the Flask backend.

This module creates and configures the Flask `app` instance, applies
extensions and registers blueprints for the different API areas.
"""

from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db


def create_app():
    """Build and return a configured Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable cross-origin requests for the frontend dev server and
    # initialize the database extension.
    CORS(app)
    db.init_app(app)

    # Register API blueprints grouped by functionality
    from routes.auth import auth_bp
    from routes.track import track_bp
    from routes.dashboard import dashboard_bp
    from routes.posts import posts_bp 

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(track_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(posts_bp, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    # In production serve behind a real web server; debug mode is for dev.
    app.run(
        ssl_context=("127.0.0.1+1.pem", "127.0.0.1+1-key.pem"),
        debug=True,
        port=5000
    )
