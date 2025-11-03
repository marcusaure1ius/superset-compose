#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
MODE=${METADATA_DB_MODE:-dev}
FILE="docker-compose-dev.yml"
if [[ "${MODE,,}" == "prod" ]]; then
  FILE="docker-compose-prod.yml"
fi
exec docker compose -f "$FILE" "$@"
