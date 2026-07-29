"""
app/__init__.py

Flask application factory.
"""
import os
from flask import Flask


def create_app():
    """1 Create the Flask application."""
    app = Flask(__name__) #Parce que Flask utilise __name__ pour connaître : où se trouve le projet ;où chercher les ressources ;où charger certains fichiers.


    # Secret key used for JWT signing.  Set the SECRET_KEY environment variable
    # in production.  The fallback is intentionally weak and must never be used
    # outside of local development.
    """1 configuration de l'application."""
    #"Si une variable d'environnement SECRET_KEY existe, utilise-la. Sinon, utilise la valeur par défaut."
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "globetrotter-secret-change-in-prod"
    )


    """3 import les blueprints existant"""
    # Register all route blueprints
    from app.auth import auth_bp
    from app.destinations import destinations_bp
    from app.recommendations import recommendations_bp
    from app.itineraries import itineraries_bp

    """4 enregistrements des blueprints"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(itineraries_bp)

    #Note:  Sans ces appels à register_blueprint, tes tests avec curl auraient tous renvoyé 404.
    
    return app

    