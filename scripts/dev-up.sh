#!/usr/bin/env bash
# Build and start every GlobeTrotter microservice locally via Docker Compose.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo "No .env found -- copying .env.example. Edit it before running in production!"
  cp .env.example .env
fi

docker compose up --build
