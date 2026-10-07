const fs = require('fs');
const assert = require('assert');
const vm = require('vm');

console.log("=== Testing 3-Column Elongated Service Tabs & Layout Optimization ===");

const html = fs.readFileSync('frontend/index.html', 'utf8');
const appJs = fs.readFileSync('frontend/app.js', 'utf8');

// 1. Assert HTML layout structure
assert(!html.includes('How Seva Setu Booking Works'), "'How Seva Setu Works' must be completely removed");
assert(!html.includes('lg:col-span-2 space-y-6'), "Category grid must no longer be squished inside lg:col-span-2");
assert(html.includes('id="service-grid"'), "service-grid must exist");
assert(html.includes('grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'), "service-grid must have 3 columns on large screens (lg:grid-cols-3)");

// 2. Secondary features row assertions
assert(html.includes('grid-cols-1 lg:grid-cols-2 gap-6'), "Subscription pass and Proximity map must be in a balanced 2-column secondary grid");
assert(html.includes('id="subscription-feature-card"'), "subscription-feature-card must exist");
assert(html.includes('id="client-map"'), "client-map must exist");
assert(html.includes('h-72 sm:h-80'), "client-map height must be enlarged to h-72 sm:h-80 to match subscription card");

console.log("✓ Test 1: HTML layout structure, full-width container & 3-column service grid verified");

// 3. Setup VM Sandbox
function createMockElement(tag) {
  return {
    tagName: tag,
    id: "",
    className: "",
    attributes: {},
    children: [],
    innerHTML: "",
    setAttribute(k, v) { this.attributes[k] = v; },
    getAttribute(k) { return this.attributes[k]; },
    appendChild(child) { this.children.push(child); }
  };
}

const mockGrid = createMockElement("div");
mockGrid.id = "service-grid";

const sandbox = {
  SERVICES: null,
  SERVICE_THEMES: null,
  state: {
    currentLanguage: "en",
    selectedService: "electrician",
    currentCustomerName: "Aarav Mehta",
    ngoVerified: false,
    showAllServices: true
  },
  document: {
    getElementById(id) {
      if (id === "service-grid") return mockGrid;
      if (id === "service-toggle-container") return { style: {} };
      return null;
    },
    createElement(tag) {
      return createMockElement(tag);
    }
  },
  isCustomerDebarredForService: () => ({ debarred: false }),
  safeCreateIcons: () => {},
  sfx: { playClick: () => {} },
  openNgoVerificationModal: () => {},
  console: console
};

vm.createContext(sandbox);

const servicesMatch = appJs.match(/const SERVICES = (\[[\s\S]*?\n\];)/);
const themesMatch = appJs.match(/const SERVICE_THEMES = (\{[\s\S]*?\n\};)/);
assert(servicesMatch && themesMatch, "SERVICES and SERVICE_THEMES extracted");

vm.runInContext("SERVICES = " + servicesMatch[1].replace(/const SERVICES = /, ''), sandbox);
vm.runInContext("SERVICE_THEMES = " + themesMatch[1].replace(/const SERVICE_THEMES = /, ''), sandbox);

const initFnCode = appJs.substring(
  appJs.indexOf("function initServiceGrid("),
  appJs.indexOf("function toggleShowAllServices()")
);
vm.runInContext(initFnCode, sandbox);

// 4. Test when NGO is NOT verified (6 standard services + 1 spanning teaser card)
sandbox.state.ngoVerified = false;
mockGrid.children = [];
sandbox.initServiceGrid();

const unverifiedCards = mockGrid.children.filter(c => c.getAttribute && c.getAttribute('data-service-id'));
assert.strictEqual(unverifiedCards.length, 6, "Exactly 6 standard services must render when NGO is unverified");

const teaser = mockGrid.children.find(c => c.id === 'artisan-teaser-card');
assert(teaser, "Artisan teaser card must be present");
assert(teaser.className.includes('col-span-1 sm:col-span-2 lg:col-span-3'), "Teaser card must span across all columns");
assert(teaser.className.includes('h-full'), "Teaser card must have equal height (h-full)");

console.log("✓ Test 2: Unverified state: 6 standard cards + full-spanning teaser banner verified");

// 5. Test when NGO IS verified (9 services + 1 artisan section divider)
sandbox.state.ngoVerified = true;
mockGrid.children = [];
sandbox.initServiceGrid();

const verifiedCards = mockGrid.children.filter(c => c.getAttribute && c.getAttribute('data-service-id'));
assert.strictEqual(verifiedCards.length, 9, "All 9 services must render when NGO is verified");

// Artisan section divider
const divider = mockGrid.children.find(c => c.id === 'artisan-guilds-section-header');
assert(divider, "Artisan guilds section header must be present when NGO is verified");
assert(divider.className.includes('col-span-1 sm:col-span-2 lg:col-span-3'), "Artisan divider must span all 3 columns");

// Verify that the 3 artisan services are pottery, blacksmith, and painting
const artisanCards = verifiedCards.filter(c => {
  const id = c.getAttribute('data-service-id');
  return ['pottery', 'blacksmith', 'painting'].includes(id);
});
assert.strictEqual(artisanCards.length, 3, "Exactly 3 artisan services must be unlocked");

// Verify equal elongation & sizing across all 9 cards
verifiedCards.forEach(card => {
  const id = card.getAttribute('data-service-id');
  const cls = card.className;
  assert(cls.includes('service-tab-card'), `Card ${id} must have service-tab-card class`);
  assert(cls.includes('h-full'), `Card ${id} must have h-full for equal row height`);
  assert(cls.includes('flex flex-col justify-between'), `Card ${id} must use flex layout for equal elongation`);
  assert(card.innerHTML.includes('service-tab-title'), `Card ${id} must have service-tab-title`);
});

console.log("✓ Test 3: Verified NGO state: 9 services (3 in each row), artisan divider spanning 3 cols, and equal elongation verified");

console.log("\n=======================================================");
console.log(" ALL 3-COLUMN ELONGATED SERVICES TESTS PASSED (100%)! ");
console.log("=======================================================");
