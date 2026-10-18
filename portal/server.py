# twinops portal - stdlib only, no dependencies.
import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORTAL_PORT", "8080"))
KUMA_URL = os.environ.get("KUMA_URL", "http://127.0.0.1:3001")
KUMA_INTERNAL = os.environ.get("KUMA_INTERNAL", "http://kuma:3001")
TIANJI_URL = os.environ.get("TIANJI_URL", "http://127.0.0.1:12345")
TIANJI_INTERNAL = os.environ.get("TIANJI_INTERNAL", "http://tianji:12345")
ROOT = os.path.dirname(os.path.abspath(__file__))


def probe(url, timeout=2):
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return "online" if r.status < 500 else "degraded"
    except Exception:
        return "offline"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/healthz":
            return self._send(200, "text/plain", b"ok")
        if path == "/api/status":
            payload = json.dumps({
                "kuma": probe(KUMA_INTERNAL),
                "tianji": probe(TIANJI_INTERNAL),
            }).encode()
            return self._send(200, "application/json", payload)
        if path in ("/", ""):
            path = "/index.html"
        safe = os.path.normpath(path).lstrip("/")
        full = os.path.join(ROOT, safe)
        if not full.startswith(ROOT) or not os.path.isfile(full):
            return self._send(404, "text/plain", b"not found")
        ctype = "text/html" if full.endswith(".html") else "text/plain"
        try:
            with open(full, "rb") as f:
                body = f.read()
            if full.endswith(".html"):
                body = body.replace(b"__KUMA_URL__", KUMA_URL.encode()).replace(
                    b"__TIANJI_URL__", TIANJI_URL.encode())
            return self._send(200, ctype, body)
        except OSError:
            return self._send(404, "text/plain", b"not found")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"[twinops] portal on 0.0.0.0:{PORT} | kuma {KUMA_URL} | tianji {TIANJI_URL}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
