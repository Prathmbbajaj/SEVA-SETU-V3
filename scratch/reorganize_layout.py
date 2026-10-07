import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract Subscription Card
sub_card_pattern = r'(<!-- Cooperative Samriddhi Pass / Subscription Card -->\s*<div class="glass-card rounded-3xl p-6 border-amber-200 relative overflow-hidden"[\s\S]*?id="subscription-feature-card">[\s\S]*?</div>\s*</div>)'
sub_match = re.search(sub_card_pattern, content)
assert sub_match, "Could not match subscription card"
sub_card_html = sub_match.group(1)

# Note: sub_card_html ends at the closing of the subscription-feature-card div. Let's make sure it's complete.
# Let's inspect where it ends:
idx_sub_start = content.find('<!-- Cooperative Samriddhi Pass / Subscription Card -->')
idx_sub_cta_end = content.find('<!-- Active Booking Live Status Card (Revealed upon booking) -->')
sub_card_exact = content[idx_sub_start:idx_sub_cta_end].rstrip()

# 2. Extract Booking Status Card
idx_booking_start = idx_sub_cta_end
idx_right_col = content.find('<!-- Right Col: Live OpenStreetMap & Transparent Quotation Card -->')
# In the original, before Right Col there was `</div>\n\n</div>` which closed lg:col-span-2 and booking-status-card
# Let's find the end of booking-status-card
booking_card_exact = content[idx_booking_start:idx_right_col].rstrip()
# booking_card_exact ends with `</div>\n\n        </div>` (one closes booking-status-card, one closes lg:col-span-2)
# We want just booking-status-card
# Let's clean up trailing `</div>` that belonged to lg:col-span-2
if booking_card_exact.endswith('</div>'):
    # Check if there are two </div> at the end
    lines = booking_card_exact.split('\n')
    while lines and lines[-1].strip() == '':
        lines.pop()
    if lines[-1].strip() == '</div>':
        lines.pop()  # remove lg:col-span-2 closing div
    booking_card_exact = '\n'.join(lines).rstrip()

# 3. Extract Leaflet Map Card
idx_map_card_start = content.find('<!-- Leaflet OSM Map -->')
idx_reviews_start = content.find('<!-- ================= CITIZEN REVIEWS & RATINGS')
map_section_exact = content[idx_map_card_start:idx_reviews_start].rstrip()
# Clean up closing tags of right col and main grid at the end
lines_map = map_section_exact.split('\n')
while lines_map and lines_map[-1].strip() == '':
    lines_map.pop()
# There were `</div>` closing client-map container, right col, and main grid
# We want the map card div:
map_card_lines = []
depth = 0
found_start = False
for line in lines_map:
    if '<div class="glass-card' in line or '<div id="client-map' in line or found_start:
        found_start = True
    map_card_lines.append(line)

# Let's verify the Leaflet Map card content:
map_card_html = """          <!-- Leaflet OSM Map -->
          <div class="glass-card rounded-3xl p-5 overflow-hidden flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-3 px-1">
                <h3 class="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-2">
                  <div class="w-7 h-7 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center">
                    <i data-lucide="map-pin" class="w-4 h-4"></i>
                  </div>
                  <span data-i18n="txt-map-title">Worker Proximity Radar Map</span>
                </h3>
                <span
                  class="text-[10px] font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-full border border-blue-200"
                  data-i18n="txt-map-live">OpenStreetMap Live</span>
              </div>
              <div id="client-map" class="h-72 sm:h-80 w-full rounded-2xl border border-slate-200 shadow-inner"></div>
            </div>
            <div class="flex items-center justify-between mt-3 px-1 text-[11px] text-slate-500 font-medium pt-2 border-t border-slate-100">
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span> <span
                  data-i18n="txt-map-you">You (Connaught Place)</span></span>
              <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-600"></span> <span
                  data-i18n="txt-map-workers">Cooperative Workers</span></span>
            </div>
          </div>"""

# Ensure subscription card has flex flex-col justify-between so it stretches nicely
sub_card_exact_styled = sub_card_exact.replace(
    'class="glass-card rounded-3xl p-6 border-amber-200 relative overflow-hidden"',
    'class="glass-card rounded-3xl p-6 border-amber-200 relative overflow-hidden flex flex-col justify-between"'
)

# Build the new layout replacement from idx_sub_start to idx_reviews_start
new_middle_layout = f"""{booking_card_exact}

        <!-- Secondary Features Row: Samriddhi Subscription Pass (Left) & Worker Proximity Radar Map (Right) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {sub_card_exact_styled}

{map_card_html}

        </div>

      </div>"""

new_content = content[:idx_sub_start] + new_middle_layout + '\n\n\n      ' + content[idx_reviews_start:]

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully reorganized index.html layout!")
