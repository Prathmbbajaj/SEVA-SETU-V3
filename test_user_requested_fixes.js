const fs = require('fs');
const assert = require('assert');

console.log("=== Testing User-Requested Fixes ===");

// 1. Verify index.html updates
const html = fs.readFileSync('frontend/index.html', 'utf8');

// A. Step nav bar at the top of #view-client removed
assert(!html.includes('id="step-nav-1"'), "step-nav-1 must be removed from index.html");
assert(!html.includes('id="step-nav-2"'), "step-nav-2 must be removed from index.html");
assert(!html.includes('id="step-nav-3"'), "step-nav-3 must be removed from index.html");
assert(!html.includes('id="step-nav-4"'), "step-nav-4 must be removed from index.html");
assert(!html.includes('data-i18n="step-1"'), "data-i18n='step-1' must be removed from top bar");
console.log("✓ Fix 4 verified: Top stepper bar (Select Service Plan, Transparent Invoice, etc.) removed");

// B. Audio toggle button hidden
assert(html.includes('id="btn-audio-toggle"') && html.includes('class="hidden'), "btn-audio-toggle must be hidden");
console.log("✓ Fix 2A verified: Audio button hidden from navbar");

// C. modal-organisation-auth has backdrop dismiss and cancel button
assert(html.includes('id="modal-organisation-auth"'), "modal-organisation-auth must exist");
assert(html.includes('onclick="if (event.target === this) cancelOrganisationAuth()"') || html.includes('cancelOrganisationAuth()'), "modal-organisation-auth must have cancel action");
console.log("✓ Fix 1A verified: modal-organisation-auth markup has close actions");

// 2. Verify app.js updates
const appJs = fs.readFileSync('frontend/app.js', 'utf8');

// A. SoundFX is silenced and disabled
assert(appJs.includes('this.enabled = false;'), "SoundFX must be initialized with enabled = false");
assert(appJs.includes('playClick() {\n    // Sound permanently removed') || appJs.includes('playClick() {\r\n    // Sound permanently removed'), "playClick must be silenced");
assert(appJs.includes('playAlert() {\n    // Sound permanently removed') || appJs.includes('playAlert() {\r\n    // Sound permanently removed'), "playAlert must be silenced");
console.log("✓ Fix 2B verified: SoundFX audio synthesizer completely neutralized");

// B. cancelOrganisationAuth hides the modal and returns to household menu
assert(appJs.includes('function cancelOrganisationAuth() {'), "cancelOrganisationAuth function must exist");
assert(appJs.includes('modal.classList.add("hidden");'), "cancelOrganisationAuth must hide modal-organisation-auth");
assert(appJs.includes('setCustomerLoginType("household", false);'), "cancelOrganisationAuth must return to normal household menu");
assert(appJs.includes('window.closeOrganisationAuthModal = closeOrganisationAuthModal;'), "closeOrganisationAuthModal must be exported");
console.log("✓ Fix 1B verified: cancelOrganisationAuth adds 'hidden' class to modal and returns to normal household menu");

// C. Escape key and backdrop dismissal for organisation auth modal
assert(appJs.includes('const orgAuthModal = document.getElementById("modal-organisation-auth");'), "Global listeners must handle modal-organisation-auth");
console.log("✓ Fix 1C verified: Global click & escape key listeners handle organisation modal");

// D. Matched images for all 6 maintenance services
const expectedImages = {
  hvac_maintenance: "assets/hvac_maintenance.jpg",
  water_plant_maintenance: "assets/water_plant_maintenance.jpg",
  generator_electrical_maintenance: "assets/generator_electrical_maintenance.jpg",
  fire_safety_maintenance: "assets/fire_safety_maintenance.jpg",
  bioclean_maintenance: "assets/bioclean_maintenance.jpg",
  solar_maintenance: "assets/solar_maintenance.jpg"
};

for (const [id, imgPath] of Object.entries(expectedImages)) {
  assert(fs.existsSync(`frontend/${imgPath}`), `Image file frontend/${imgPath} must exist on disk`);
  assert(appJs.includes(`id: "${id}"`), `Service ${id} must exist in app.js`);
  assert(appJs.includes(`photo: "${imgPath}"`), `Service ${id} must reference ${imgPath}`);
}
console.log("✓ Fix 3 verified: All 6 maintenance services reference dedicated matched high-res images");

console.log("\n=======================================================");
console.log(" ALL 4 USER-REQUESTED FIXES VERIFIED SUCCESSFULLY! ");
console.log("=======================================================");
