import subprocess
import os

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.tailwindcss.com"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
  body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 20px; background: #0f172a; }}
</style>
</head>
<body class="space-y-8">

  <div class="text-white text-lg font-bold">Navbar Comparison (At actual 48px / 12rem scale)</div>

  <!-- Option 1: App Icon on White Squircle -->
  <div class="p-4 bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-950 rounded-2xl border border-blue-900/50 flex items-center space-x-3.5">
    <img src="v5_app_icon_white.png" class="w-12 h-12 rounded-2xl object-contain shadow-lg hover:scale-105 transition-transform flex-shrink-0" />
    <div class="flex flex-col justify-center">
      <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center gap-2 leading-tight">
        Seva Setu <span class="text-amber-400 font-bold text-base sm:text-lg">(सेवा सेतु)</span>
      </h1>
      <p class="text-xs sm:text-[13px] text-amber-300/95 font-bold tracking-wide leading-none mt-1">
        सेवा से समृद्धि
      </p>
    </div>
    <span class="ml-auto text-xs text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full">Option 1: Modern White App Icon</span>
  </div>

  <!-- Option 2: Transparent Emblem on Frosted Glass Capsule -->
  <div class="p-4 bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-950 rounded-2xl border border-blue-900/50 flex items-center space-x-3.5">
    <div class="w-12 h-12 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 p-1 flex items-center justify-center shadow-lg hover:scale-105 transition-transform flex-shrink-0">
      <img src="v5_emblem_transparent.png" class="w-full h-full object-contain" />
    </div>
    <div class="flex flex-col justify-center">
      <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center gap-2 leading-tight">
        Seva Setu <span class="text-amber-400 font-bold text-base sm:text-lg">(सेवा सेतु)</span>
      </h1>
      <p class="text-xs sm:text-[13px] text-amber-300/95 font-bold tracking-wide leading-none mt-1">
        सेवा से समृद्धि
      </p>
    </div>
    <span class="ml-auto text-xs text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full">Option 2: Transparent Emblem on Glass</span>
  </div>

  <!-- Option 3: Modern Dark Glass App Icon -->
  <div class="p-4 bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-950 rounded-2xl border border-blue-900/50 flex items-center space-x-3.5">
    <img src="v5_app_icon_dark.png" class="w-12 h-12 rounded-2xl object-contain shadow-lg border border-blue-500/30 hover:scale-105 transition-transform flex-shrink-0" />
    <div class="flex flex-col justify-center">
      <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center gap-2 leading-tight">
        Seva Setu <span class="text-amber-400 font-bold text-base sm:text-lg">(सेवा सेतु)</span>
      </h1>
      <p class="text-xs sm:text-[13px] text-amber-300/95 font-bold tracking-wide leading-none mt-1">
        सेवा से समृद्धि
      </p>
    </div>
    <span class="ml-auto text-xs text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full">Option 3: Deep Navy App Icon</span>
  </div>

  <!-- Option 4: Pure Transparent Floating Vector Mark -->
  <div class="p-4 bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-950 rounded-2xl border border-blue-900/50 flex items-center space-x-3.5">
    <img src="v5_emblem_transparent.png" class="w-12 h-12 object-contain hover:scale-105 transition-transform flex-shrink-0" />
    <div class="flex flex-col justify-center">
      <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center gap-2 leading-tight">
        Seva Setu <span class="text-amber-400 font-bold text-base sm:text-lg">(सेवा सेतु)</span>
      </h1>
      <p class="text-xs sm:text-[13px] text-amber-300/95 font-bold tracking-wide leading-none mt-1">
        सेवा से समृद्धि
      </p>
    </div>
    <span class="ml-auto text-xs text-slate-400 bg-slate-800/80 px-3 py-1 rounded-full">Option 4: Floating Transparent Mark</span>
  </div>

</body>
</html>"""

html_path = os.path.abspath("scratch/compare_navbar.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

png_path = os.path.abspath("scratch/compare_navbar.png")
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--window-size=900,600",
    f"--screenshot={png_path}",
    html_path
]
subprocess.run(cmd, capture_output=True)
print(f"Rendered comparison: {os.path.exists(png_path)}")
