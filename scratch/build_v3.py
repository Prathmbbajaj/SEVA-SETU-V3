import os
import subprocess

def build_svg_v3(style="app_icon_white", size=512):
    # Palette
    # Modern Indian Saffron: #FF9E1B -> #FF6000 -> #DD3E00
    # Modern Cyan/Teal: #38BDF8 -> #0D9488 -> #0F766E
    # Modern India Green: #4ADE80 -> #10B981 -> #047857
    # Modern Royal Blue: #1E3A8A -> #2563EB -> #38BDF8 -> #1D4ED8

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{size}" height="{size}">
  <defs>
    <!-- Saffron Gradient -->
    <linearGradient id="gSaffron" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFA826" />
      <stop offset="50%" stop-color="#FF6B00" />
      <stop offset="100%" stop-color="#E04600" />
    </linearGradient>

    <!-- Center Teal Gradient -->
    <linearGradient id="gTeal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" />
      <stop offset="30%" stop-color="#06B6D4" />
      <stop offset="75%" stop-color="#0D9488" />
      <stop offset="100%" stop-color="#0F766E" />
    </linearGradient>

    <!-- Green Gradient -->
    <linearGradient id="gGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>

    <!-- Bridge Royal Gradient -->
    <linearGradient id="gBridge" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#1E40AF" />
      <stop offset="30%" stop-color="#2563EB" />
      <stop offset="50%" stop-color="#38BDF8" />
      <stop offset="70%" stop-color="#2563EB" />
      <stop offset="100%" stop-color="#1D4ED8" />
    </linearGradient>

    <!-- Glass Rim Highlight -->
    <linearGradient id="gRim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.65" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </linearGradient>

    <!-- Subtle Metallic Edge -->
    <linearGradient id="gEdge" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.7" />
      <stop offset="50%" stop-color="#94A3B8" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.25" />
    </linearGradient>

    <!-- Soft Drop Shadow -->
    <filter id="markShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.18" />
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.10" />
    </filter>

    <filter id="ambientGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="30" result="blur" />
    </filter>
  </defs>
'''

    if style == "app_icon_white":
        svg += '''
  <!-- Background: Pristine Ultra-Modern White Porcelain Squircle -->
  <rect x="16" y="16" width="480" height="480" rx="112" fill="#FFFFFF" filter="url(#markShadow)" />
  <rect x="16" y="16" width="480" height="480" rx="112" fill="none" stroke="#F1F5F9" stroke-width="2" />
'''
    elif style == "app_icon_dark":
        svg += '''
  <!-- Background: Deep Navy Slate Squircle -->
  <rect x="16" y="16" width="480" height="480" rx="112" fill="#090E1A" filter="url(#markShadow)" />
  <rect x="16" y="16" width="480" height="480" rx="112" fill="none" stroke="#1E293B" stroke-width="2" />
  <!-- Subtle center blue luminescence -->
  <circle cx="256" cy="240" r="140" fill="#2563EB" opacity="0.15" filter="url(#ambientGlow)" />
