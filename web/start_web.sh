#!/usr/bin/env bash
# start_web.sh — launch the GGSD harness view on hilarious_marcupial (245).
# User-level only: no sudo, no pip, stdlib python3. Idempotent-ish: refuses
# to start a second copy.
set -euo pipefail
cd "$(dirname "$0")/.."
if pgrep -f "ggsd_web.py" >/dev/null; then
  echo "ggsd_web already running:"; pgrep -af "ggsd_web.py"; exit 0
fi
nohup python3 web/ggsd_web.py --host 0.0.0.0 --port 8080 > web/ggsd_web.log 2>&1 &
echo "started pid $! — log: web/ggsd_web.log"
sleep 1
curl -s -o /dev/null -w "local check: %{http_code}\n" http://127.0.0.1:8080/health
