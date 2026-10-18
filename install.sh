#!/usr/bin/env bash
# twinops bootstrap: copies env, starts the whole stack, prints next steps.
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env from .env.example"
  echo "==> Set JWT_SECRET and POSTGRES_PASSWORD before going remote:"
  echo "==>   openssl rand -hex 32"
fi

echo "==> Starting Uptime Kuma + Tianji + Postgres + portal..."
docker compose up -d --build

echo ""
echo "==> Portal          : http://127.0.0.1:8080"
echo "==> Uptime Kuma     : http://127.0.0.1:3001   (first visit = admin setup)"
echo "==> Tianji          : http://127.0.0.1:12345   (first account = admin)"
echo ""
echo "==> For remote access, put your own reverse proxy or Cloudflare Tunnel in front."
