import subprocess
import urllib.request
import json
import time
import os
import shutil

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
port = 9333
profile_dir = os.path.abspath("scratch/temp_edge_debug")
if os.path.exists(profile_dir):
    shutil.rmtree(profile_dir, ignore_errors=True)

cmd = [
    edge,
    "--headless",
    "--disable-gpu",
    f"--remote-debugging-port={port}",
    f"--user-data-dir={profile_dir}",
    "http://localhost:8000"
]

proc = subprocess.Popen(cmd)
time.sleep(2)

try:
    req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
    targets = json.loads(req.read().decode())
    print("Edge targets:", len(targets))
    page = next(t for t in targets if t.get("type") == "page")
    print("Page URL:", page.get("url"))
    ws_url = page.get("webSocketDebuggerUrl")
    print("WS:", ws_url)
finally:
    proc.terminate()
