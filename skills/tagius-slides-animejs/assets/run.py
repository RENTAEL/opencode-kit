#!/usr/bin/env python3
"""
Local server launcher for the slides-animejs presentation bundle.
Stdlib only; serves the bundle and opens the browser automatically.
Copied into the built `./presentation/` by `scripts/build.py`.
"""
import http.server
import os
import socketserver
import sys
import threading
import webbrowser

PORT = int(os.environ.get("SLIDES_PORT", 8000))
HOST = "127.0.0.1"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("\r[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def open_browser():
    webbrowser.open(f"http://{HOST}:{PORT}/index.html")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer((HOST, PORT), QuietHandler) as httpd:
        print(f"  slides-animejs serving at  http://{HOST}:{PORT}")
        print("  Ctrl+C to stop.")
        threading.Timer(0.6, open_browser).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped.")
