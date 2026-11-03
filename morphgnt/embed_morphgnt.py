#!/usr/bin/env python3
"""
embed_morphgnt.py — Custom embedder for MorphGNT bias/fidelity analysis.

Replaces FullMetalPacket/ai_probe/embed_repo.py for this target.
FMP's embed_repo.py only handles .kt/.java/.xml (Android); MorphGNT has
.py, .yaml, .md, and small .txt lexicon files.

Skips:
  - Large NT data files in sblgnt/ and python/pysblgnt/sblgnt/ (≥1000 lines)
  - Binary, compiled, venv files
  - probe_output/ and probe_index/ dirs

Output: probe_index/embeddings.json  (same schema as FMP embed_repo.py)
"""

import os, json, time, argparse
from pathlib import Path
from openai import OpenAI, APIError, RateLimitError

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

SKIP_DIRS = {
    ".git", "__pycache__", ".pytest_cache", ".venv", "venv", "probe_output",
    "probe_index", "build", "dist", "node_modules", ".tox",
}

SKIP_EXTENSIONS = {
    ".pyc", ".pyo", ".so", ".zip", ".tar", ".gz", ".png", ".jpg", ".pdf",
    ".lock", ".DS_Store", ".env", ".bin",
}

EMBED_EXTENSIONS = {".py", ".yaml", ".yml", ".md", ".txt", ".rst", ".toml", ".cfg", ".ini"}

# Skip large NT data files — they contain tokenized text, not methodology.
# Files with these patterns in their path + ≥1000 lines are skipped.
NT_DATA_PATTERN = "-morphgnt.txt"

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150


def should_skip_file(path: str, content_line_count: int) -> bool:
    basename = os.path.basename(path)
    if NT_DATA_PATTERN in basename and content_line_count >= 1000:
        return True
    return False


def iter_files(root: str):
    for dirpath, dirnames, files in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in EMBED_EXTENSIONS:
                continue
            if ext in SKIP_EXTENSIONS:
                continue
            yield os.path.join(dirpath, fname)


def main():
    parser = argparse.ArgumentParser(description="Embed MorphGNT for ai_probe.")
    parser.add_argument("root", help="MorphGNT directory to embed")
    parser.add_argument("--out", default=None, help="Output dir (default: <root>/../probe_index)")
    parser.add_argument("--model", default="text-embedding-3-small")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if args.out:
        out_dir = os.path.abspath(args.out)
    else:
        out_dir = os.environ.get(
            "AI_PROBE_INDEX_DIR",
            os.path.join(root, "..", "probe_index")
        )
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    outfile = os.path.join(out_dir, "embeddings.json")

    client = OpenAI()
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    # Resume
    vectors = []
    if os.path.exists(outfile):
        try:
            vectors = json.load(open(outfile))
            print(f"🟡 Resuming from {len(vectors)} saved embeddings.")
        except Exception:
            print("⚠️  Could not load existing embeddings. Starting fresh.")
            vectors = []

    # Build corpus
    corpus = []
    skipped_large = []
    for fpath in iter_files(root):
        try:
            text = open(fpath, encoding="utf-8", errors="ignore").read()
        except Exception as e:
            print(f"⚠️  Skipping {fpath}: {e}")
            continue

        line_count = text.count("\n")
        if should_skip_file(fpath, line_count):
            skipped_large.append(fpath)
            continue

        # Make path relative to root for consistent keys
        rel_path = os.path.relpath(fpath, root)
        for chunk in splitter.split_text(text):
            corpus.append({"path": rel_path, "text": chunk})

    print(f"Files skipped (large NT data): {len(skipped_large)}")
    print(f"Total chunks to embed: {len(corpus)}")

    start_idx = len(vectors)
    batch_size = 64

    for i in range(start_idx, len(corpus), batch_size):
        batch = corpus[i : i + batch_size]
        retry = 0
        while True:
            try:
                resp = client.embeddings.create(
                    model=args.model,
                    input=[c["text"] for c in batch],
                )
                for c, e in zip(batch, resp.data):
                    c["embedding"] = e.embedding
                    vectors.append(c)
                break
            except RateLimitError:
                wait = 5 * (2 ** retry)
                print(f"⏳ Rate limit, sleeping {wait}s (attempt {retry + 1})...")
                time.sleep(wait)
                retry += 1
                if retry > 5:
                    print("❌ Too many retries; aborting batch.")
                    break
            except APIError as e:
                print(f"⚠️  API error: {e}. Retrying in 10s...")
                time.sleep(10)
                retry += 1

        # Periodic checkpoint
        if i % 640 < batch_size:
            json.dump(vectors, open(outfile, "w"), indent=2)
            print(f"   checkpoint: {len(vectors)} embeddings saved")

    json.dump(vectors, open(outfile, "w"), indent=2)
    print(f"✅ Saved {len(vectors)} embeddings → {outfile}")


if __name__ == "__main__":
    main()
