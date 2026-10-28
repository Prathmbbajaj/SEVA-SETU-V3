import os
import subprocess

# Let's craft a pristine SVG definition
def generate_svg(variant="modern_vibrant", bg="transparent", size=512):
    """
    variant:
      - 'modern_vibrant': Clean modern gradients, crisp lines, transparent background
      - 'app_icon_white': Premium modern app icon on clean white squircle
      - 'app_icon_dark': Premium modern app icon on deep navy glass squircle
    """
    view_w = 600
    view_h = 500

    # Gradient definitions
    # Saffron:
    # Teal:
    # Emerald:
    # Royal Blue:
    svg_defs = """
  <defs>
    <!-- Left Figure Gradient (Saffron / Energy) -->
    <linearGradient id="gradOrange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF9F1C" />
      <stop offset="60%" stop-color="#FF6B00" />
      <stop offset="100%" stop-color="#E05300" />
    </linearGradient>

    <!-- Center Figure Gradient (Teal / Trust & Technology) -->
    <linearGradient id="gradTeal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2DD4BF" />
      <stop offset="50%" stop-color="#0D9488" />
      <stop offset="100%" stop-color="#0F766E" />
    </linearGradient>

    <!-- Right Figure Gradient (Green / Growth & Welfare) -->
    <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34D399" />
      <stop offset="60%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#059669" />
    </linearGradient>

    <!-- Bridge Gradient (Royal Blue / Foundation & Unity) -->
    <linearGradient id="gradBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1D4ED8" />
      <stop offset="25%" stop-color="#2563EB" />
      <stop offset="50%" stop-color="#3B82F6" />
      <stop offset="75%" stop-color="#2563EB" />
      <stop offset="100%" stop-color="#1D4ED8" />
    </linearGradient>

    <!-- Subtle Soft Shadow for Professional Elevation -->
    <filter id="softShadow" x="-10%" y="-10%" width="125%" height="125%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.18" />
    </filter>

    <filter id="subtleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0284C7" flood-opacity="0.25" />
    </filter>
  </defs>
"""

    # Geometric coordinates for the emblem:
    # Center X = 300
    #
    # 1. Bridge (Setu):
    # Span from X=50 to X=550. Center at X=300.
    # Top arc: starts (50, 375), control point (300, 310), ends (550, 375)
    # Right wing end: curves to (550, 375) -> sharp tip or curved return.
    # Bottom cutout:
    # Pier right: (440, 375)
    # Right arch cutout: (440, 375) -> (380, 375)
    # Pier center-right: (380, 375)
    # Center main arch cutout: (380, 375) up to peak at Y=335, down to (220, 375)
    # Pier center-left: (220, 375)
    # Left arch cutout: (220, 375) -> (160, 375)
    # Left wing: curves to (50, 375)
    #
    # 2. Three arches:
    # Center Arch (Teal):
    # Outer radius ~ 95, inner radius ~ 60 (thickness 35).
    # Arch center at (300, 290). Peak at Y=195. Inner peak at Y=230.
    # Legs come down to Y=285.
    # Center Head: Circle at (300, 130), radius ~ 36.
    #
    # Left Arch (Orange):
    # Outer radius ~ 75, inner radius ~ 45 (thickness 30).
    # Center at (200, 290). Peak at Y=215.
    # Left Head: Circle at (185, 175), radius ~ 28.
    #
    # Right Arch (Green):
    # Outer radius ~ 75, inner radius ~ 45 (thickness 30).
    # Center at (400, 290). Peak at Y=215.
    # Right Head: Circle at (415, 175), radius ~ 28.

    # Let's write the SVG elements
    svg_body = ""

    if bg == "white_card":
        svg_body += f"""
    <!-- Modern Squircle Background -->
    <rect x="20" y="20" width="560" height="460" rx="90" fill="#FFFFFF" filter="url(#softShadow)" />
    <rect x="20" y="20" width="560" height="460" rx="90" fill="none" stroke="#E2E8F0" stroke-width="3" />
"""
    elif bg == "dark_card":
        svg_body += f"""
    <!-- Modern Dark Glass Squircle -->
    <rect x="20" y="20" width="560" height="460" rx="90" fill="#0B1329" filter="url(#softShadow)" />
    <rect x="20" y="20" width="560" height="460" rx="90" fill="none" stroke="#1E293B" stroke-width="4" />
    <circle cx="300" cy="250" r="180" fill="#3B82F6" opacity="0.08" filter="blur(40px)" />
"""

    emblem_group = """
    <g id="seva-setu-emblem" filter="url(#softShadow)">
      <!-- ================= 1. BRIDGE (SETU) ================= -->
      <!-- Smooth, elegant architectural bridge with 3 arches underneath and aerodynamic tapered deck -->
      <path d="
        M 45 385
        C 150 372, 210 325, 300 325
        C 390 325, 450 372, 555 385
        C 515 396, 475 397, 440 380
        C 432 372, 425 365, 410 365
        C 395 365, 388 372, 380 385
        C 370 385, 365 370, 360 355
        C 345 332, 255 332, 240 355
        C 235 370, 230 385, 220 385
        C 212 372, 205 365, 190 365
        C 175 365, 168 372, 160 380
        C 125 397, 85 396, 45 385
        Z
      " fill="url(#gradBlue)" />

      <!-- ================= 2. LEFT FIGURE (ORANGE / SAFFRON) ================= -->
      <!-- Head -->
      <circle cx="180" cy="182" r="32" fill="url(#gradOrange)" />
      <!-- Arch Body -->
      <path d="
        M 120 305
        C 120 235, 175 220, 220 238
        C 225 240, 230 244, 236 249
        C 225 272, 208 278, 195 274
        C 172 266, 158 275, 158 305
        Z
      " fill="url(#gradOrange)" />

      <!-- ================= 3. RIGHT FIGURE (GREEN / EMERALD) ================= -->
      <!-- Head -->
      <circle cx="420" cy="182" r="32" fill="url(#gradGreen)" />
      <!-- Arch Body -->
      <path d="
        M 480 305
        C 480 235, 425 220, 380 238
        C 375 240, 370 244, 364 249
        C 375 272, 392 278, 405 274
        C 428 266, 442 275, 442 305
        Z
      " fill="url(#gradGreen)" />

      <!-- ================= 4. CENTER FIGURE (TEAL / TURQUOISE) ================= -->
      <!-- Head -->
      <circle cx="300" cy="118" r="40" fill="url(#gradTeal)" />
      <!-- Elevated Center Arch Body -->
      <path d="
        M 205 305
        C 205 230, 235 170, 300 170
        C 365 170, 395 230, 395 305
        L 355 305
        C 355 245, 335 210, 300 210
        C 265 210, 245 245, 245 305
        Z
      " fill="url(#gradTeal)" />
    </g>
"""

    full_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" width="{size}" height="{int(size * view_h / view_w)}">
{svg_defs}
{svg_body}
{emblem_group}
</svg>"""
    return full_svg

with open("scratch/logo_draft.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg(bg="transparent"))

with open("scratch/logo_white_card.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg(bg="white_card"))

with open("scratch/logo_dark_card.svg", "w", encoding="utf-8") as f:
    f.write(generate_svg(bg="dark_card"))

print("Generated drafts in scratch/")
