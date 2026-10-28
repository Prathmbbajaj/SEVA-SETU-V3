import shutil
import os

# Source files from scratch
src_icon_png = "scratch/v6_app_icon_white.png"
src_icon_svg = "scratch/v6_app_icon_white.svg"
src_emblem_png = "scratch/v6_emblem_transparent.png"
src_emblem_svg = "scratch/v6_emblem_transparent.svg"

dest_dir = "frontend/assets"

# 1. Main app logo (PNG and SVG)
shutil.copyfile(src_icon_png, os.path.join(dest_dir, "seva_setu_logo.png"))
shutil.copyfile(src_icon_svg, os.path.join(dest_dir, "seva_setu_logo.svg"))

# 2. Transparent emblem variants
shutil.copyfile(src_emblem_png, os.path.join(dest_dir, "seva_setu_emblem_transparent.png"))
shutil.copyfile(src_emblem_svg, os.path.join(dest_dir, "seva_setu_emblem_transparent.svg"))

# 3. Dedicated app icon
shutil.copyfile(src_icon_png, os.path.join(dest_dir, "seva_setu_app_icon.png"))

print("Assets installed into frontend/assets:")
for f in ["seva_setu_logo.png", "seva_setu_logo.svg", "seva_setu_emblem_transparent.png", "seva_setu_emblem_transparent.svg", "seva_setu_app_icon.png"]:
    p = os.path.join(dest_dir, f)
    print(f" - {f}: {os.path.getsize(p)} bytes")
