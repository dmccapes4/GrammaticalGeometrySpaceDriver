#!/usr/bin/env bash
# run_ai_probe.sh
# Run FullMetalPacket/ai_probe against MorphGNT with custom config.
# Output goes to: morphgnt/probe_output/
# Usage: bash morphgnt/run_ai_probe.sh
# Must be run from GrammaticalGeometrySpaceDriver/ root.

set -euo pipefail

GGSD_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MORPHGNT_DIR="$GGSD_ROOT/morphgnt"
FMP_ROOT="/home/dylanmccapes/dev/PORTAL_VISION_LUCIFER/FullMetalPacket"
PROBE_DIR="$FMP_ROOT/ai_probe"
PYTHON="$FMP_ROOT/.PacketForge/bin/python"
OUTPUT_DIR="$MORPHGNT_DIR/probe_output"
INDEX_DIR="$MORPHGNT_DIR/probe_index"
CUSTOM_CONFIG="$MORPHGNT_DIR/ai_probe_morphgnt_config.yaml"
ORIG_CONFIG="$PROBE_DIR/config.yaml"
BACKUP_CONFIG="$PROBE_DIR/config.yaml.ggsd_backup"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$INDEX_DIR"

echo "========================================"
echo "MorphGNT ai_probe — Bias & Fidelity Run"
echo "Target:  $MORPHGNT_DIR"
echo "Output:  $OUTPUT_DIR"
echo "Started: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
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
export AI_PROBE_REPO_ROOT="$MORPHGNT_DIR"
export AI_PROBE_INDEX_PATH="$INDEX_DIR/embeddings.json"
export PYTHONPATH="$FMP_ROOT:$PROBE_DIR:$PYTHONPATH"

cd "$PROBE_DIR"

# ── Phase 1: Embed ──────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 1: embed_repo"
"$PYTHON" embed_repo.py --root "$MORPHGNT_DIR"
# embed_repo writes to ai_probe_index/ under FMP — copy to our index dir
if [ -f "$FMP_ROOT/ai_probe_index/embeddings.json" ]; then
    cp "$FMP_ROOT/ai_probe_index/embeddings.json" "$INDEX_DIR/embeddings.json"
    echo "  Copied embeddings → $INDEX_DIR/embeddings.json"
fi

# ── Phase 2: TS Search ──────────────────────────────────────────────────────
echo ""
echo "▶ Phase 2: ts_search"
"$PYTHON" ts_search.py "$MORPHGNT_DIR" \
    --scope-git-root "$MORPHGNT_DIR"

# ── Phase 3: Probe ──────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 3: probe_agent"
"$PYTHON" probe_agent.py \
    --index "$INDEX_DIR/embeddings.json" \
    --ts "$OUTPUT_DIR/ts_hits.json" \
    --scope-git-root "$MORPHGNT_DIR"

# ── Phase 4: Gap ────────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 4: gap_agent"
"$PYTHON" gap_agent.py \
    --scope-git-root "$MORPHGNT_DIR"

# ── Phase 5: Report ─────────────────────────────────────────────────────────
echo ""
echo "▶ Phase 5: report_agent"
"$PYTHON" report_agent.py

echo ""
echo "========================================"
echo "Done: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "Report: $OUTPUT_DIR/"
echo "========================================"
