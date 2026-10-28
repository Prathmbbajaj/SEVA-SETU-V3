import os
import subprocess

def create_refined_svg(style="emblem_transparent", size=512):
    """
    Precision vector recreation of Seva Setu emblem:
    - ViewBox: 0 0 512 512
    - Center X = 256
    """
    
    # Coordinates:
    # Bridge:
    # Spans from X=32 to X=480 (width ~ 448).
    # Top arc bows smoothly:
    # Starts at (32, 360), peaks at (256, 308), ends at (480, 360).
    #
    # Bridge Bottom profile:
    # Wing tip left: (32, 360) -> sweeps inwards to left pier (140, 365) with a shallow arch cutout:
    #   left arch from (70, 370) to (140, 365), peak at (105, 355)
    # Left pier: at X=140 to X=165, foot at Y=378
    # Center arch: from (165, 378) to (347, 378), smooth semicircular arch cutout peaking at (256, 328)
    # Right pier: at X=347 to X=372, foot at Y=378
    # Right arch cutout: from (372, 365) to (442, 370), peak at (407, 355)
    # Wing tip right: sweeps to (480, 360)
    #
    # Arches (Figures):
    # Center Arch (Teal):
    #   Center at X=256, Y=290
    #   Outer radius = 86, thickness = 32 -> Inner radius = 54
    #   Apex: outer at Y=144, inner at Y=176
    #   Legs end at Y=286 (conforming to the bridge top curve)
    #   Center Head: Circle at (256, 92), radius = 34
    #
    # Left Arch (Saffron):
    #   Center at X=160, Y=296
    #   Outer radius = 68, thickness = 26 -> Inner radius = 42
    #   Apex: outer at Y=178, inner at Y=204
    #   Left leg ends at Y=296, right leg connects behind the center arch at (210, 280)
    #   Left Head: Circle at (152, 136), radius = 25
    #
    # Right Arch (Green):
    #   Center at X=352, Y=296
    #   Outer radius = 68, thickness = 26 -> Inner radius = 42
    #   Apex: outer at Y=178, inner at Y=204
    #   Right leg ends at Y=296, left leg connects behind the center arch at (302, 280)
    #   Right Head: Circle at (360, 136), radius = 25

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{size}" height="{size}">
  <defs>
    <!-- Left Figure Gradient: Vibrant Indian Saffron -->
    <linearGradient id="gradSaffron" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF9D00" />
      <stop offset="45%" stop-color="#FF6A00" />
      <stop offset="100%" stop-color="#E24700" />
    </linearGradient>

    <!-- Center Figure Gradient: Modern Teal / Turquoise -->
    <linearGradient id="gradTeal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" />
      <stop offset="40%" stop-color="#0EA5E9" />
      <stop offset="85%" stop-color="#0D9488" />
      <stop offset="100%" stop-color="#0F766E" />
    </linearGradient>

    <!-- Right Figure Gradient: Fresh India Green / Emerald -->
    <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4ADE80" />
      <stop offset="50%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#047857" />
    </linearGradient>

    <!-- Bridge Gradient: Royal Sapphire Blue -->
    <linearGradient id="gradBridge" x1="0%" y1="30%" x2="100%" y2="70%">
      <stop offset="0%" stop-color="#1E40AF" />
      <stop offset="25%" stop-color="#2563EB" />
      <stop offset="50%" stop-color="#38BDF8" />
      <stop offset="75%" stop-color="#2563EB" />
      <stop offset="100%" stop-color="#1D4ED8" />
    </linearGradient>

    <!-- Top Highlight Sheen Gradient -->
    <linearGradient id="gradSheen" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0" />
    </linearGradient>

    <!-- Soft Ambient Elevation Shadow -->
    <filter id="logoShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.22" />
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#0F172A" flood-opacity="0.12" />
    </filter>

    <!-- Subtle Bevel Stroke Filter for Premium 3D Touch -->
    <linearGradient id="bevelGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.6" />
      <stop offset="50%" stop-color="#CBD5E1" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.2" />
    </linearGradient>
  </defs>
'''

    if style == "app_icon_white":
        svg_content += '''
  <!-- Background: Pristine Porcelain Squircle with Soft Glow -->
  <rect x="16" y="16" width="480" height="480" rx="108" fill="#FFFFFF" filter="url(#logoShadow)" />
  <rect x="16" y="16" width="480" height="480" rx="108" fill="none" stroke="#E2E8F0" stroke-width="2.5" />
