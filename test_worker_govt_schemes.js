const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('--- RUNNING TESTS: Worker App GUI & Government Policies Hub ---');

// 1. Check HTML file presence and required elements
const htmlPath = path.join(__dirname, 'frontend', 'index.html');
assert(fs.existsSync(htmlPath), 'frontend/index.html must exist');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

assert(htmlContent.includes('id="worker-govt-schemes-hub"'), 'index.html must include #worker-govt-schemes-hub');
assert(htmlContent.includes('id="worker-welfare-header-pill"'), 'index.html must include #worker-welfare-header-pill in worker cockpit header');
assert(htmlContent.includes('id="worker-govt-schemes-grid"'), 'index.html must include #worker-govt-schemes-grid');
assert(htmlContent.includes('id="scheme-search-input"'), 'index.html must include #scheme-search-input');
assert(htmlContent.includes('id="modal-govt-scheme-details"'), 'index.html must include #modal-govt-scheme-details');
assert(htmlContent.includes('id="scheme-modal-calculator-box"'), 'index.html must include #scheme-modal-calculator-box');
assert(htmlContent.includes('id="btn-modal-claim-scheme"'), 'index.html must include #btn-modal-claim-scheme');
assert(htmlContent.includes('id="scheme-modal-claim-success"'), 'index.html must include #scheme-modal-claim-success');

console.log('✅ HTML markup verification passed: Worker hub, modal, header pill, and calculator present.');

// 2. Check CSS styles
const cssPath = path.join(__dirname, 'frontend', 'style.css');
assert(fs.existsSync(cssPath), 'frontend/style.css must exist');
const cssContent = fs.readFileSync(cssPath, 'utf8');

assert(cssContent.includes('.govt-scheme-card'), 'style.css must define .govt-scheme-card');
assert(cssContent.includes('.scheme-img-thumb'), 'style.css must define .scheme-img-thumb');
assert(cssContent.includes('.tricolor-strip'), 'style.css must define .tricolor-strip');
assert(cssContent.includes('.voucher-card-preview'), 'style.css must define .voucher-card-preview');

console.log('✅ CSS style verification passed: Scheme cards, images, badges, and vouchers styled.');

// 3. Check App.js logic and GOVT_WORKER_POLICIES definition
const appJsPath = path.join(__dirname, 'frontend', 'app.js');
assert(fs.existsSync(appJsPath), 'frontend/app.js must exist');
const appJsContent = fs.readFileSync(appJsPath, 'utf8');

assert(appJsContent.includes('const GOVT_WORKER_POLICIES'), 'app.js must define GOVT_WORKER_POLICIES');
assert(appJsContent.includes('function initGovtWorkerSchemes'), 'app.js must define initGovtWorkerSchemes');
assert(appJsContent.includes('function renderGovtWorkerSchemes'), 'app.js must define renderGovtWorkerSchemes');
assert(appJsContent.includes('function filterGovtSchemes'), 'app.js must define filterGovtSchemes');
assert(appJsContent.includes('function openGovtSchemeDetails'), 'app.js must define openGovtSchemeDetails');
assert(appJsContent.includes('function claimGovtScheme'), 'app.js must define claimGovtScheme');

// Mock a lightweight browser environment to evaluate GOVT_WORKER_POLICIES
const vm = require('vm');
const sandbox = {
    window: {},
    console: console,
    state: {},
    document: {
        getElementById: () => null,
        querySelectorAll: () => []
    }
};
vm.createContext(sandbox);

// Extract the GOVT_WORKER_POLICIES constant from app.js
const matchSchemes = appJsContent.match(/const GOVT_WORKER_POLICIES\s*=\s*(\[[\s\S]*?\n\]);/);
assert(matchSchemes, 'Should locate GOVT_WORKER_POLICIES array in app.js');

const policiesCode = `var GOVT_WORKER_POLICIES = ${matchSchemes[1]};`;
vm.runInContext(policiesCode, sandbox);
const policies = sandbox.GOVT_WORKER_POLICIES;

assert(Array.isArray(policies), 'GOVT_WORKER_POLICIES must be an array');
assert(policies.length >= 6, `Expected at least 6 policies, found ${policies.length}`);

console.log(`✅ Loaded ${policies.length} government worker policies.`);

