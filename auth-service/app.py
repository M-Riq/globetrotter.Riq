"""
Auth Service entrypoint (Application Factory pattern, same as the
monolith's app/__init__.py).
"""
from flask import Flask
from flask_cors import CORS

import config
from routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    CORS(app, origins=config.CORS_ORIGINS)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": config.SERVICE_NAME}, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
