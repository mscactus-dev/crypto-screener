#!/usr/bin/env python3
"""
Simple HTTP server for Bitcoin Financial Astrology Web App
"""

import http.server
import socketserver
import json
import subprocess
import os
from urllib.parse import urlparse

PORT = 8000

class AstroHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/run-astro-calc':
            # Run the astrology calculation
            try:
                # Import and run the analysis
                import astro_calc
                result = astro_calc.analyze_bitcoin_astrology()

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error = {'error': str(e)}
                self.wfile.write(json.dumps(error).encode())
        else:
            # Serve static files
            super().do_GET()

if __name__ == '__main__':
    os.chdir('/home/user/crypto-screener')

    with socketserver.TCPServer(("", PORT), AstroHandler) as httpd:
        print("=" * 70)
        print("BITCOIN FINANCIAL ASTROLOGY WEB SERVER")
        print("=" * 70)
        print(f"\nServer running at: http://localhost:{PORT}/")
        print(f"\nOpen this URL in your browser:")
        print(f"  → http://localhost:{PORT}/bitcoin-astrology.html")
        print(f"\nPress Ctrl+C to stop the server")
        print("=" * 70)
        httpd.serve_forever()