'''

    svg += '''
  <g id="seva-setu-emblem" filter="url(#markShadow)">
    
    <!-- ================= 1. BRIDGE (SETU) ================= -->
    <g id="bridge">
      <path d="
        M 38 354
        C 125 342, 185 304, 256 304
        C 327 304, 387 342, 474 354
        C 475 356, 473 358, 470 359
        C 420 367, 385 367, 360 362
        C 358 362, 356 364, 356 368
        L 354 380
        C 354 383, 351 385, 347 385
        L 334 385
        C 330 385, 328 382, 328 377
        C 322 344, 292 328, 256 328
        C 220 328, 190 344, 184 377
        C 184 382, 182 385, 178 385
        L 165 385
        C 161 385, 158 383, 158 380
        L 156 368
        C 156 364, 154 362, 152 362
        C 127 367, 92 367, 42 359
        C 39 358, 37 356, 38 354
        Z
      " fill="url(#gBridge)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Sleek Top Deck Highlight -->
      <path d="
        M 42 354
        C 127 343, 186 306, 256 306
        C 326 306, 385 343, 470 354
      " fill="none" stroke="url(#gRim)" stroke-width="2" stroke-linecap="round" />
    </g>

    <!-- ================= 2. LEFT ARCH (SAFFRON - CITIZEN) ================= -->
    <g id="left-figure">
      <!-- Head -->
      <circle cx="152" cy="148" r="28" fill="url(#gSaffron)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="152" cy="148" r="28" fill="url(#gRim)" />

      <!-- Arch Body: Starts on bridge, arches up, terminates cleanly at center arch -->
      <path d="
        M 94 290
        C 94 208, 140 178, 180 178
        C 208 178, 226 195, 234 212
        C 218 226, 204 238, 194 238
        C 168 238, 150 216, 134 216
        C 122 216, 120 236, 120 290
        C 120 293, 117 295, 114 295
        L 100 295
        C 97 295, 94 293, 94 290
        Z
      " fill="url(#gSaffron)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen on Left Arch -->
      <path d="
        M 104 260
        C 108 200, 142 180, 178 180
        C 198 180, 215 190, 226 206
      " fill="none" stroke="url(#gRim)" stroke-width="1.8" stroke-linecap="round" />
    </g>

    <!-- ================= 3. RIGHT ARCH (GREEN - WORKER) ================= -->
    <g id="right-figure">
      <!-- Head -->
      <circle cx="360" cy="148" r="28" fill="url(#gGreen)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="360" cy="148" r="28" fill="url(#gRim)" />

      <!-- Arch Body: Symmetrical to left arch -->
      <path d="
        M 418 290
        C 418 208, 372 178, 332 178
        C 304 178, 286 195, 278 212
        C 294 226, 308 238, 318 238
        C 344 238, 362 216, 378 216
        C 390 216, 392 236, 392 290
        C 392 293, 395 295, 398 295
        L 412 295
        C 415 295, 418 293, 418 290
        Z
      " fill="url(#gGreen)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen on Right Arch -->
      <path d="
        M 408 260
        C 404 200, 370 180, 334 180
        C 314 180, 297 190, 286 206
      " fill="none" stroke="url(#gRim)" stroke-width="1.8" stroke-linecap="round" />
    </g>

    <!-- ================= 4. CENTER ARCH (TEAL - SEVA SETU ARCH) ================= -->
    <g id="center-figure">
      <!-- Head -->
      <circle cx="256" cy="98" r="36" fill="url(#gTeal)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="256" cy="98" r="36" fill="url(#gRim)" />

      <!-- Center Arch Body -->
      <path d="
        M 178 284
        C 178 198, 210 138, 256 138
        C 302 138, 334 198, 334 284
        C 334 287, 331 289, 328 289
        L 306 289
        C 303 289, 300 287, 300 284
        C 300 212, 280 174, 256 174
        C 232 174, 212 212, 212 284
        C 212 287, 209 289, 206 289
        L 184 289
        C 181 289, 178 287, 178 284
        Z
      " fill="url(#gTeal)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen on Center Arch -->
      <path d="
        M 194 235
        C 206 166, 230 140, 256 140
        C 282 140, 306 166, 318 235
      " fill="none" stroke="url(#gRim)" stroke-width="2.2" stroke-linecap="round" />
    </g>

  </g>
</svg>'''
    return svg

for s in ["app_icon_white", "app_icon_dark", "emblem_transparent"]:
    svg_file = f"scratch/v3_{s}.svg"
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(build_svg_v3(style=s, size=512))

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for s in ["app_icon_white", "app_icon_dark", "emblem_transparent"]:
    name = f"v3_{s}"
    svg_path = os.path.abspath(f"scratch/{name}.svg")
    png_path = os.path.abspath(f"scratch/{name}.png")
    html_path = os.path.abspath(f"scratch/{name}.html")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 512px; height: 512px; background: transparent; overflow: hidden; }}
  img {{ width: 512px; height: 512px; display: block; }}
</style>
</head>
<body>
  <img src="{svg_path.replace(chr(92), '/')}" />
</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        "--window-size=512,512",
        f"--screenshot={png_path}",
        html_path
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"Rendered {name}.png: {os.path.exists(png_path)}")

