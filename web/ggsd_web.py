#!/usr/bin/env python3
"""
ggsd_web.py — GGSD harness view for hilarious_marcupial (245).

Stdlib only. No sudo, no pip. Serves:
  /                harness view (temperature first, progress, log tail)
  /runs            every completed verse run, newest format aware
  /runs/<slug>     one run: report.md + decoding summary
  /runs/<slug>/decoding.json   raw decoding JSON
  /health          hardware health (HTML; ?format=json for JSON)
  /api/snapshot    harness_view/v0.1 snapshot (LineGuard protocol, ACA)
  /api/health      hardware health JSON
  /api/progress    runs/matthew_full/progress.json passthrough

Reads ~/ggsd/runs (GGSD_RUNS override). Binds 127.0.0.1 by default;
deploy on 245 uses --host 0.0.0.0 --port 8080 behind the UDM forward.
Optional basic auth: GGSD_WEB_USER / GGSD_WEB_PASS env vars.
"""
from __future__ import annotations

import base64
import glob
import html
import json
import os
import re
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

GGSD_DIR = Path(os.environ.get("GGSD_DIR", Path(__file__).resolve().parent.parent))
RUNS = Path(os.environ.get("GGSD_RUNS", GGSD_DIR / "runs"))
FULL = RUNS / "matthew_full_v004" if (RUNS / "matthew_full_v004").exists() else RUNS / "matthew_full"
CACHE: dict = {"ts": 0.0, "health": None}
SLUG_RE = re.compile(r"^Matthew_\d+_\d+_\d{8}T\d{6}Z$")

CSS = """
body{background:#0d1117;color:#e6edf3;font-family:ui-monospace,Menlo,monospace;
margin:2rem auto;max-width:960px;padding:0 1rem;line-height:1.45}
a{color:#58a6ff}h1{font-size:1.3rem}h2{font-size:1.05rem;margin-top:2rem}
.temp{font-size:3.2rem;font-weight:700}.ok{color:#3fb950}.warn{color:#d29922}.bad{color:#f85149}
.bar{background:#21262d;height:18px;border-radius:6px;overflow:hidden}
.bar>div{background:#3fb950;height:100%}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #21262d;
padding:.3rem .5rem;text-align:left;font-size:.85rem}
pre{background:#161b22;padding:1rem;overflow:auto;border-radius:6px;font-size:.8rem}
.mut{color:#8b949e}.card{border:1px solid #21262d;border-radius:8px;padding:1rem;margin:.6rem 0}
"""


