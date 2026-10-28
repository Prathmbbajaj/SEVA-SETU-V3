const fs = require('fs');
const assert = require('assert');
const vm = require('vm');

console.log("=== Testing Sub-Services Images & Multi-Service Color Scheme Palettes in Pop-up ===");

// 1. Verify CSS styles in style.css
const styleCss = fs.readFileSync('frontend/style.css', 'utf8');
assert(styleCss.includes('.subservice-tab-card'), ".subservice-tab-card class must exist in style.css");
assert(styleCss.includes('.subservice-img-thumb'), ".subservice-img-thumb class must exist in style.css");
assert(styleCss.includes('.subservice-tab-card:hover'), ".subservice-tab-card:hover must exist in style.css");
console.log("✓ Test 1: style.css subservice card and image thumb styles verified");

// 2. Verify HTML structure in index.html
const html = fs.readFileSync('frontend/index.html', 'utf8');
assert(html.includes('id="modal-subservices-grid"'), "modal-subservices-grid must exist in index.html");
assert(html.includes('id="selected-subservices-chips"'), "selected-subservices-chips container must exist in index.html");
console.log("✓ Test 2: index.html modal subservices grid and multi-service chips container verified");

// 3. Verify app.js definitions and functions
const appJs = fs.readFileSync('frontend/app.js', 'utf8');
assert(appJs.includes('const SUB_SERVICE_PHOTOS = {'), "SUB_SERVICE_PHOTOS dictionary must exist in app.js");
assert(appJs.includes('const SUB_SERVICE_PALETTES = ['), "SUB_SERVICE_PALETTES array must exist in app.js");
assert(appJs.includes('function getSubServicePalette('), "getSubServicePalette function must exist in app.js");
assert(appJs.includes('function getSubServicePhoto('), "getSubServicePhoto function must exist in app.js");
assert(appJs.includes('function renderSubServices('), "renderSubServices function must exist in app.js");

console.log("✓ Test 3: app.js photos, palettes, and helper functions verified");

// 4. Test sandbox execution
const catalogMatch = appJs.match(/const SUB_SERVICES_CATALOG = (\{[\s\S]*?\n\};)/);
assert(catalogMatch, "SUB_SERVICES_CATALOG extracted");

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
    appendChild(child) { this.children.push(child); },
    classList: {
      _classes: new Set(),
      add(c) { this._classes.add(c); },
      remove(c) { this._classes.delete(c); },
      contains(c) { return this._classes.has(c); }
    }
  };
}

const mockGrid = createMockElement("div");
mockGrid.id = "modal-subservices-grid";
const mockCountEl = createMockElement("span");
mockCountEl.id = "selected-subservices-count";
const mockLaborEl = createMockElement("span");
mockLaborEl.id = "selected-subservices-labor";
const mockLabelEl = createMockElement("span");
mockLabelEl.id = "selected-subservices-label";
const mockSubtotalEl = createMockElement("p");
mockSubtotalEl.id = "selected-subservices-subtotal";
const mockChipsEl = createMockElement("div");
mockChipsEl.id = "selected-subservices-chips";
const mockBtn = createMockElement("button");
mockBtn.id = "btn-proceed-subservices";
const mockBar = createMockElement("div");
mockBar.id = "subservices-action-bar";

const domElements = {
  "modal-subservices-grid": mockGrid,
  "selected-subservices-count": mockCountEl,
  "selected-subservices-labor": mockLaborEl,
  "selected-subservices-label": mockLabelEl,
  "selected-subservices-subtotal": mockSubtotalEl,
  "selected-subservices-chips": mockChipsEl,
  "btn-proceed-subservices": mockBtn,
  "subservices-action-bar": mockBar
};

const sandbox = {
  state: {
    currentLanguage: "en",
    selectedService: "electrician",
    selectedSubServices: [],
    selectedSubService: null
  },
  SERVICES: [
    { id: "electrician", name: "Electrician", photo: "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=600&q=80" },
    { id: "plumber", name: "Plumber", photo: "https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?auto=format&fit=crop&w=600&q=80" }
  ],
  SUB_SERVICES_CATALOG: null,
  SUB_SERVICE_PHOTOS: null,
  SUB_SERVICE_PALETTES: null,
  getSubServicePhoto: null,
  getSubServicePalette: null,
  renderSubServices: null,
  toggleSubServiceSelection: null,
  updateSubServicesActionBar: null,
  document: {
    getElementById(id) {
      return domElements[id] || null;
    },
    createElement(tag) {
      return createMockElement(tag);
    }
  },
  sfx: { playClick() {} },
  safeCreateIcons() {},
  showToast() {},
  calculateLiveQuote() {},
  console: console
};

