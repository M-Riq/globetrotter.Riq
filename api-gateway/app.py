"""
API Gateway.

A thin reverse proxy: forwards each request to the microservice
responsible for it (see config.SERVICE_ROUTES) and streams the
response back unchanged. It does not re-implement authentication or
business logic -- every service validates its own JWT and enforces
its own RBAC, exactly as if the frontend were calling it directly.
This keeps the gateway simple, stateless, and safe to scale
horizontally or replace with a managed API gateway later.
"""
import requests
from flask import Flask, Response, request
from flask_cors import CORS

import config


def _match_service(full_path: str):
    for prefix in config.ORDERED_PREFIXES:
        if full_path == prefix or full_path.startswith(prefix + "/"):
            return config.SERVICE_ROUTES[prefix]
    return None


def create_app():
    app = Flask(__name__)
    CORS(app, origins=config.CORS_ORIGINS)

    @app.route("/health")
    def health():
        results = {}
        overall_ok = True
        for name, base_url in config.HEALTH_ENDPOINTS.items():
            try:
                resp = requests.get(f"{base_url}/health", timeout=2)
                results[name] = {"status": "up" if resp.status_code == 200 else "degraded"}
                if resp.status_code != 200:
                    overall_ok = False
            except requests.RequestException:
                results[name] = {"status": "down"}
                overall_ok = False
        return {"status": "ok" if overall_ok else "degraded", "services": results}, (200 if overall_ok else 503)

    @app.route("/api/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def proxy(subpath):
        full_path = "/api/" + subpath
        target_base = _match_service(full_path)
        if not target_base:
            return {"success": False, "error": "no route configured for this path"}, 404

        target_url = f"{target_base}{full_path}"
        forward_headers = {k: v for k, v in request.headers if k.lower() != "host"}

        try:
            upstream_resp = requests.request(
                method=request.method,
                url=target_url,
                headers=forward_headers,
                params=request.args,
                data=request.get_data(),
                timeout=15,
            )
        except requests.RequestException:
            return {"success": False, "error": "upstream service unavailable"}, 502

        excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
        response_headers = [
            (k, v) for k, v in upstream_resp.headers.items() if k.lower() not in excluded_headers
        ]
        return Response(upstream_resp.content, status=upstream_resp.status_code, headers=response_headers)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
