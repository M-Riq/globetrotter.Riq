#!/usr/bin/env bash
# Quick check that every service is reachable and healthy.
set -euo pipefail
GATEWAY_URL="${GATEWAY_URL:-http://localhost:5000}"
echo "Checking $GATEWAY_URL/health ..."
curl -sf "$GATEWAY_URL/health" | python3 -m json.tool
