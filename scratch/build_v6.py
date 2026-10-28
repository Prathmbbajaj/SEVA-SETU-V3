import os
import subprocess

def build_svg_v6(style="app_icon_white", size=512):
    # ViewBox: 0 0 512 512
    # Bolder strokes & optimized scale for perfect small-size (32px-48px) and high-res (512px-1024px) legibility
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{size}" height="{size}">
  <defs>
    <!-- Saffron Gradient (Energy, Citizen Empowerment) -->
    <linearGradient id="gSaffron" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFB338" />
      <stop offset="40%" stop-color="#FF7200" />
      <stop offset="100%" stop-color="#E64A00" />
    </linearGradient>

    <!-- Center Teal Gradient (Trust, Technology, Cooperation) -->
    <linearGradient id="gTeal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38E1CA" />
      <stop offset="35%" stop-color="#0284C7" />
      <stop offset="75%" stop-color="#0D9488" />
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
      <stop offset="0%" stop-color="#1D4ED8" />
      <stop offset="30%" stop-color="#2563EB" />
      <stop offset="50%" stop-color="#38BDF8" />
      <stop offset="70%" stop-color="#2563EB" />
      <stop offset="100%" stop-color="#1E40AF" />
    </linearGradient>

    <!-- Top Rim Highlight -->
    <linearGradient id="gRim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.65" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </linearGradient>

    <!-- Vector Edge Stroke -->
    <linearGradient id="gEdge" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.75" />
      <stop offset="50%" stop-color="#94A3B8" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.2" />
    </linearGradient>

    <!-- Ambient Shadow -->
    <filter id="markShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.16" />
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.10" />
    </filter>
  </defs>
'''

    if style == "app_icon_white":
        svg += '''
  <!-- Background: Pristine Porcelain Squircle with Micro-Border -->
  <rect x="18" y="18" width="476" height="476" rx="116" fill="#FFFFFF" filter="url(#markShadow)" />
  <rect x="18" y="18" width="476" height="476" rx="116" fill="none" stroke="#F1F5F9" stroke-width="2.5" />
'''

    # Center group scaled and centered
    svg += '''
  <g id="seva-setu-emblem" transform="translate(0, 4)" filter="url(#markShadow)">
    
    <!-- ================= 1. BRIDGE (SETU) ================= -->
    <g id="bridge">
      <!-- Bold, elegant bridge profile with clear arch & piers -->
      <path d="
        M 38 350
        C 125 336, 185 298, 256 298
        C 327 298, 387 336, 474 350
        C 475 352, 473 355, 469 356
        C 420 365, 385 365, 360 360
        C 357 360, 355 362, 355 366
        L 353 382
        C 353 385, 350 387, 346 387
        L 331 387
        C 327 387, 325 384, 325 379
        C 318 342, 290 324, 256 324
        C 222 324, 194 342, 187 379
        C 187 384, 185 387, 181 387
        L 166 387
        C 162 387, 159 385, 159 382
        L 157 366
        C 157 362, 155 360, 152 360
        C 127 365, 92 365, 43 356
        C 39 355, 37 352, 38 350
        Z
      " fill="url(#gBridge)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Deck Sheen -->
      <path d="
        M 42 350
        C 127 337, 186 300, 256 300
        C 326 300, 385 337, 470 350
      " fill="none" stroke="url(#gRim)" stroke-width="2.5" stroke-linecap="round" />
    </g>

    <!-- ================= 2. LEFT ARCH (SAFFRON - CITIZEN) ================= -->
    <g id="left-figure">
      <!-- Head -->
      <circle cx="148" cy="138" r="30" fill="url(#gSaffron)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="148" cy="138" r="30" fill="url(#gRim)" />

      <!-- Arch Body -->
      <path d="
        M 88 312
        C 88 198, 130 166, 172 166
        C 194 166, 210 178, 220 195
        L 194 218
        C 186 206, 176 198, 164 198
        C 138 198, 120 220, 120 306
        C 120 310, 116 312, 112 312
        L 94 314
        C 90 314, 88 312, 88 312
        Z
      " fill="url(#gSaffron)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen -->
      <path d="
        M 100 265
        C 104 195, 136 168, 170 168
        C 188 168, 204 180, 216 193
      " fill="none" stroke="url(#gRim)" stroke-width="2" stroke-linecap="round" />
    </g>

    <!-- ================= 3. RIGHT ARCH (GREEN - WORKER) ================= -->
    <g id="right-figure">
      <!-- Head -->
      <circle cx="364" cy="138" r="30" fill="url(#gGreen)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="364" cy="138" r="30" fill="url(#gRim)" />

      <!-- Arch Body -->
      <path d="
        M 424 312
        C 424 198, 382 166, 340 166
        C 318 166, 302 178, 292 195
        L 318 218
        C 326 206, 336 198, 348 198
        C 374 198, 392 220, 392 306
        C 392 310, 396 312, 400 312
        L 418 314
        C 422 314, 424 312, 424 312
        Z
      " fill="url(#gGreen)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen -->
      <path d="
        M 412 265
        C 408 195, 376 168, 342 168
        C 324 168, 308 180, 296 193
      " fill="none" stroke="url(#gRim)" stroke-width="2" stroke-linecap="round" />
    </g>

    <!-- ================= 4. CENTER ARCH (TEAL - SEVA SETU ARCH) ================= -->
    <g id="center-figure">
      <!-- Head -->
      <circle cx="256" cy="88" r="38" fill="url(#gTeal)" stroke="url(#gEdge)" stroke-width="1.2" />
      <circle cx="256" cy="88" r="38" fill="url(#gRim)" />

      <!-- Center Arch Body -->
      <path d="
        M 174 284
        C 174 190, 208 126, 256 126
        C 304 126, 338 190, 338 284
        C 338 288, 334 290, 330 290
        L 305 290
        C 301 290, 298 288, 298 284
        C 298 206, 278 164, 256 164
        C 234 164, 214 206, 214 284
        C 214 288, 211 290, 207 290
        L 182 290
        C 178 290, 174 288, 174 284
        Z
      " fill="url(#gTeal)" stroke="url(#gEdge)" stroke-width="1.2" />

      <!-- Top Sheen -->
      <path d="
        M 192 230
        C 204 158, 228 128, 256 128
        C 284 128, 308 158, 320 230
      " fill="none" stroke="url(#gRim)" stroke-width="2.5" stroke-linecap="round" />
    </g>

  </g>
</svg>'''
    return svg

for s in ["app_icon_white", "emblem_transparent"]:
    svg_file = f"scratch/v6_{s}.svg"
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(build_svg_v6(style=s, size=512))

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for s in ["app_icon_white", "emblem_transparent"]:
    name = f"v6_{s}"
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
