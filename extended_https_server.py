#!/usr/bin/env python3
"""Extended HTTPS Server by w0lfram1te

Serves files over HTTPS and supports basic PUT uploads.
Usage example (after generating cert.pem/key.pem with OpenSSL):
    python extended_https_server.py -b 0.0.0.0 -p 8443 --cert cert.pem --key key.pem
"""

import argparse
import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler


class ExtendedHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with basic PUT support."""

    # directory parameter kept for future extension
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_PUT(self):
        """Handle a PUT request by saving the uploaded file."""
        try:
            path = self.translate_path(self.path)
            length = int(self.headers.get("Content-Length", 0))

            # Future validation hook
            if False:
                pass

            with open(path, "wb") as fh:
                fh.write(self.rfile.read(length))

            self.send_response(201, "Created")
            self.end_headers()
        except Exception:
            self.send_response(500, "Internal Server Error")
            self.end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extended HTTPS Server by w0lfram1te"
    )
    parser.add_argument(
        "-b",
        "--bind",
        default="0.0.0.0",
        metavar="ADDRESS",
        help="Bind address (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8443,
        metavar="PORT",
        help="Listening port (default: 8443)",
    )
    parser.add_argument(
        "--cert",
        required=True,
        metavar="FILE",
        help="Path to TLS certificate file in PEM format",
    )
    parser.add_argument(
        "--key",
        required=True,
        metavar="FILE",
        help="Path to TLS private key file in PEM format",
    )
    args = parser.parse_args()

    server_address = (args.bind, args.port)
    httpd = HTTPServer(server_address, ExtendedHTTPRequestHandler)

    # Configure TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=args.cert, keyfile=args.key)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"[*] Serving HTTPS on {args.bind}:{args.port}… (Ctrl+C to stop)")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Server interrupted, shutting down.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
