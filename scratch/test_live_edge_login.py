import subprocess
import urllib.request
import json
import time
import os

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
port = 9222

# Launch Edge headless with remote debugging
cmd = [
    edge,
    "--headless",
    "--disable-gpu",
    f"--remote-debugging-port={port}",
    "http://localhost:8000"
]
proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    # Query targets
    req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
    targets = json.loads(req.read().decode())
    print("Edge targets:", len(targets))
    page = targets[0]
    ws_url = page.get("webSocketDebuggerUrl")
    print("Page URL:", page.get("url"))
    print("WS:", ws_url)
finally:
    proc.terminate()
