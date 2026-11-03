#!/usr/bin/env bash
# run_ai_probe.sh — MorphGNT bias/fidelity probe
# Runs FullMetalPacket/ai_probe stages against MorphGNT vendor dir.
# Uses embed_morphgnt.py (custom) instead of embed_repo.py (Android-only).
# Run from GrammaticalGeometrySpaceDriver root:
#   bash morphgnt/run_ai_probe.sh

set -euo pipefail

GGSD_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MORPHGNT_DIR="$GGSD_ROOT/morphgnt"
FMP_ROOT="/home/dylanmccapes/dev/PORTAL_VISION_LUCIFER/FullMetalPacket"
PROBE_DIR="$FMP_ROOT/ai_probe"
PYTHON="$MORPHGNT_DIR/probe_venv/bin/python"  # Linux venv; .PacketForge is a dead macOS venv
OUTPUT_DIR="$MORPHGNT_DIR/probe_output"
INDEX_DIR="$MORPHGNT_DIR/probe_index"
CUSTOM_CONFIG="$MORPHGNT_DIR/ai_probe_morphgnt_config.yaml"
ORIG_CONFIG="$PROBE_DIR/config.yaml"
BACKUP_CONFIG="$PROBE_DIR/config.yaml.ggsd_backup"

mkdir -p "$OUTPUT_DIR" "$INDEX_DIR"

echo "========================================"
echo "MorphGNT ai_probe — Bias & Fidelity Run"
echo "GGSD root: $GGSD_ROOT"
echo "Target:    $MORPHGNT_DIR"
echo "Output:    $OUTPUT_DIR"
echo "Started:   $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "========================================"

# Swap config
cp "$ORIG_CONFIG" "$BACKUP_CONFIG"
cp "$CUSTOM_CONFIG" "$ORIG_CONFIG"

restore_config() {
    echo "Restoring original config.yaml..."
    cp "$BACKUP_CONFIG" "$ORIG_CONFIG"
    rm -f "$BACKUP_CONFIG"
}
trap restore_config EXIT

# Export env vars that ai_probe pipeline reads
export AI_PROBE_OUTPUT_DIR="$OUTPUT_DIR"
export AI_PROBE_REPO_ROOT="$GGSD_ROOT"          # git root for path scoping
export AI_PROBE_INDEX_PATH="$INDEX_DIR/embeddings.json"
export PYTHONPATH="$FMP_ROOT:$PROBE_DIR:${PYTHONPATH:-}"

# ── Phase 1: Embed ──────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 1: embed_morphgnt (custom embedder)"
"$PYTHON" "$MORPHGNT_DIR/embed_morphgnt.py" \
    "$MORPHGNT_DIR" \
    --out "$INDEX_DIR"

# ── Phase 2: TS Search ──────────────────────────────────────────────────────
echo ""
echo "▶ Phase 2: ts_search"
cd "$PROBE_DIR"
"$PYTHON" ts_search.py "$GGSD_ROOT" \
    --scope-git-root "$GGSD_ROOT"

# ── Phase 3: Probe ──────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 3: probe_agent"
"$PYTHON" probe_agent.py \
    --index "$INDEX_DIR/embeddings.json" \
    --ts "$OUTPUT_DIR/ts_hits.json" \
    --scope-git-root "$GGSD_ROOT"

# ── Phase 4: Gap ────────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 4: gap_agent"
"$PYTHON" gap_agent.py \
    --scope-git-root "$GGSD_ROOT"

# ── Phase 5: Report ─────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 5: report_agent"
"$PYTHON" report_agent.py

echo ""
echo "========================================"
echo "Done: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "Report output: $OUTPUT_DIR/"
echo "========================================"
