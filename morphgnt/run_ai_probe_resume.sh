#!/usr/bin/env bash
# run_ai_probe_resume.sh — Resume from Phase 2 (embeddings already done)
# Run from GrammaticalGeometrySpaceDriver root:
#   bash morphgnt/run_ai_probe_resume.sh

set -euo pipefail

GGSD_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MORPHGNT_DIR="$GGSD_ROOT/morphgnt"
FMP_ROOT="/home/dylanmccapes/dev/PORTAL_VISION_LUCIFER/FullMetalPacket"
PROBE_DIR="$FMP_ROOT/ai_probe"
PYTHON="$MORPHGNT_DIR/probe_venv/bin/python"
OUTPUT_DIR="$MORPHGNT_DIR/probe_output"
INDEX_DIR="$MORPHGNT_DIR/probe_index"
CUSTOM_CONFIG="$MORPHGNT_DIR/ai_probe_morphgnt_config.yaml"
ORIG_CONFIG="$PROBE_DIR/config.yaml"
BACKUP_CONFIG="$PROBE_DIR/config.yaml.ggsd_backup"

mkdir -p "$OUTPUT_DIR" "$INDEX_DIR"

echo "========================================"
echo "MorphGNT ai_probe — Resume from Phase 2"
echo "GGSD root: $GGSD_ROOT"
echo "Embeddings: $(wc -c < "$INDEX_DIR/embeddings.json") bytes ready"
echo "Resumed:   $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
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

export AI_PROBE_OUTPUT_DIR="$OUTPUT_DIR"
export AI_PROBE_REPO_ROOT="$GGSD_ROOT"
export AI_PROBE_INDEX_PATH="$INDEX_DIR/embeddings.json"
export PYTHONPATH="$FMP_ROOT:$PROBE_DIR:${PYTHONPATH:-}"

cd "$PROBE_DIR"

# ── Phase 2: TS Search ──────────────────────────────────────────────────────
echo ""
echo "▶ Phase 2: ts_search"
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
echo "========================================"
