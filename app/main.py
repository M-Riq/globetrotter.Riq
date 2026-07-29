"""
app/main.py

Flask application entry point.

Run locally:
    python app/main.py

Or via Docker / docker-compose (see project root).
"""
import os

#Va chercher la fonction create_app() dans le package app
from app import create_app

app = create_app()

#"Exécute ce bloc uniquement si ce fichier est lancé directement."
if __name__ == "__main__":
    
    #"Cherche la variable d'environnement PORT. Si elle n'existe pas, utilise 5000."
    port = int(os.environ.get("PORT", 5000))
    # Enable debug mode only when explicitly requested (e.g. FLASK_DEBUG=1).
    # Never enable debug in production – it exposes an interactive debugger.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
