# Extended Python Server

This project extends the basic functionality of Python 3’s built‑in `http.server` module, adding **PUT** support and an optional **HTTPS/TLS** wrapper for quick, lab‑style file sharing.

Currently supported methods: `GET`, `HEAD`, and `PUT`.

For extra context and payload ideas, see [https://w0lfram1te.com/python-http-server-with-put-support](https://w0lfram1te.com/python-http-server-with-put-support).

---

## Usage (HTTP‑only)

```
usage: ehttpserver.py [-h] [-b BIND] [-p PORT] [port]

Extended HTTP Server by w0lfram1te

positional arguments:
  port                  listening port

optional arguments:
  -h, --help            show this help message and exit
  -b BIND, --bind BIND  bind address
  -p PORT, --port PORT  listening port
```

Quick start – download and run on port 8000, listening on all interfaces:

```bash
wget https://raw.githubusercontent.com/w0lfram1te/extended-http-server/main/ehttpserver.py
python3 ehttpserver.py
```

---

## TLS / HTTPS Quick Start

`extended_https_server.py` is a drop‑in wrapper that speaks HTTPS. You supply a certificate/key pair and it handles the TLS handshake for you.

### 1. Generate a self‑signed cert (lab / CTF)

```bash
# One‑liner: key.pem + cert.pem valid for 365 days, CN = localhost
openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
        -keyout key.pem -out cert.pem \
        -subj "/CN=localhost"

# Launch HTTPS server on :8443
python extended_https_server.py \
       --cert cert.pem --key key.pem \
       --bind 0.0.0.0 --port 8443
```

*Visit [https://localhost:8443/](https://localhost:8443/) (ignore browser warnings) or upload with:*

```bash
curl -k -T file.txt https://localhost:8443/file.txt
```

### 2. Use a Let’s Encrypt certificate (production‑ish)

```bash
# Obtain cert with Certbot (stand‑alone mode shown here)
sudo certbot certonly --standalone -d example.com

# Run the server with the renewed symlinks
sudo python extended_https_server.py \
     --cert /etc/letsencrypt/live/example.com/fullchain.pem \
     --key  /etc/letsencrypt/live/example.com/privkey.pem \
     --bind 0.0.0.0 --port 8443
```

* `fullchain.pem` includes the intermediate CA, maximizing client compatibility.
* The symlinks in `/etc/letsencrypt/live/` are updated automatically at each renewal; just reload or restart the server so the new cert is picked up.

---

## PUT upload examples

### PowerShell 7

```powershell
Invoke-WebRequest -Method PUT -Uri "https://example.com:8443/test.txt" \
    -Body (Get-Content -Raw .\test.txt) -SkipCertificateCheck
```

### Python requests (ignore cert warning)

```python
import requests, urllib3, pathlib
urllib3.disable_warnings()
requests.put(
    'https://example.com:8443/test.txt',
    data=pathlib.Path('test.txt').read_bytes(),
    verify=False
)
```

Happy hacking! ⚡

