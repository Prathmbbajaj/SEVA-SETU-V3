import re
import os

with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect where view-client starts
idx_vc = html.find('<section id="view-client"')
print("view-client found at:", idx_vc)
