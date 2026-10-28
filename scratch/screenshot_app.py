import subprocess
import os

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html = os.path.abspath("frontend/index.html")
png = os.path.abspath("scratch/app_header.png")

file_url = "file:///" + html.replace("\\", "/")

cmd = [
    edge,
    "--headless",
    "--disable-gpu",
    "--window-size=1280,800",
    f"--screenshot={png}",
    file_url
]

subprocess.run(cmd, capture_output=True)
print("Screenshot exists:", os.path.exists(png))