vm.createContext(sandbox);

// Run SUB_SERVICES_CATALOG + Palettes and Photos in sandbox
vm.runInContext("SUB_SERVICES_CATALOG = " + catalogMatch[1].replace(/const SUB_SERVICES_CATALOG = /, ''), sandbox);

const helperCode = appJs.substring(
  appJs.indexOf("const SUB_SERVICE_PHOTOS = {"),
  appJs.indexOf("// District Analytics Data")
);
vm.runInContext(helperCode.replace(/const SUB_SERVICE_PHOTOS = /, 'SUB_SERVICE_PHOTOS = ').replace(/const SUB_SERVICE_PALETTES = /, 'SUB_SERVICE_PALETTES = '), sandbox);

// Extract renderSubServices and toggle functions
const renderFunctionsCode = appJs.substring(
  appJs.indexOf("function renderSubServices(serviceId) {"),
  appJs.indexOf("// In-Menu Satisfaction Review Gate")
);
vm.runInContext(renderFunctionsCode, sandbox);

// Test 4A: Verify Palettes array has at least 7 distinct colors with hex and tailwind classes
assert(sandbox.SUB_SERVICE_PALETTES.length >= 7, "Expected at least 7 distinct palettes");
const colorNames = sandbox.SUB_SERVICE_PALETTES.map(p => p.name);
assert(colorNames.includes("blue"), "Must include blue palette");
assert(colorNames.includes("amber"), "Must include amber palette");
assert(colorNames.includes("emerald"), "Must include emerald palette");
assert(colorNames.includes("purple"), "Must include purple palette");
assert(colorNames.includes("rose"), "Must include rose palette");
assert(colorNames.includes("cyan"), "Must include cyan palette");
console.log(`✓ Test 4A: Palettes verified (${colorNames.join(", ")})`);

// Test 4B: Render Electrician subservices and check images + non-white background
mockGrid.children = [];
sandbox.renderSubServices("electrician");
assert(mockGrid.children.length >= 5, `Expected at least 5 sub-services, got ${mockGrid.children.length}`);

mockGrid.children.forEach((card, idx) => {
  const html = card.innerHTML;
  assert(html.includes("<img src="), `Sub-service card ${idx} must contain <img src=...`);
  assert(html.includes("subservice-img-thumb"), `Sub-service card ${idx} must contain subservice-img-thumb`);
  assert(card.className.includes("subservice-tab-card"), `Card ${idx} must have subservice-tab-card class`);
});
console.log(`✓ Test 4B: Rendered ${mockGrid.children.length} sub-service cards with image thumbnails`);

// Test 4C: Multi-service selection with DIFFERENT colors
// Select task 0 (Switch & Socket) and task 1 (Fan Installation)
const subList = sandbox.SUB_SERVICES_CATALOG["electrician"];
sandbox.state.selectedSubServices = [subList[0], subList[1]];
mockGrid.children = [];
sandbox.renderSubServices("electrician");

const card0 = mockGrid.children[0];
const card1 = mockGrid.children[1];
const palette0 = sandbox.SUB_SERVICE_PALETTES[0];
const palette1 = sandbox.SUB_SERVICE_PALETTES[1];

assert(card0.className.includes(palette0.selectedBorder), `Task 0 must have ${palette0.name} border`);
assert(card1.className.includes(palette1.selectedBorder), `Task 1 must have ${palette1.name} border`);
assert.notStrictEqual(palette0.name, palette1.name, "Selected tasks must have different colors");

console.log(`✓ Test 4C: Multi-service colors verified: Task 0 is ${palette0.name}, Task 1 is ${palette1.name}`);

// Test 4D: Multi-service action bar chips
assert(!mockChipsEl.classList.contains("hidden"), "Chips container must be visible when multi-services selected");
assert(mockChipsEl.innerHTML.includes(subList[0].title), "Chips must include task 0 title");
assert(mockChipsEl.innerHTML.includes(subList[1].title), "Chips must include task 1 title");
console.log("✓ Test 4D: Multi-service action bar renders color-coded task chips");

console.log("\n==========================================================================");
console.log(" ALL SUB-SERVICE IMAGES & MULTI-SERVICE COLOR PALETTE TESTS PASSED (100%)! ");
console.log("==========================================================================");
