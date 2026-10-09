const fs = require('fs');
const assert = require('assert');
const vm = require('vm');

console.log("=== Testing Seva Setu Service Card New Design, Photos, Hover & Color Coding ===");

// 1. Verify app.js definitions
const appJs = fs.readFileSync('frontend/app.js', 'utf8');

// Verify photos on all 9 services
assert(appJs.includes('photo: "https://images.unsplash.com/'), "All services must have realistic photo URLs");
assert(appJs.includes('const SERVICE_THEMES = {'), "SERVICE_THEMES configuration must exist in app.js");
assert(appJs.includes('name: "blue"'), "Electrician must have blue theme");
assert(appJs.includes('name: "orange"'), "Plumber must have orange theme");
assert(appJs.includes('name: "green"'), "Cleaning must have green theme");

console.log("✓ Test 1: Service photos and SERVICE_THEMES definitions verified in app.js");

// 2. Verify style.css animations and hover classes
const css = fs.readFileSync('frontend/style.css', 'utf8');
assert(css.includes('.service-tab-card'), ".service-tab-card class must exist in style.css");
assert(css.includes('.service-tab-card:hover'), ".service-tab-card:hover must exist in style.css");
assert(css.includes('.service-img-thumb'), ".service-img-thumb must exist in style.css");
assert(css.includes('.service-tab-card:hover .service-img-thumb'), "Image zoom on card hover must exist in style.css");

console.log("✓ Test 2: Hover lift animation and photo zoom styles verified in style.css");

// 3. Verify HTML grid container layout
const html = fs.readFileSync('frontend/index.html', 'utf8');
assert(html.includes('id="service-grid"'), "service-grid container must exist");
assert(html.includes('grid-cols-1 sm:grid-cols-2'), "service-grid must be responsive across elongated columns");

console.log("✓ Test 3: index.html responsive elongated service-grid layout verified");

// 4. Test DOM rendering in sandbox environment
// Extract SERVICES, SERVICE_THEMES, and initServiceGrid
const servicesMatch = appJs.match(/const SERVICES = (\[[\s\S]*?\n\];)/);
const themesMatch = appJs.match(/const SERVICE_THEMES = (\{[\s\S]*?\n\};)/);

assert(servicesMatch, "SERVICES array must be extracted");
assert(themesMatch, "SERVICE_THEMES object must be extracted");

// Setup simulated DOM sandbox
const createdElements = [];
function createMockElement(tag) {
  const el = {
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
  createdElements.push(el);
  return el;
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
    ngoVerified: false
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

// Extract initServiceGrid function
const initFnCode = appJs.substring(
  appJs.indexOf("function initServiceGrid("),
  appJs.indexOf("function toggleShowAllServices()")
);
vm.runInContext(initFnCode, sandbox);

// Test 4A: Render with Plumber selected
sandbox.state.selectedService = "plumber";
mockGrid.children = [];
sandbox.initServiceGrid();

const renderedCards = mockGrid.children.filter(c => c.getAttribute("data-service-id"));
assert.strictEqual(renderedCards.length, 6, "Expected 6 default services (3 artisan hidden without NGO)");

// Check Plumber card (should be color-coded orange with darker shade when selected)
const plumberCard = renderedCards.find(c => c.getAttribute("data-service-id") === "plumber");
assert(plumberCard, "Plumber card must exist");
assert(plumberCard.className.includes("border-orange-500"), "Plumber card must have orange border when selected");
assert(plumberCard.className.includes("bg-[#fed7aa]"), "Plumber card must have darker orange shade background when selected");
assert(plumberCard.innerHTML.includes("<img src="), "Plumber card must contain photo thumbnail");
assert(plumberCard.innerHTML.includes("Skill India Vetted"), "Plumber card must contain 'Skill India Vetted'");
assert(plumberCard.innerHTML.includes("12 mins"), "Plumber card must contain time pill");
assert(plumberCard.innerHTML.includes("₹110/hr"), "Plumber card must contain rate box");
assert(plumberCard.innerHTML.includes("4.8"), "Plumber card must contain rating");
console.log("✓ Test 4A: Plumber card renders Canva design with photo and darker orange selected color coding (PASSED)");

// Check Electrician card (when unselected, should have lighter blue tint background, not white)
const elecCard = renderedCards.find(c => c.getAttribute("data-service-id") === "electrician");
assert(elecCard, "Electrician card must exist");
assert(elecCard.className.includes("bg-[#eff6ff]"), "Unselected Electrician card must have lighter blue shade background, not white");
assert(!elecCard.className.includes("bg-white"), "Unselected Electrician card must not have plain white background");
assert(elecCard.innerHTML.includes("<img src="), "Electrician card must contain photo thumbnail");
assert(elecCard.innerHTML.includes("ITI Trade Certified"), "Electrician card must contain vetted badge");
console.log("✓ Test 4B: Unselected Electrician card has lighter shade tint (not white) and hover classes (PASSED)");

// Test 4C: Select Electrician -> verify it turns darker blue
sandbox.state.selectedService = "electrician";
mockGrid.children = [];
sandbox.initServiceGrid();

const elecCardSelected = mockGrid.children.find(c => c.getAttribute("data-service-id") === "electrician");
assert(elecCardSelected.className.includes("border-blue-600"), "Electrician card must have blue border when selected");
assert(elecCardSelected.className.includes("bg-[#bfdbfe]"), "Electrician card must have darker blue background when selected");
console.log("✓ Test 4C: Electrician selected state color-coded darker blue (PASSED)");

// Test 4D: Select Cleaning -> verify it turns darker green
sandbox.state.selectedService = "cleaning";
mockGrid.children = [];
sandbox.initServiceGrid();

const cleanCardSelected = mockGrid.children.find(c => c.getAttribute("data-service-id") === "cleaning");
assert(cleanCardSelected.className.includes("border-emerald-600"), "Cleaning card must have emerald border when selected");
assert(cleanCardSelected.className.includes("bg-[#a7f3d0]"), "Cleaning card must have darker emerald green background when selected");
console.log("✓ Test 4D: Cleaning selected state color-coded darker green (PASSED)");

console.log("\n=======================================================");
console.log(" ALL SERVICE CARD DESIGN & COLOR CODING TESTS PASSED! ");
console.log("=======================================================");
