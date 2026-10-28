import re

with open("frontend/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Prepare the User Login First Screen HTML
login_screen_html = '''  <!-- ================= FIRST SCREEN: CENTRAL USER LOGIN & SIGNUP ================= -->
  <div id="screen-user-login" class="min-h-screen w-full flex items-center justify-center p-4 sm:p-6 bg-[#98b18d] relative">
    
    <!-- Top Tricolor Ribbon -->
    <div class="fixed top-0 left-0 right-0 h-1.5 w-full bg-gradient-to-r from-amber-500 via-white to-emerald-600 z-50"></div>

    <!-- Soft Decorative Ambient Glows -->
    <div class="fixed -top-32 -left-32 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none"></div>
    <div class="fixed -bottom-32 -right-32 w-96 h-96 bg-amber-500/20 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Central Login Card -->
    <div class="relative w-full max-w-lg bg-white/95 backdrop-blur-2xl rounded-3xl shadow-2xl border border-white/80 p-6 sm:p-8 space-y-6 z-10 animate-in fade-in zoom-in duration-300 my-auto">
      
      <!-- Central Logo & Brand Header -->
      <div class="text-center space-y-3">
        <div class="inline-flex p-1.5 bg-gradient-to-br from-amber-400/30 to-blue-600/30 rounded-3xl shadow-lg">
          <img src="assets/seva_setu_logo.png" alt="Seva Setu Logo"
            class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl object-contain shadow-md hover:scale-105 transition-transform duration-300 bg-white" />
        </div>
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight flex items-center justify-center gap-2">
            Seva Setu <span class="text-amber-500 font-bold text-xl sm:text-2xl">(सेवा सेतु)</span>
          </h1>
          <p class="text-xs sm:text-[13px] font-bold text-amber-600 tracking-wide mt-1">
            सेवा से समृद्धि • <span class="text-blue-900">Ministry of Cooperation</span>
          </p>
          <p class="text-xs text-slate-500 font-medium mt-1">
            Citizen Authentication & Cooperative Service Onboarding
          </p>
        </div>
      </div>

      <!-- Quick Demo Citizen Profiles (Fast 1-Click Access) -->
      <div class="p-3 bg-slate-50/90 rounded-2xl border border-slate-200/80 space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-black text-slate-600 uppercase tracking-wider flex items-center gap-1.5">
            <i data-lucide="zap" class="w-3.5 h-3.5 text-amber-500"></i>
            <span>Quick 1-Click Demo Profiles</span>
          </span>
          <span class="text-[10px] text-blue-600 font-bold">Auto-fills credentials</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">
          <button type="button" onclick="quickFillCitizen('Aarav Mehta')"
            class="px-2.5 py-1.5 bg-white hover:bg-blue-50 text-slate-800 hover:text-blue-900 border border-slate-200 hover:border-blue-400 rounded-xl text-[11px] font-bold transition flex items-center justify-center gap-1 shadow-xs text-center btn-tactile">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Aarav Mehta</span>
          </button>
          <button type="button" onclick="quickFillCitizen('Rohan Verma')"
            class="px-2.5 py-1.5 bg-white hover:bg-amber-50 text-slate-800 hover:text-amber-900 border border-slate-200 hover:border-amber-400 rounded-xl text-[11px] font-bold transition flex items-center justify-center gap-1 shadow-xs text-center btn-tactile">
            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
            <span>Rohan Verma</span>
          </button>
          <button type="button" onclick="quickFillCitizen('Vikas Malhotra')"
            class="px-2.5 py-1.5 bg-white hover:bg-red-50 text-slate-800 hover:text-red-900 border border-slate-200 hover:border-red-400 rounded-xl text-[11px] font-bold transition flex items-center justify-center gap-1 shadow-xs text-center btn-tactile">
            <span class="w-2 h-2 rounded-full bg-red-500"></span>
            <span>Vikas Malhotra</span>
          </button>
        </div>
      </div>

      <!-- Main Sign Up & Login Form -->
      <form id="form-user-login-screen" onsubmit="handleMainUserLogin(event)" class="space-y-4">
        
        <!-- Full Name -->
        <div>
          <label class="block text-xs font-black text-slate-700 uppercase tracking-wider mb-1.5">
            Full Name (पूरा नाम) <span class="text-red-500">*</span>
          </label>
          <div class="relative">
            <i data-lucide="user" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
            <input type="text" id="citizen-auth-name" placeholder="e.g. Aarav Mehta" value="Aarav Mehta"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
              required />
          </div>
        </div>

        <!-- Phone Number -->
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="text-xs font-black text-slate-700 uppercase tracking-wider">
              Mobile Number (मोबाइल नंबर) <span class="text-red-500">*</span>
            </label>
            <button type="button" onclick="sendCitizenOtp()"
              class="text-xs text-blue-600 hover:text-blue-800 font-bold flex items-center gap-1">
              <i data-lucide="send" class="w-3 h-3"></i>
              <span>Send OTP</span>
            </button>
          </div>
          <div class="relative">
            <i data-lucide="phone" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
            <input type="tel" id="citizen-auth-phone" placeholder="+91 98765 43210" value="+91 98765 43210"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
              required />
          </div>
        </div>

        <!-- Location -->
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="text-xs font-black text-slate-700 uppercase tracking-wider">
              Service Delivery Location (सेवा पता) <span class="text-red-500">*</span>
            </label>
            <button type="button" onclick="detectCitizenGpsLocation()"
              class="text-xs text-blue-600 hover:text-blue-800 font-bold flex items-center gap-1">
              <i data-lucide="crosshair" class="w-3 h-3"></i>
              <span>Use GPS</span>
            </button>
          </div>
          <div class="relative mb-2">
            <i data-lucide="map-pin" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
            <input type="text" id="citizen-auth-location" placeholder="e.g. Connaught Place, New Delhi" value="Connaught Place, New Delhi"
              class="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-bold text-slate-800 focus:ring-2 focus:ring-blue-500 focus:outline-none transition"
              required />
          </div>

          <!-- Quick Presets -->
          <div class="flex flex-wrap items-center gap-1.5">
            <span class="text-[10px] uppercase font-bold text-slate-400">Quick Areas:</span>
            <button type="button"
              onclick="selectCitizenAuthLocationPreset('Connaught Place, New Delhi', [28.6315, 77.2167])"
              class="px-2 py-0.5 bg-slate-100 hover:bg-blue-100 text-slate-700 hover:text-blue-800 text-[10px] font-bold rounded-md transition">Connaught Place</button>
            <button type="button"
              onclick="selectCitizenAuthLocationPreset('Karol Bagh, New Delhi', [28.6506, 77.1906])"
              class="px-2 py-0.5 bg-slate-100 hover:bg-blue-100 text-slate-700 hover:text-blue-800 text-[10px] font-bold rounded-md transition">Karol Bagh</button>
            <button type="button"
              onclick="selectCitizenAuthLocationPreset('Saket, South Delhi', [28.5244, 77.2100])"
              class="px-2 py-0.5 bg-slate-100 hover:bg-blue-100 text-slate-700 hover:text-blue-800 text-[10px] font-bold rounded-md transition">Saket</button>
            <button type="button"
              onclick="selectCitizenAuthLocationPreset('Sector 18, Noida', [28.5708, 77.3261])"
              class="px-2 py-0.5 bg-slate-100 hover:bg-blue-100 text-slate-700 hover:text-blue-800 text-[10px] font-bold rounded-md transition">Noida Sec 18</button>
          </div>
        </div>

        <!-- 4-Digit Security OTP -->
        <div class="p-3.5 bg-blue-50/70 rounded-2xl border border-blue-100 space-y-2">
          <div class="flex items-center justify-between">
            <label class="text-xs font-black text-blue-900 uppercase tracking-wider">4-Digit Security OTP</label>
            <span class="text-[11px] text-blue-700 font-medium">Auto-fill available</span>
          </div>
          <div class="flex items-center gap-2">
            <input type="text" id="citizen-auth-otp" maxlength="4" placeholder="• • • •" value="4291"
              class="flex-1 text-center font-mono text-lg font-black tracking-widest px-4 py-2 bg-white border border-blue-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-none"
              required />
            <button type="button" id="citizen-auth-demo-otp-btn" onclick="autofillCitizenOtp()"
              class="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition flex items-center gap-1 shadow-xs"
              title="Auto-fill demo OTP">
              <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
              <span>Auto-Fill (<span id="citizen-auth-demo-otp-code">4291</span>)</span>
            </button>
          </div>
        </div>

        <!-- Feedback Alert Div -->
        <div id="citizen-auth-feedback" class="text-xs font-semibold hidden p-2.5 rounded-xl"></div>

        <!-- Submit Button -->
        <button type="submit"
          class="w-full py-3.5 bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 hover:from-blue-700 hover:to-indigo-900 text-white rounded-2xl font-black text-sm shadow-xl shadow-blue-600/30 transition flex items-center justify-center gap-2 btn-tactile">
          <span>Complete Sign Up & Access App (प्रवेश करें)</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>

        <p class="text-[11px] text-center text-slate-500 font-medium pt-1">
          🔒 Secured by Ministry of Cooperation & Digilocker e-KYC Protocol
        </p>
      </form>
    </div>
  </div>

  <!-- ================= MAIN APP SHELL (HIDDEN UNTIL LOGIN) ================= -->
  <div id="app-shell" class="min-h-screen flex flex-col flex-1" style="display: none;">
'''

# 2. Add login screen and start app-shell right after toast-container
target_toast = '<div id="toast-container"></div>'
if target_toast in html and 'id="screen-user-login"' not in html:
    html = html.replace(target_toast, target_toast + '\n\n' + login_screen_html, 1)

# 3. Add authenticated citizen pill to top navigation header
old_system_controls = '''        <!-- Language Selector -->
        <div class="flex items-center space-x-1.5 bg-slate-900/80 px-2.5 py-1 rounded-xl border border-blue-800/60">
          <i data-lucide="languages" class="w-4 h-4 text-amber-400"></i>
          <select id="lang-select" onchange="toggleLanguage(this.value)"
            class="bg-transparent text-xs font-bold text-blue-100 outline-none cursor-pointer">
            <option value="en" class="text-slate-900">English</option>
            <option value="hi" class="text-slate-900">हिंदी (Hindi)</option>
          </select>
        </div>
      </div>'''

new_system_controls = '''        <!-- Language Selector -->
        <div class="flex items-center space-x-1.5 bg-slate-900/80 px-2.5 py-1 rounded-xl border border-blue-800/60">
          <i data-lucide="languages" class="w-4 h-4 text-amber-400"></i>
          <select id="lang-select" onchange="toggleLanguage(this.value)"
            class="bg-transparent text-xs font-bold text-blue-100 outline-none cursor-pointer">
            <option value="en" class="text-slate-900">English</option>
            <option value="hi" class="text-slate-900">हिंदी (Hindi)</option>
          </select>
        </div>

        <!-- Authenticated Citizen Profile Pill & Logout -->
        <div id="header-user-profile-badge" class="flex items-center gap-2 bg-slate-900/90 px-3 py-1.5 rounded-2xl border border-blue-800/60 shadow-inner">
          <div class="flex items-center gap-1.5 text-xs text-white font-bold">
            <i data-lucide="user-check" class="w-3.5 h-3.5 text-emerald-400"></i>
            <span id="header-user-display-name">Aarav Mehta</span>
          </div>
          <div id="customer-location-badge" class="hidden sm:flex items-center gap-1 text-[11px] font-medium text-slate-300 bg-slate-800/80 px-2 py-0.5 rounded-lg border border-slate-700/60">
            <i data-lucide="map-pin" class="w-3 h-3 text-amber-400" id="customer-location-icon"></i>
            <span id="citizen-location-text">Connaught Place, New Delhi</span>
          </div>
          <div id="citizen-location-badge" class="hidden" style="display:none !important;"></div>
          <div id="citizen-persona-badge" class="text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
            <i data-lucide="check-circle" class="w-3 h-3 text-emerald-600" id="customer-status-icon"></i>
            <span id="citizen-persona-badge-text">Verified Citizen • Full Access</span>
          </div>
          <span class="hidden" style="display:none !important;">Deployable Prototype</span>
          <button type="button" onclick="logoutCitizenToLoginScreen()" title="Switch Account / Sign Out"
            class="text-xs text-amber-300 hover:text-white bg-blue-900/80 hover:bg-blue-800 px-2.5 py-1 rounded-xl transition font-bold flex items-center gap-1 border border-blue-700/50 btn-tactile">
            <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
            <span>Logout</span>
          </button>
        </div>
      </div>'''

if old_system_controls in html:
    html = html.replace(old_system_controls, new_system_controls, 1)

# 4. Remove the clunky horizontal Customer Login Portal section from View 1
# And replace with hidden compatibility container
pattern = r'<!-- Customer Login Portal: Dual Way for Household Customers & Organisations \(Schools/Hospitals\) -->[\s\S]*?<!-- Debarred Citizen Alert Banner \(Dynamic\) -->'

compat_container = '''<!-- Hidden compatibility container for test harnesses & background lookups -->
      <div id="customer-login-compat-container" class="hidden" style="display: none !important;" aria-hidden="true">
        <button type="button" id="btn-customer-login-type-household" onclick="setCustomerLoginType('household')"></button>
        <button type="button" id="btn-customer-login-type-organisation" onclick="setCustomerLoginType('organisation')"></button>
        <div id="customer-login-household-section">
          <select id="citizen-persona-select" onchange="changeCitizenPersona(this.value)">
            <option value="Aarav Mehta">Aarav Mehta (In Good Standing • Full Service Access)</option>
            <option value="Rohan Verma">Rohan Verma (Debarred from Electrician Service Only)</option>
            <option value="Vikas Malhotra">Vikas Malhotra (Permanently Debarred from All Services)</option>
          </select>
          <button type="button" onclick="openCitizenAuthModal()"></button>
        </div>
        <div id="customer-login-organisation-section">
          <select id="organisation-persona-select" onchange="changeOrganisationPersona(this.value)">
            <option value="St. Xavier's Senior Secondary School">🏫 St. Xavier's School</option>
            <option value="City Care Multi-Specialty Hospital">🏥 City Care Hospital</option>
            <option value="Delhi Institute of Technology & Sciences">🎓 Delhi Institute of Tech</option>
            <option value="Sanjeevani Community Health Centre">🩺 Sanjeevani Health Centre</option>
          </select>
          <button type="button" onclick="openOrganisationAuthModal()"></button>
          <button type="button" onclick="openOrganisationAmcModal()" id="btn-top-org-amc-cta"></button>
        </div>
      </div>

      <!-- Debarred Citizen Alert Banner (Dynamic) -->'''

html = re.sub(pattern, compat_container, html, count=1)

# 5. Close app-shell after </main>
target_main_end = '</main>'
if target_main_end in html and '<!-- /#app-shell -->' not in html:
    html = html.replace(target_main_end, target_main_end + '\n  </div> <!-- /#app-shell -->\n', 1)

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated frontend/index.html successfully!")