// 4. Verify each policy structure, fields, and image paths on disk
policies.forEach((policy, index) => {
    assert(policy.id, `Policy #${index} must have an id`);
    assert(policy.title, `Policy ${policy.id} must have title`);
    assert(policy.title_hi, `Policy ${policy.id} must have title_hi`);
    assert(policy.ministry, `Policy ${policy.id} must have ministry`);
    assert(policy.category, `Policy ${policy.id} must have category`);
    assert(Array.isArray(policy.eligible_trades), `Policy ${policy.id} eligible_trades must be an array`);
    assert(policy.benefit_summary, `Policy ${policy.id} must have benefit_summary`);
    assert(policy.image, `Policy ${policy.id} must have an image path`);
    assert(policy.entitlement_amount, `Policy ${policy.id} must have entitlement_amount`);
    assert(Array.isArray(policy.benefits), `Policy ${policy.id} benefits must be an array`);
    assert(policy.helpline, `Policy ${policy.id} must have helpline`);
    assert(policy.portal_url, `Policy ${policy.id} must have portal_url`);

    // Verify physical file on disk
    const imageFullPath = path.join(__dirname, 'frontend', policy.image);
    assert(fs.existsSync(imageFullPath), `Image file must exist on disk: ${policy.image}`);
    const stat = fs.statSync(imageFullPath);
    assert(stat.size > 10000, `Image file ${policy.image} must be valid high-res image (found size: ${stat.size} bytes)`);

    console.log(`  - [Scheme ${policy.id}] "${policy.title_short}" -> Image verified (${Math.round(stat.size / 1024)} KB)`);
});

// 5. Test Category Filtering Logic
const toolkitPolicies = policies.filter(p => p.category === 'toolkit_loan');
assert(toolkitPolicies.length >= 2, 'Should find at least 2 toolkit & loan schemes (PM Vishwakarma & PM SVANidhi)');

const socialSecPolicies = policies.filter(p => p.category === 'social_security');
assert(socialSecPolicies.length >= 2, 'Should find at least 2 social security schemes (e-Shram & State Gig Board)');

const healthcarePolicies = policies.filter(p => p.category === 'healthcare');
assert(healthcarePolicies.length >= 1, 'Should find at least 1 healthcare scheme (Ayushman Bharat PM-JAY)');

const skillPolicies = policies.filter(p => p.category === 'skill_cert');
assert(skillPolicies.length >= 1, 'Should find at least 1 skill certification scheme (Skill India PMKVY RPL)');

// 6. Test Trade Eligibility Matching
function isWorkerEligible(workerTrade, policy) {
    if (policy.eligible_trades.includes('all')) return true;
    return policy.eligible_trades.some(t => t.toLowerCase() === workerTrade.toLowerCase());
}

// Electrician and Carpenter should match Vishwakarma
const vishwakarma = policies.find(p => p.id === 'pm_vishwakarma');
assert(isWorkerEligible('electrician', vishwakarma), 'Electrician should qualify for PM Vishwakarma');
assert(isWorkerEligible('carpenter', vishwakarma), 'Carpenter should qualify for PM Vishwakarma');
assert(isWorkerEligible('tailoring', vishwakarma), 'Tailoring should qualify for PM Vishwakarma');

// Universal schemes match all trades
const eshram = policies.find(p => p.id === 'eshram_pmsby');
assert(isWorkerEligible('electrician', eshram), 'Electrician should qualify for e-Shram Card');
assert(isWorkerEligible('plumber', eshram), 'Plumber should qualify for e-Shram Card');
assert(isWorkerEligible('driver', eshram), 'Driver should qualify for e-Shram Card');

const ayushman = policies.find(p => p.id === 'ayushman_pmjay');
assert(isWorkerEligible('blacksmith', ayushman), 'Blacksmith should qualify for Ayushman Bharat');
// 7. Verify Positioning: Govt Schemes Hub must be located BELOW Normal Job / Radar section
const radarIdx = htmlContent.indexOf('id="worker-normal-job-section"');
const hubIdx = htmlContent.indexOf('id="worker-govt-schemes-hub"');
assert(radarIdx !== -1, 'worker-normal-job-section must exist in index.html');
assert(hubIdx !== -1, 'worker-govt-schemes-hub must exist in index.html');
assert(hubIdx > radarIdx, 'worker-govt-schemes-hub must be positioned BELOW worker-normal-job-section');
console.log('✅ Positioning verified: Government policies hub is placed below the worker radar.');

// 8. Verify Freelance Mode Entirely Removed
assert(!htmlContent.includes('id="worker-freelance-section"'), 'Freelance section (#worker-freelance-section) must be removed entirely');
assert(!htmlContent.includes('id="worker-mode-control-bar"'), 'Freelance duty mode control bar must be removed');
assert(!htmlContent.includes('Switch to Freelance Mode'), 'Freelance quick-action switch banner must be removed');
console.log('✅ Freelancing mode completely eliminated from worker interface.');

// 9. Verify CSS line-clamp warning fix
assert(cssContent.includes('line-clamp: 2;'), 'style.css must define standard line-clamp property');
console.log('✅ CSS standard line-clamp property verified.');

console.log('✅ Qualification and category filtering rules validated successfully.');
console.log('--- ALL WORKER GOVT SCHEMES TESTS PASSED (100%) ---');
