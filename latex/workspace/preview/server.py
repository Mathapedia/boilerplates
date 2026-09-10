#!/usr/bin/env python3
"""Static server for `make preview` plus two tiny editor endpoints.

  GET  /api/files          -> JSON list of editable files under tex/
  PUT  /tex/<path>         -> write the file (tex/ only; .tex/.bib/.mmd)

Everything else is plain static serving of the workspace, so the page can
load build/svg/*.svg and build/svg/stamp exactly as before.
"""
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.abspath(os.getcwd())
TEX = os.path.join(ROOT, "tex")
EXTS = (".tex", ".bib", ".mmd")


def editable_files():
    out = []
    for base, _dirs, files in os.walk(TEX):
        for f in files:
            if f.endswith(EXTS):
                out.append(os.path.relpath(os.path.join(base, f), ROOT))
    return sorted(out)


def safe_tex_path(url_path):
    p = os.path.abspath(os.path.join(ROOT, url_path.lstrip("/")))
    if not p.startswith(TEX + os.sep) or not p.endswith(EXTS):
        return None
    return p


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_):  # keep latexmk output readable
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/api/files":
            body = json.dumps(editable_files()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def do_PUT(self):
        target = safe_tex_path(self.path.split("?")[0])
        if target is None:
            self.send_error(403, "only tex/**/*.{tex,bib,mmd} are writable")
            return
        n = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(n)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)
        self.send_response(204)
        self.end_headers()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
