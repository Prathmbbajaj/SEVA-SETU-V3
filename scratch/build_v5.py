import os
import subprocess

def build_svg_v5(style="app_icon_white", size=512):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{size}" height="{size}">
  <defs>
    <!-- Saffron Gradient (Energy, Citizen Empowerment) -->
    <linearGradient id="gSaffron" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFA826" />
      <stop offset="45%" stop-color="#FF6B00" />
      <stop offset="100%" stop-color="#E04600" />
    </linearGradient>

    <!-- Center Teal Gradient (Trust, Technology, Cooperation) -->
    <linearGradient id="gTeal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" />
      <stop offset="35%" stop-color="#0EA5E9" />
      <stop offset="80%" stop-color="#0D9488" />
      <stop offset="100%" stop-color="#0F766E" />
    </linearGradient>

    <!-- Green Gradient (Growth, Welfare, Samriddhi) -->
    <linearGradient id="gGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>

    <!-- Bridge Royal Sapphire Gradient (The Setu / Foundation) -->
    <linearGradient id="gBridge" x1="0%" y1="20%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#1E40AF" />
      <stop offset="30%" stop-color="#2563EB" />
      <stop offset="50%" stop-color="#38BDF8" />
      <stop offset="70%" stop-color="#2563EB" />
      <stop offset="100%" stop-color="#1D4ED8" />
    </linearGradient>

    <!-- Soft Glass Sheen Highlights -->
    <linearGradient id="gRim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.65" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </linearGradient>

    <!-- Subtle Bevel Edge Stroke for Modern Vector Depth -->
    <linearGradient id="gEdge" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.75" />
      <stop offset="50%" stop-color="#94A3B8" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.2" />
    </linearGradient>

    <!-- Soft Ambient Elevation Shadow -->
    <filter id="markShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#0F172A" flood-opacity="0.16" />
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.10" />
    </filter>

    <filter id="ambientGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="32" result="blur" />
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
  <!-- Background: Deep Navy Slate Squircle (Matching Seva Setu Header) -->
  <rect x="16" y="16" width="480" height="480" rx="112" fill="#090E1A" filter="url(#markShadow)" />
  <rect x="16" y="16" width="480" height="480" rx="112" fill="none" stroke="#1E293B" stroke-width="2" />
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

      <!-- Top Deck Sheen -->
      <path d="
        M 42 354
        C 127 343, 186 306, 256 306
        C 326 306, 385 343, 470 354
      " fill="none" stroke="url(#gRim)" stroke-width="2" stroke-linecap="round" />
    </g>

    <!-- ================= 2. LEFT ARCH (SAFFRON - CITIZEN) ================= -->
    <g id="left-figure">
      <!-- Head -->
      <circle cx="150" cy="144" r="28" fill="url(#gSaffron)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="150" cy="144" r="28" fill="url(#gRim)" />

      <!-- Arch Body: Contours smoothly down to bridge deck -->
      <path d="
        M 92 316
        C 92 206, 132 174, 172 174
        C 192 174, 206 185, 216 200
        L 194 220
        C 186 210, 176 202, 166 202
        C 142 202, 120 224, 120 310
        C 120 313, 117 315, 114 315
        L 98 318
        C 95 318, 92 316, 92 316
        Z
      " fill="url(#gSaffron)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen on Left Arch -->
      <path d="
        M 102 270
        C 106 200, 136 176, 170 176
        C 188 176, 202 187, 212 198
      " fill="none" stroke="url(#gRim)" stroke-width="1.8" stroke-linecap="round" />
    </g>

    <!-- ================= 3. RIGHT ARCH (GREEN - WORKER) ================= -->
    <g id="right-figure">
      <!-- Head -->
      <circle cx="362" cy="144" r="28" fill="url(#gGreen)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="362" cy="144" r="28" fill="url(#gRim)" />

      <!-- Arch Body: Contours smoothly down to bridge deck -->
      <path d="
        M 420 316
        C 420 206, 380 174, 340 174
        C 320 174, 306 185, 296 200
        L 318 220
        C 326 210, 336 202, 346 202
        C 370 202, 392 224, 392 310
        C 392 313, 395 315, 398 315
        L 414 318
        C 417 318, 420 316, 420 316
        Z
      " fill="url(#gGreen)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen on Right Arch -->
      <path d="
        M 410 270
        C 406 200, 376 176, 342 176
        C 324 176, 310 187, 300 198
      " fill="none" stroke="url(#gRim)" stroke-width="1.8" stroke-linecap="round" />
    </g>

    <!-- ================= 4. CENTER ARCH (TEAL - SEVA SETU ARCH) ================= -->
    <g id="center-figure">
      <!-- Head -->
      <circle cx="256" cy="94" r="36" fill="url(#gTeal)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="256" cy="94" r="36" fill="url(#gRim)" />

      <!-- Center Arch Body -->
      <path d="
        M 178 290
        C 178 198, 210 134, 256 134
        C 302 134, 334 198, 334 290
        C 334 293, 331 295, 328 295
        L 306 295
        C 303 295, 300 293, 300 290
        C 300 212, 280 170, 256 170
        C 232 170, 212 212, 212 290
        C 212 293, 209 295, 206 295
        L 184 295
        C 181 295, 178 293, 178 290
        Z
      " fill="url(#gTeal)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen on Center Arch -->
      <path d="
        M 194 235
        C 206 166, 230 136, 256 136
        C 282 136, 306 166, 318 235
      " fill="none" stroke="url(#gRim)" stroke-width="2.2" stroke-linecap="round" />
    </g>

  </g>
</svg>'''
    return svg

for s in ["app_icon_white", "app_icon_dark", "emblem_transparent"]:
    svg_file = f"scratch/v5_{s}.svg"
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(build_svg_v5(style=s, size=512))

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for s in ["app_icon_white", "app_icon_dark", "emblem_transparent"]:
    name = f"v5_{s}"
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
