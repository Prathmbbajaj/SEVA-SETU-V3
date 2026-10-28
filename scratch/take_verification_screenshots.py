import subprocess
import os
import time

edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_path = os.path.abspath("frontend/index.html")
file_url = "file:///" + html_path.replace("\\", "/")

# 1. Capture the initial Login First Screen
login_png = os.path.abspath("scratch/screenshot_login_screen.png")
cmd1 = [
    edge,
    "--headless",
    "--disable-gpu",
    "--window-size=1280,950",
    f"--screenshot={login_png}",
    file_url
]
subprocess.run(cmd1, capture_output=True)
print("Login Screen Screenshot exists:", os.path.exists(login_png), login_png)

# 2. To capture the main app screen after login, let's create a temporary index_logged_in.html
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make screen-user-login hidden and app-shell visible as if enterMainApp() ran
logged_in_content = content.replace(
    'id="screen-user-login" class="min-h-screen w-full flex items-center justify-center p-4 sm:p-6 bg-[#98b18d] relative"',
    'id="screen-user-login" class="hidden" style="display:none;"'
).replace(
    'id="app-shell" class="min-h-screen flex flex-col flex-1" style="display: none;"',
    'id="app-shell" class="min-h-screen flex flex-col flex-1" style="display: flex;"'
)

temp_html = os.path.abspath("scratch/temp_logged_in.html")
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(logged_in_content)

main_app_png = os.path.abspath("scratch/screenshot_main_app.png")
cmd2 = [
    edge,
    "--headless",
    "--disable-gpu",
    "--window-size=1280,950",
    f"--screenshot={main_app_png}",
    "file:///" + temp_html.replace("\\", "/")
]
subprocess.run(cmd2, capture_output=True)
print("Main App Screenshot exists:", os.path.exists(main_app_png), main_app_png)
