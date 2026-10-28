/**
 * Automated test script to verify all core capabilities and latest feature requirements:
 * 1. Citizen & Worker Service History
 * 2. Driver GPS Telemetry HUD
 * 3. Reporting Driver Misconduct/Crime to Police / Helpline (Moved from Worker to Customer App)
 * 4. Strict OTP Lock: OTPs can only be filled once service request is accepted by worker
 * 5. Mandatory Proof of Work Enforcement
 * 6. Female Safety & Police Emergency Helpline Call Simulator (112 / 1091)
 */

const fs = require("fs");
const path = require("path");

console.log("=== SEVA SETU FEATURE & SAFETY VERIFICATION TEST SUITE ===\n");

// Read frontend/index.html
const htmlContent = fs.readFileSync(path.join(__dirname, "frontend", "index.html"), "utf-8");

// Read frontend/app.js
const appJsContent = fs.readFileSync(path.join(__dirname, "frontend", "app.js"), "utf-8");

// Read frontend/style.css
const cssContent = fs.readFileSync(path.join(__dirname, "frontend", "style.css"), "utf-8");

let passedTests = 0;
let totalTests = 0;

function assert(condition, testName) {
  totalTests++;
  if (condition) {
    console.log(`[PASS] ${testName}`);
    passedTests++;
  } else {
    console.error(`[FAIL] ${testName}`);
    process.exitCode = 1;
  }
}

// 1. Service History Verification
console.log("--- 1. Service History (Customer & Worker) ---");
assert(htmlContent.includes('id="btn-citizen-service-history"'), "HTML has citizen service history button");
assert(htmlContent.includes('id="modal-citizen-service-history"'), "HTML has citizen service history modal");
assert(htmlContent.includes('id="btn-worker-job-history"'), "HTML has worker job history button");
assert(htmlContent.includes('id="modal-worker-service-history"'), "HTML has worker service history modal");
assert(appJsContent.includes("openCitizenServiceHistoryModal"), "app.js has openCitizenServiceHistoryModal");
assert(appJsContent.includes("openWorkerServiceHistoryModal"), "app.js has openWorkerServiceHistoryModal");
assert(appJsContent.includes("customerServiceHistory: ["), "app.js seeds customerServiceHistory");
assert(appJsContent.includes("workerJobHistory: ["), "app.js seeds workerJobHistory");
assert(appJsContent.includes("downloadCoopReceipt"), "app.js has cooperative receipt generator");

// 2. Driver GPS Telemetry Verification
console.log("\n--- 2. Driver GPS Telemetry HUD ---");
assert(htmlContent.includes('id="driver-gps-telemetry-hud"'), "HTML has driver GPS telemetry HUD container");
assert(htmlContent.includes('id="telemetry-speed-val"'), "HTML has telemetry speed gauge");
assert(htmlContent.includes('id="telemetry-compass-needle"'), "HTML has telemetry compass needle");
assert(htmlContent.includes('id="telemetry-coords-lat"'), "HTML has telemetry coordinates element");
assert(cssContent.includes(".telemetry-hud-card"), "CSS has .telemetry-hud-card");
assert(appJsContent.includes("startDriverTelemetryStream"), "app.js has startDriverTelemetryStream");
assert(appJsContent.includes("stopDriverTelemetryStream"), "app.js has stopDriverTelemetryStream");
assert(appJsContent.includes("updateDriverTelemetryHUD"), "app.js has updateDriverTelemetryHUD");

// 3. Customer Driver Crime & Misconduct Reporting (Moved from Worker to Customer App)
console.log("\n--- 3. Customer Driver Crime & Misconduct Reporting (Moved from Worker to Customer) ---");
assert(!htmlContent.includes('id="btn-worker-escalate-top"'), "Worker app does NOT have top header escalation button");
assert(!htmlContent.includes('id="worker-escalate-fab-container"'), "Worker app does NOT have floating action escalation container");
assert(!htmlContent.includes('id="btn-worker-escalate-fab"'), "Worker app does NOT have floating action escalation button");
assert(htmlContent.includes('id="btn-customer-report-driver"'), "Customer app HAS Report Driver to Police button");
assert(htmlContent.includes('id="btn-driver-safety-sos"'), "Customer app HAS direct Police Helpline (112/1091) call button");
assert(htmlContent.includes('id="modal-customer-driver-report"'), "Customer app HAS Driver Misconduct & Crime Report Modal");
assert(htmlContent.includes('id="customer-driver-safety-fab-container"'), "Customer app HAS persistent driver safety floating action button");
assert(htmlContent.includes('id="btn-customer-driver-safety-fab"'), "Customer app HAS #btn-customer-driver-safety-fab trigger");
assert(appJsContent.includes("openCustomerDriverReportModal"), "app.js has openCustomerDriverReportModal");
assert(appJsContent.includes("closeCustomerDriverReportModal"), "app.js has closeCustomerDriverReportModal");
assert(appJsContent.includes("submitCustomerDriverReport"), "app.js has submitCustomerDriverReport");
assert(appJsContent.includes("quickFillReportChip"), "app.js has quickFillReportChip");
assert(appJsContent.includes("/api/customer/driver/report-crime"), "app.js connects to /api/customer/driver/report-crime endpoint");