def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def health() -> dict:
    if time.time() - CACHE["ts"] < 5 and CACHE["health"]:
        return CACHE["health"]
    h: dict = {"host": "hilarious_marcupial (245)", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw",
             "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=8).stdout.strip()
        n, t, u, mu, mt, pw = [x.strip() for x in out.split(",")]
        h["gpu"] = {"name": n, "temp_c": float(t), "util_pct": float(u),
                    "mem_used_mib": float(mu), "mem_total_mib": float(mt), "power_w": float(pw)}
    except Exception as e:
        h["gpu"] = {"error": str(e)}
    try:
        with open("/proc/meminfo") as f:
            mem = dict((k, int(v.split()[0])) for k, v in
                       (line.split(":", 1) for line in f if ":" in line))
        h["ram"] = {"used_pct": round(100 * (1 - mem["MemAvailable"] / mem["MemTotal"]), 1),
                    "total_gib": round(mem["MemTotal"] / 1048576, 1)}
        h["load1"] = round(os.getloadavg()[0], 2)
        h["cpus"] = os.cpu_count()
    except Exception as e:
        h["ram"] = {"error": str(e)}
    try:
        st = os.statvfs(RUNS)
        h["disk_runs"] = {"free_gib": round(st.f_bavail * st.f_frsize / 2**30, 1),
                          "total_gib": round(st.f_blocks * st.f_frsize / 2**30, 1)}
    except Exception:
        pass
    try:
        r = subprocess.run(["curl", "-s", "-m", "3", "http://127.0.0.1:11434/api/tags"],
                           capture_output=True, text=True, timeout=5)
        h["ollama"] = "up" if r.returncode == 0 and r.stdout else "down"
    except Exception:
        h["ollama"] = "down"
    try:
        r = subprocess.run(["pgrep", "-af", "run_matthew.py"], capture_output=True, text=True, timeout=5)
        h["ggsd_run"] = {"alive": bool(r.stdout.strip()),
                         "cmd": r.stdout.strip().splitlines()[0] if r.stdout.strip() else None}
    except Exception:
        h["ggsd_run"] = {"alive": None}
    # CPU temperature: report only what the kernel exposes; never invent it.
    temps = []
    for z in sorted(glob.glob("/sys/class/thermal/thermal_zone*/temp")):
        try:
            temps.append(int(Path(z).read_text().strip()) / 1000.0)
        except Exception:
            pass
    h["cpu_temp_c"] = max(temps) if temps else None
    h["cpu_temp_note"] = None if temps else "not exposed by kernel on this host; GPU temp is the measured one"
    CACHE.update(ts=time.time(), health=h)
    return h


def progress() -> dict:
    return _read_json(FULL / "progress.json") or {"n_done": 0, "n_total": 1071, "status": "unknown"}


def completed_refs() -> list[str]:
    c = _read_json(FULL / "completed.json")
    return c if isinstance(c, list) else []


def error_count() -> int:
    p = FULL / "errors.jsonl"
    try:
        return sum(1 for _ in p.open(encoding="utf-8"))
    except Exception:
        return 0


def log_tail(n: int = 25) -> list[str]:
    logs = sorted(GGSD_DIR.glob("ggsd_matthew*.log"), key=lambda p: p.stat().st_mtime)
    if not logs:
        return []
    try:
        return logs[-1].read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    except Exception:
        return []


def snapshot() -> dict:
    """harness_view/v0.1 (LineGuard HARNESS_VIEW_PROTOCOL, via ACA)."""
    p, h = progress(), health()
    done, total = p.get("n_done", 0), p.get("n_total", 1071)
    rate = p.get("rate_verses_per_hour")
    eta_s = None
    if rate:
        eta_s = int((total - done) / rate * 3600)
    gpu = h.get("gpu", {})
    return {
        "protocol": "harness_view/v0.1", "host": "245", "arm": "ggsd_matthew",
        "stage": "decode", "label": "245 · GGSD Matthew (Qwen3-30B)",
        "alive": bool(h.get("ggsd_run", {}).get("alive")),
        "started_ts": p.get("started_utc"), "now_ts": h["ts"],
        "target": total, "done": done, "unit": "verses",
        "rate_per_h": rate, "eta_s": eta_s,
        "artifact": str(FULL / "completed.json"),
        "log": str(GGSD_DIR / "ggsd_matthew_v004.log"),
        "metrics": {"errors": error_count(),
                    "gpu_temp_c": gpu.get("temp_c"), "gpu_util_pct": gpu.get("util_pct"),
                    "current_verse": p.get("current_verse"), "status": p.get("status")},
        "last": {"id": p.get("current_verse"), "preview": log_tail(3)},
        "log_tail": log_tail(10), "notes": [],
    }


def list_runs() -> list[dict]:
    out = []
    for d in RUNS.glob("Matthew_*_*"):
        if not d.is_dir():
            continue
        meta = _read_json(d / "run_meta.json") or {}
        dec = d / "verse_grammatical_decoding.json"
        gates = None
        if dec.exists():
            dj = _read_json(dec)
            if dj and "gates" in dj:
                gates = len(dj["gates"])
        out.append({"slug": d.name, "verse_ref": meta.get("verse_ref", d.name),
                    "model": (meta.get("model_id") or "").replace("ollama/", ""),
                    "driver": meta.get("driver_version"), "words": meta.get("word_count"),
                    "finished": meta.get("finished_at"), "gates": gates,
                    "has_report": (d / "report.md").exists()})
    def key(r):
        m = re.match(r"Matthew_(\d+)_(\d+)_", r["slug"])
        return (int(m.group(1)), int(m.group(2))) if m else (99, 99)
    return sorted(out, key=key)


def page(title: str, body: str, refresh: bool = False) -> bytes:
    meta = '<meta http-equiv="refresh" content="30">' if refresh else ""
    return (f"<!doctype html><html><head><meta charset=utf-8>{meta}"
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head>"
            f"<body>{body}<p class=mute></p><p class=mute>"
            f"<a href=/>harness</a> · <a href=/runs>runs</a> · <a href=/health>health</a> · "
            f"<a href=/api/snapshot>snapshot json</a></p></body></html>").encode()


STATS_CACHE: dict = {"ts": 0.0, "stats": None}


def run_stats() -> dict:
    """Aggregate stats over per-verse run dirs (cached 30 s)."""
    if time.time() - STATS_CACHE["ts"] < 30 and STATS_CACHE["stats"]:
        return STATS_CACHE["stats"]
    runs = list_runs()
    by_slug: dict[str, dict] = {}
    for r in runs:  # latest dir per verse wins (list sorted by verse, then name)
        by_slug[r["verse_ref"]] = r
    latest = sorted(by_slug.values(),
                    key=lambda r: str(r.get("finished") or ""), reverse=True)
    chapters: dict[int, int] = {}
    for ref in completed_refs():
        m = re.match(r"Matthew (\d+):", ref)
        if m:
            chapters[int(m.group(1))] = chapters.get(int(m.group(1)), 0) + 1
    stats = {
        "last20": latest[:20],
        "run_dirs": len(runs),
        "verses_with_runs": len(by_slug),
        "words": sum(r.get("words") or 0 for r in by_slug.values()),
        "gates_003": sum(r["gates"] for r in by_slug.values() if r.get("gates") is not None),
        "verses_003": sum(1 for r in by_slug.values() if r.get("gates") is not None),
        "chapters": chapters,
        "current_chapter": max(chapters) if chapters else None,
    }
    STATS_CACHE.update(ts=time.time(), stats=stats)
    return stats


def home() -> bytes:
    p, h, s = progress(), health(), snapshot()
    st = run_stats()
    gpu = h.get("gpu", {})
    t = gpu.get("temp_c")
    cls = "ok" if t is not None and t < 75 else ("warn" if t is not None and t < 85 else "bad")
    done, total = p.get("n_done", 0), p.get("n_total", 1071)
    pct = round(100 * done / total, 1) if total else 0
    tail = "\n".join(html.escape(x) for x in log_tail(25))
    last_rows = "".join(
        f"<tr><td><a href=/runs/{r['slug']}>{html.escape(str(r['verse_ref']))}</a></td>"
        f"<td>{r['words'] or ''}</td><td>{'—' if r['gates'] is None else r['gates']}</td>"
        f"<td>{html.escape(str(r['driver'] or ''))}</td>"
        f"<td>{html.escape(str(r['finished'] or ''))}</td></tr>" for r in st["last20"])
    chap = " · ".join(f"{c}:{n}" for c, n in sorted(st["chapters"].items()))
    started = str(p.get("started_utc") or "")
    body = f"""
<h1>GGSD · harness view — hilarious_marcupial</h1>
<div class=card><div class=temp><span class={cls}>{t if t is not None else '?'}°C</span>
<span style="font-size:1rem" class=mute>GPU {html.escape(str(gpu.get('name','')))} ·
util {gpu.get('util_pct','?')}% · mem {gpu.get('mem_used_mib','?')}/{gpu.get('mem_total_mib','?')} MiB ·
{gpu.get('power_w','?')} W · RAM used {h.get('ram',{}).get('used_pct','?')}% ·
disk free {h.get('disk_runs',{}).get('free_gib','?')} GiB · load {h.get('load1','?')}</span></div></div>
<div class=card><b>{done} / {total} verses ({pct}%)</b> — {html.escape(str(p.get('status')))}
<div class=bar><div style="width:{pct}%"></div></div>
<p>current: <b>{html.escape(str(p.get('current_verse')))}</b> ·
rate {p.get('rate_verses_per_hour')} v/h · ETA {p.get('eta_hours')} h ·
model {html.escape(str(p.get('model','')).replace('ollama/',''))} · driver 0.0.4 ·
started {html.escape(started)} · updated {html.escape(str(p.get('updated_utc','')))}</p>
<p>run process {'<span class=ok>ALIVE</span>' if s['alive'] else '<span class=bad>NOT ALIVE</span>'} ·
ollama {h.get('ollama')} · verse errors logged {error_count()}</p></div>
<div class=card><h2 style="margin-top:0">stats</h2>
<p>words decoded (latest run per verse): <b>{st['words']:,}</b> ·
gates in current decodings: <b>{st['gates_003']}</b> across {st['verses_003']} verses ·
run dirs on disk {st['run_dirs']} · verses with runs {st['verses_with_runs']}</p>
<p class=mute>chapters completed (chapter:verses) — {html.escape(chap)}</p></div>
<div class=card><h2 style="margin-top:0">last 20 runs</h2>
<table><tr><th>verse</th><th>words</th><th>gates</th><th>driver</th><th>finished (UTC)</th></tr>
{last_rows}</table>
<p class=mute>all runs: <a href=/runs>/runs</a> · hardware: <a href=/health>/health</a></p></div>
<h2>log tail</h2><pre>{tail}</pre>"""
    return page("GGSD harness — 245", body, refresh=True)


def runs_page() -> bytes:
    rows = list_runs()
    done = set(completed_refs())
    trs = ""
    for r in rows:
        g = "—" if r["gates"] is None else str(r["gates"])
        trs += (f"<tr><td><a href=/runs/{r['slug']}>{html.escape(str(r['verse_ref']))}</a></td>"
                f"<td>{'✓' if r['verse_ref'] in done else ''}</td><td>{r['words'] or ''}</td>"
                f"<td>{g}</td><td>{html.escape(str(r['driver'] or ''))}</td>"
                f"<td>{html.escape(str(r['finished'] or ''))}</td></tr>")
    body = (f"<h1>GGSD runs — {len(rows)} verse runs on disk</h1>"
            f"<p class=mute>gate counts appear for driver 0.0.4 runs; earlier runs predate "
            f"the punctuation layer (deterministic backfill still owed).</p>"
            f"<table><tr><th>verse</th><th>done</th><th>words</th><th>gates</th>"
            f"<th>driver</th><th>finished (UTC)</th></tr>{trs}</table>")
    return page("GGSD runs", body)


def run_page(slug: str):
    if not SLUG_RE.match(slug):
        return None
    d = RUNS / slug
    if not d.is_dir():
        return None
    meta = _read_json(d / "run_meta.json") or {}
    dec = _read_json(d / "verse_grammatical_decoding.json") or {}
    report = ""
    rp = d / "report.md"
    if rp.exists():
        report = rp.read_text(encoding="utf-8", errors="replace")
    gates = dec.get("gates")
    gate_html = ""
    if gates is not None:
        gate_html = "<h2>gates</h2><pre>" + html.escape(json.dumps(gates, ensure_ascii=False, indent=1)) + "</pre>"
    body = (f"<h1>{html.escape(str(meta.get('verse_ref', slug)))}</h1>"
            f"<p class=mute>model {html.escape(str(meta.get('model_id')))} · driver "
            f"{html.escape(str(meta.get('driver_version')))} · words {meta.get('word_count')} · "
            f"<a href=/runs/{slug}/decoding.json>decoding json</a></p>"
            f"{gate_html}<h2>report</h2><pre>{html.escape(report)}</pre>")
    return page(slug, body)


def health_page() -> bytes:
    h = health()
    gpu = h.get("gpu", {})
    rows = "".join(f"<tr><td>{html.escape(str(k))}</td><td>{html.escape(json.dumps(v, ensure_ascii=False))}</td></tr>"
                   for k, v in h.items())
    t = gpu.get("temp_c")
    cls = "ok" if t is not None and t < 75 else ("warn" if t is not None and t < 85 else "bad")
    body = (f"<h1>health — hilarious_marcupial</h1>"
            f"<div class=temp><span class={cls}>{t if t is not None else '?'}°C</span> "
            f"<span style='font-size:1rem' class=mute>GPU</span></div>"
            f"<p class=mute>CPU temp: {h.get('cpu_temp_c') if h.get('cpu_temp_c') is not None else html.escape(str(h.get('cpu_temp_note')))}</p>"
            f"<table>{rows}</table><p class=mute>JSON: <a href=/api/health>/api/health</a></p>")
    return page("245 health", body, refresh=True)


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _auth_ok(self) -> bool:
        u, pw = os.environ.get("GGSD_WEB_USER"), os.environ.get("GGSD_WEB_PASS")
        if not u:
            return True
        got = self.headers.get("Authorization", "")
        try:
            dec = base64.b64decode(got.split(" ", 1)[1]).decode()
        except Exception:
            return False
        return dec == f"{u}:{pw}"

    def _send(self, code: int, body: bytes, ctype: str = "text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj):
        self._send(200, json.dumps(obj, ensure_ascii=False, indent=1).encode(),
                   "application/json; charset=utf-8")

    def do_GET(self):
        if not self._auth_ok():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="ggsd"')
            self.end_headers()
            return
        path = urlparse(self.path).path.rstrip("/") or "/"
        qs = parse_qs(urlparse(self.path).query)
        try:
            if path == "/":
                self._send(200, home())
            elif path == "/runs":
                self._send(200, runs_page())
            elif path.startswith("/runs/") and path.endswith("/decoding.json"):
                slug = path.split("/")[2]
                if SLUG_RE.match(slug) and (RUNS / slug / "verse_grammatical_decoding.json").exists():
                    self._send(200, (RUNS / slug / "verse_grammatical_decoding.json").read_bytes(),
                               "application/json; charset=utf-8")
                else:
                    self._send(404, b"not found")
            elif path.startswith("/runs/"):
                b = run_page(path.split("/")[2])
                self._send(200, b) if b else self._send(404, b"not found")
            elif path == "/health":
                self._json(health()) if qs.get("format") == ["json"] else self._send(200, health_page())
            elif path == "/api/health":
                self._json(health())
            elif path == "/api/snapshot":
                self._json(snapshot())
            elif path == "/api/progress":
                self._json(progress())
            else:
                self._send(404, b"not found")
        except Exception as e:
            self._send(500, f"error: {html.escape(str(e))}".encode())


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    print(f"ggsd_web on {args.host}:{args.port} runs={RUNS}", flush=True)
    ThreadingHTTPServer((args.host, args.port), H).serve_forever()
