const fs = require('fs');
const assert = require('assert');
const vm = require('vm');

console.log("=== Testing Service Tab Card & Sub-Service Text Box Formatting ===");

const appJs = fs.readFileSync('frontend/app.js', 'utf8');
const styleCss = fs.readFileSync('frontend/style.css', 'utf8');

// 1. Verify CSS rules for box text formatting
assert(styleCss.includes('.service-tab-title'), ".service-tab-title rule must exist in style.css");
assert(styleCss.includes('-webkit-line-clamp: 2'), "-webkit-line-clamp: 2 must exist for multi-line title fitting");
assert(styleCss.includes('word-break: break-word'), "word-break: break-word must exist to prevent text overflow");
console.log("✓ Test 1: style.css line clamping and text fitting styles verified");

// 2. Extract SERVICES, SERVICE_THEMES, and functions
const servicesMatch = appJs.match(/const SERVICES = (\[[\s\S]*?\n\];)/);
const themesMatch = appJs.match(/const SERVICE_THEMES = (\{[\s\S]*?\n\};)/);
assert(servicesMatch && themesMatch, "SERVICES and SERVICE_THEMES extracted");

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
    selectedService: "plumber",
    currentCustomerName: "Aarav Mehta",
    ngoVerified: true // test with NGO verified so all 9 services + subsidy boxes render!
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
  isCustomerDebarredForService() {
    return { debarred: false };
  },
  sfx: { playClick() {} },
  safeCreateIcons() {},
  console: console
};

vm.createContext(sandbox);
vm.runInContext("SERVICES = " + servicesMatch[1].replace(/const SERVICES = /, ''), sandbox);
vm.runInContext("SERVICE_THEMES = " + themesMatch[1].replace(/const SERVICE_THEMES = /, ''), sandbox);

const initFnCode = appJs.substring(
  appJs.indexOf("function initServiceGrid("),
  appJs.indexOf("function toggleShowAllServices()")
);
vm.runInContext(initFnCode, sandbox);

// 3. Render all 9 services (including artisans with NGO subsidies) in English
mockGrid.children = [];
sandbox.initServiceGrid();

const renderedCards = mockGrid.children.filter(c => c.getAttribute && c.getAttribute("data-service-id"));
assert.strictEqual(renderedCards.length, 9, "All 9 services should render when NGO verified");

renderedCards.forEach(card => {
  const serviceId = card.getAttribute("data-service-id");
  const html = card.innerHTML;

  // Verify Card Box formatting:
  assert(card.className.includes("h-full"), `Card ${serviceId} must have h-full for equal box heights`);
  assert(card.className.includes("flex flex-col justify-between"), `Card ${serviceId} must use flex-col justify-between`);

  // Verify Title formatting:
  assert(html.includes("service-tab-title"), `Card ${serviceId} title must have service-tab-title class`);
  assert(html.includes("line-clamp-2"), `Card ${serviceId} title must have line-clamp-2`);
  assert(html.includes("break-words"), `Card ${serviceId} title must have break-words`);

  // Verify Gradient Time Pill formatting:
  assert(html.includes("whitespace-nowrap"), `Card ${serviceId} time pill must prevent word wrapping`);

  // Verify Rate Box formatting:
  assert(html.includes("max-w-[70%]"), `Card ${serviceId} rate box must constrain width to prevent overflow`);
  assert(html.includes("tracking-tight"), `Card ${serviceId} rate box must use tracking-tight`);

  // Verify Rating Box formatting:
  assert(html.includes("★"), `Card ${serviceId} must contain star icon`);
});

console.log("✓ Test 2: All 9 service cards (English) have proper box formatting and constraints");

// 4. Test Hindi rendering to ensure longer Hindi words format without breaking
sandbox.state.currentLanguage = "hi";
mockGrid.children = [];
sandbox.initServiceGrid();

const hindiCards = mockGrid.children.filter(c => c.getAttribute && c.getAttribute("data-service-id"));
assert.strictEqual(hindiCards.length, 9, "All 9 services should render in Hindi");

hindiCards.forEach(card => {
  const serviceId = card.getAttribute("data-service-id");
  const html = card.innerHTML;

  assert(html.includes("service-tab-title"), `Card ${serviceId} (Hindi) must have service-tab-title class`);
  assert(html.includes("/घंटा"), `Card ${serviceId} (Hindi) rate box must include /घंटा suffix`);
});

console.log("✓ Test 3: All 9 service cards (Hindi) have proper text box formatting");

// 5. Verify teaser card formatting (when NGO unverified)
sandbox.state.currentLanguage = "en";
sandbox.state.ngoVerified = false;
mockGrid.children = [];
sandbox.initServiceGrid();

const teaserCard = mockGrid.children.find(c => c.id === "artisan-teaser-card");
assert(teaserCard, "Teaser card must exist when NGO is not verified");
assert(teaserCard.className.includes("h-full"), "Teaser card must have h-full");
assert(teaserCard.innerHTML.includes("service-tab-title"), "Teaser card title must have service-tab-title");
assert(teaserCard.innerHTML.includes("DARPAN ID Unlock"), "Teaser card must contain formatted DARPAN ID unlock box");
assert(teaserCard.innerHTML.includes("20% Subsidy"), "Teaser card must contain formatted 20% Subsidy box");

console.log("✓ Test 4: Heritage Crafts teaser card box formatting verified");

console.log("\n=======================================================");
console.log(" ALL TEXT BOX FORMATTING TESTS PASSED (100%)!          ");
console.log("=======================================================");