'''
    elif style == "app_icon_dark":
        svg_content += '''
  <!-- Background: Deep Navy Glass Squircle -->
  <rect x="16" y="16" width="480" height="480" rx="108" fill="#090E1A" filter="url(#logoShadow)" />
  <rect x="16" y="16" width="480" height="480" rx="108" fill="none" stroke="#1E293B" stroke-width="2.5" />
  <circle cx="256" cy="240" r="160" fill="#2563EB" opacity="0.12" filter="blur(40px)" />
'''

    # Emblem Paths
    svg_content += '''
  <g id="seva-setu-mark" filter="url(#logoShadow)">
    
    <!-- ================= 1. BRIDGE (SETU) ================= -->
    <g id="bridge-group">
      <path d="
        M 34 362
        C 120 348, 185 310, 256 310
        C 327 310, 392 348, 478 362
        C 440 374, 405 370, 376 366
        L 374 380
        C 374 382, 370 384, 365 384
        L 347 384
        C 344 384, 342 381, 342 376
        C 338 344, 302 332, 256 332
        C 210 332, 174 344, 170 376
        C 170 381, 168 384, 165 384
        L 147 384
        C 142 384, 138 382, 138 380
        L 136 366
        C 107 370, 72 374, 34 362
        Z
      " fill="url(#gradBridge)" stroke="url(#bevelGold)" stroke-width="1.2" />

      <!-- Top Highlight on Bridge Deck -->
      <path d="
        M 38 362
        C 122 349, 186 312, 256 312
        C 326 312, 390 349, 474 362
      " fill="none" stroke="url(#gradSheen)" stroke-width="2" stroke-linecap="round" />
    </g>

    <!-- ================= 2. LEFT ARCH (SAFFRON / CITIZEN SEVA) ================= -->
    <g id="left-figure">
      <!-- Head -->
      <circle cx="152" cy="144" r="27" fill="url(#gradSaffron)" stroke="url(#bevelGold)" stroke-width="1" />
      <circle cx="152" cy="144" r="27" fill="url(#gradSheen)" />

      <!-- Arch Body -->
      <path d="
        M 94 294
        C 94 212, 142 182, 184 182
        C 212 182, 235 196, 248 214
        C 232 232, 218 244, 204 242
        C 182 238, 166 226, 150 226
        C 134 226, 122 248, 122 294
        Z
      " fill="url(#gradSaffron)" stroke="url(#bevelGold)" stroke-width="1.2" />
    </g>

    <!-- ================= 3. RIGHT ARCH (GREEN / WORKER SAMRIDDHI) ================= -->
    <g id="right-figure">
      <!-- Head -->
      <circle cx="360" cy="144" r="27" fill="url(#gradGreen)" stroke="url(#bevelGold)" stroke-width="1" />
      <circle cx="360" cy="144" r="27" fill="url(#gradSheen)" />

      <!-- Arch Body -->
      <path d="
        M 418 294
        C 418 212, 370 182, 328 182
        C 300 182, 277 196, 264 214
        C 280 232, 294 244, 308 242
        C 330 238, 346 226, 362 226
        C 378 226, 390 248, 390 294
        Z
      " fill="url(#gradGreen)" stroke="url(#bevelGold)" stroke-width="1.2" />
    </g>

    <!-- ================= 4. CENTER ARCH (TEAL / UNITY & COOPERATION) ================= -->
    <g id="center-figure">
      <!-- Head -->
      <circle cx="256" cy="92" r="35" fill="url(#gradTeal)" stroke="url(#bevelGold)" stroke-width="1.2" />
      <circle cx="256" cy="92" r="35" fill="url(#gradSheen)" />

      <!-- Center Arch Body (Overarching & Anchoring Both Sides) -->
      <path d="
        M 174 286
        C 174 200, 208 140, 256 140
        C 304 140, 338 200, 338 286
        L 300 286
        C 300 216, 282 178, 256 178
        C 230 178, 212 216, 212 286
        Z
      " fill="url(#gradTeal)" stroke="url(#bevelGold)" stroke-width="1.2" />

      <!-- Top Highlight on Center Arch -->
      <path d="
        M 200 240
        C 214 170, 240 142, 256 142
        C 272 142, 298 170, 312 240
      " fill="none" stroke="url(#gradSheen)" stroke-width="2" stroke-linecap="round" />
    </g>

  </g>
</svg>'''
    return svg_content

for s in ["emblem_transparent", "app_icon_white", "app_icon_dark"]:
    with open(f"scratch/refined_{s}.svg", "w", encoding="utf-8") as f:
        f.write(create_refined_svg(style=s, size=512))

print("Created refined SVGs in scratch/")
