import subprocess
import os

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_path = os.path.abspath("frontend/index.html")

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make screen-user-login hidden and app-shell visible
logged_in = content.replace(
    'id="screen-user-login" class="min-h-screen w-full flex items-center justify-center p-4 sm:p-6 bg-[#98b18d] relative"',
    'id="screen-user-login" class="hidden" style="display:none;"'
).replace(
    'id="app-shell" class="min-h-screen flex flex-col flex-1" style="display: none;"',
    'id="app-shell" class="min-h-screen flex flex-col flex-1" style="display: flex;"'
)

temp_file = os.path.abspath("frontend/temp_logged_in.html")
with open(temp_file, "w", encoding="utf-8") as f:
    f.write(logged_in)

out_png = os.path.abspath("scratch/screenshot_main_app_clean.png")
file_url = "file:///" + temp_file.replace("\\", "/")
cmd = [edge, "--headless", "--disable-gpu", "--window-size=1280,950", f"--screenshot={out_png}", file_url]
subprocess.run(cmd, capture_output=True)

if os.path.exists(temp_file):
    os.remove(temp_file)

print("Clean Main App Screenshot exists:", os.path.exists(out_png), out_png)
