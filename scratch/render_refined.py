import subprocess
import os

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

targets = [
    ("refined_emblem_transparent", 512, 512),
    ("refined_app_icon_white", 512, 512),
    ("refined_app_icon_dark", 512, 512),
]

for name, w, h in targets:
    svg_path = os.path.abspath(f"scratch/{name}.svg")
    png_path = os.path.abspath(f"scratch/{name}.png")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {w}px; height: {h}px; background: transparent; overflow: hidden; }}
  img {{ width: {w}px; height: {h}px; display: block; }}
</style>
</head>
<body>
  <img src="{svg_path.replace(os.sep, '/')}" />
</body>
</html>"""
    
    html_path = os.path.abspath(f"scratch/{name}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={w},{h}",
        f"--screenshot={png_path}",
        html_path
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    print(f"Rendered {name}.png, exists: {os.path.exists(png_path)}")
