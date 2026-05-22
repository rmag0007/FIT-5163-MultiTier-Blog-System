from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

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
    app.run(ssl_context="adhoc", debug=True)