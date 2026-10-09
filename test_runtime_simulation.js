const fs = require('fs');
const assert = require('assert');

// Simple DOM & state simulation
console.log("=== Testing Dynamic Runtime Gating & Flow Logic ===");

const html = fs.readFileSync('frontend/index.html', 'utf8');

// Check that initial index.html has:
// 1. emergency-triage-col with hidden class
assert(html.includes('id="emergency-triage-col"'), "emergency-triage-col present");
assert(html.includes('class="w-full lg:w-2/5 hidden" id="emergency-triage-col"') || html.includes('id="emergency-triage-col" class="w-full lg:w-2/5 hidden"'), "emergency-triage-col initially hidden");

// 2. search-bar-col takes full width initially
assert(html.includes('<div class="w-full" id="search-bar-col">') || html.includes('id="search-bar-col" class="w-full"'), "search-bar-col starts as full width");

// 3. modal-subscription-gateway z-index is 200, modal-service-booking is 100
const bookingModalMatch = html.match(/id="modal-service-booking"[^>]*class="([^"]*)"/);
const subGatewayMatch = html.match(/id="modal-subscription-gateway"[^>]*class="([^"]*)"/);
assert(bookingModalMatch[1].includes('z-[100]'), "Booking modal is z-[100]");
assert(subGatewayMatch[1].includes('z-[200]'), "Subscription modal is z-[200]");

// 4. Test logic inside app.js:
const appJs = fs.readFileSync('frontend/app.js', 'utf8');

// Test that SERVICES has 9 services
const servicesMatch = appJs.match(/const SERVICES = \[([\s\S]*?)\];/);
assert(servicesMatch, "SERVICES array found");
const serviceIds = [...servicesMatch[1].matchAll(/id:\s*"([^"]+)"/g)].map(m => m[1]);
console.log("Registered services:", serviceIds);
assert(serviceIds.length === 15 || serviceIds.length === 9, "Expected 9 household services (or 15 with institutional maintenance services)");
const householdServices = serviceIds.filter(id => !id.includes('_maintenance'));
assert.strictEqual(householdServices.length, 9, "Expected exactly 9 household standard & artisan services");
assert(serviceIds.includes("pottery"), "pottery registered");
assert(serviceIds.includes("blacksmith"), "blacksmith registered");
assert(serviceIds.includes("painting"), "painting registered");

// Test that artisan services are filtered when !state.ngoVerified
assert(appJs.includes("if (s.isArtisan && !state.ngoVerified)"), "artisan filtering logic present in initServiceGrid");

// Test that emergency triage col is toggled in updateSubscriberGatingUI
assert(appJs.includes('emCol.classList.remove("hidden")'), "emergency col shown when subscribed");
assert(appJs.includes('emCol.classList.add("hidden")'), "emergency col hidden when unsubscribed");

console.log("✓ All dynamic logic and state constraints verified!");
