#!/usr/bin/env python3
"""
Folio Web Studio Launcher.
Serves the Folio web application locally and opens your default browser.
Run via: python3 run_web.py
"""
import os
import sys
import socketserver
import http.server
import webbrowser
import socket

DEFAULT_PORT = 5050
WEB_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class FolioHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean logging format
        sys.stdout.write(f"[Folio Web] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


def find_available_port(start_port: int = DEFAULT_PORT) -> int:
    port = start_port
    while port < start_port + 100:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
        port += 1
    return start_port


def main():
    if not os.path.exists(WEB_DIRECTORY):
        print(f"Error: Web directory not found at: {WEB_DIRECTORY}")
        sys.exit(1)

    # Automated verification check mode (does not block server)
    if "--test-check" in sys.argv or "--check" in sys.argv:
        index_file = os.path.join(WEB_DIRECTORY, "index.html")
        editor_file = os.path.join(WEB_DIRECTORY, "editor.html")
        css_file = os.path.join(WEB_DIRECTORY, "static", "css", "styles.css")
        editor_css = os.path.join(WEB_DIRECTORY, "static", "css", "editor.css")
        js_file = os.path.join(WEB_DIRECTORY, "static", "js", "app.js")
        editor_js = os.path.join(WEB_DIRECTORY, "static", "js", "editor.js")
        
        assert os.path.exists(index_file), "index.html must exist"
        assert os.path.exists(editor_file), "editor.html must exist"
        assert os.path.exists(css_file), "styles.css must exist"
        assert os.path.exists(editor_css), "editor.css must exist"
        assert os.path.exists(js_file), "app.js must exist"
        assert os.path.exists(editor_js), "editor.js must exist"
        
        assert os.path.getsize(index_file) > 1000, "index.html has content"
        assert os.path.getsize(editor_file) > 1000, "editor.html has content"
        assert os.path.getsize(css_file) > 1000, "styles.css has content"
        assert os.path.getsize(editor_css) > 1000, "editor.css has content"
        assert os.path.getsize(js_file) > 1000, "app.js has content"
        assert os.path.getsize(editor_js) > 1000, "editor.js has content"
        print("✅ Folio Web & Editor static files verification passed successfully.")
        sys.exit(0)

    port = find_available_port(DEFAULT_PORT)
    url = f"http://localhost:{port}"

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), FolioHTTPRequestHandler) as httpd:
        print("=" * 70)
        print(" ✨ FOLIO — Production-Quality Editorial CV Studio Web Edition")
        print("=" * 70)
        print(f" 🌐 Running at:   {url}")
        print(f" 📁 Serving from: {WEB_DIRECTORY}")
        print(f" ⌨️  Press Ctrl+C to stop the local web server")
        print("=" * 70)

        # Automatically open in browser if not in headless environment
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Folio Web Server gracefully stopped.")


if __name__ == "__main__":
    main()
