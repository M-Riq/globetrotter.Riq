"""
Itinerary Service entrypoint.
"""
from flask import Flask
from flask_cors import CORS

import config
from routes.admin_routes import admin_itinerary_bp
from routes.itinerary_routes import itinerary_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    CORS(app, origins=config.CORS_ORIGINS)

    app.register_blueprint(itinerary_bp, url_prefix="/api/itineraries")
    app.register_blueprint(admin_itinerary_bp, url_prefix="/api/admin/itineraries")

    @app.route("/health")
    def health():
        return {
            "status": "ok",
            "service": config.SERVICE_NAME,
            "google_maps_configured": bool(config.MAPBOX_ACCESS_TOKEN),
        }, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