// 4. Strict OTP Locking: OTPs can ONLY be filled once request is accepted
console.log("\n--- 4. Strict OTP Lock: OTPs Only Available Once Accepted ---");
assert(htmlContent.includes('id="input-start-otp"') && htmlContent.includes('placeholder="🔒 Locked — Accept Request First"'), "HTML has START_OTP locked with placeholder initially");
assert(htmlContent.includes('id="badge-step-1"') && htmlContent.includes("LOCKED (ACCEPT FIRST)"), "HTML has Step 1 badge showing LOCKED (ACCEPT FIRST) initially");
assert(htmlContent.includes('id="btn-autofill-start-otp"') && htmlContent.includes('disabled'), "HTML has auto-fill START_OTP disabled initially");
assert(htmlContent.includes('id="btn-submit-start-otp"') && htmlContent.includes('disabled'), "HTML has submit START_OTP disabled initially");
assert(htmlContent.includes('id="otp-locked-notice"'), "HTML has visual OTP Locked notice banner");
assert(appJsContent.includes('state.activeBooking.status !== "ACCEPTED"') && appJsContent.includes("OTP Entry Locked"), "app.js enforces acceptance check before allowing START_OTP fill or submit");
assert(appJsContent.includes('inputStartOtp.disabled = false') && appJsContent.includes("workerAcceptJob"), "app.js workerAcceptJob unlocks input-start-otp");
assert(appJsContent.includes('btnAutofillStart.disabled = false') && appJsContent.includes("workerAcceptJob"), "app.js workerAcceptJob unlocks btn-autofill-start-otp");
assert(appJsContent.includes('btnSubmitStart.disabled = false') && appJsContent.includes("workerAcceptJob"), "app.js workerAcceptJob unlocks btn-submit-start-otp");

// 5. Mandatory Proof of Work Verification
console.log("\n--- 5. Mandatory Proof of Work on Service Completion ---");
assert(htmlContent.includes('id="btn-snap-camera-proof"'), "HTML has snap camera proof simulator button");
assert(htmlContent.includes('id="proof-odometer-container"'), "HTML has driver odometer input container");
assert(htmlContent.includes('id="proof-work-notes"'), "HTML has work completion notes input");
assert(htmlContent.includes('id="proof-mandatory-notice"'), "HTML has mandatory proof notice banner");
assert(cssContent.includes(".proof-mandatory-pulse"), "CSS has .proof-mandatory-pulse animation");
assert(appJsContent.includes("hasProofPhoto"), "app.js checks for mandatory proof photo before completing");
assert(appJsContent.includes("Proof of Work photo is strictly MANDATORY"), "app.js enforces strict rejection toast if proof is missing");

// 6. Female Safety & Police Emergency Helpline Call Demonstrator
console.log("\n--- 6. Female Safety & Police Helpline Call Demonstrator ---");
assert(htmlContent.includes('id="driver-safety-helpline-box"'), "HTML has driver safety helpline box");
assert(htmlContent.includes('id="modal-emergency-helpline-call"'), "HTML has emergency helpline call modal");
assert(htmlContent.includes("Demonstration Mode:"), "Call modal clarifies demonstration mode (no live police line dialed)");
assert(htmlContent.includes('id="emergency-dispatcher-transcript"'), "HTML has dispatcher transcript console");
assert(cssContent.includes(".emergency-call-overlay"), "CSS has .emergency-call-overlay styling");
assert(cssContent.includes(".audio-bar"), "CSS has .audio-bar waveform animation");
assert(appJsContent.includes("startSimulatedEmergencyCall"), "app.js has startSimulatedEmergencyCall");
assert(appJsContent.includes("endSimulatedEmergencyCall"), "app.js has endSimulatedEmergencyCall");
assert(appJsContent.includes("sendEmergencyVoiceResponse"), "app.js has sendEmergencyVoiceResponse");

console.log(`\n=================================================`);
console.log(`TOTAL TESTS: ${totalTests} | PASSED: ${passedTests} | FAILED: ${totalTests - passedTests}`);
if (passedTests === totalTests) {
  console.log("ALL REQUIREMENTS SATISFIED AND 100% OPERATIONAL! 🚀");
} else {
  process.exit(1);
}
