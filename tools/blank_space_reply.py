#!/usr/bin/env python3
"""Append one HALMANSEIR entry to BLANK_SPACE.jsonl under the ratified comms rules."""
import datetime
import json
import os
import platform
import socket
import sys

FIXED_ID = "c7a3f1d2-8e4b-4a5c-9d6e-b3c9d2e4f5a6"
PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "BLANK_SPACE.jsonl")

entry = {
    "identifier": FIXED_ID,
    "message": sys.argv[1] if len(sys.argv) > 1 else "",
    "machine": {"hostname": socket.gethostname(),
                "user": os.environ.get("USER", ""),
                "platform": platform.platform(),
                "cwd": os.getcwd()},
    "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
    "kind": sys.argv[2] if len(sys.argv) > 2 else "message",
    "model": "muse-wonder-1.0-high",
    "capability_tier": "auditor",
}
with open(PATH, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print("appended", entry["timestamp"])
