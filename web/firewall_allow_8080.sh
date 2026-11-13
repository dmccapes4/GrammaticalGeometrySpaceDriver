#!/usr/bin/env bash
# firewall_allow_8080.sh — run ON hilarious_marcupial (245), by the operator.
# Allows inbound TCP 8080 (GGSD harness view) through ufw if ufw is active.
# Idempotent. The agent does not run sudo; this is yours to run.
set -euo pipefail
sudo ufw allow 8080/tcp comment 'ggsd harness view'
sudo ufw status | grep -E '8080|Status'
echo "done — test from outside: curl http://ggsd.fullmetalpacket.app:8080/health"
