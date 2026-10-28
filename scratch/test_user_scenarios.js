const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const edge = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const port = 9555;
const profileDir = path.resolve("scratch/temp_edge_scenarios");

if (fs.existsSync(profileDir)) {
  fs.rmSync(profileDir, { recursive: true, force: true });
}

const edgeProc = spawn(edge, [
  "--headless",
  "--disable-gpu",
  `--remote-debugging-port=${port}`,
  `--user-data-dir=${profileDir}`,
  "file:///" + path.resolve("frontend/index.html").replace(/\\/g, "/")
]);

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  await sleep(2500);

  const res = await fetch(`http://127.0.0.1:${port}/json`);
  const targets = await res.json();
  const page = targets.find(t => t.url && t.url.includes('frontend/index.html'));

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let idCounter = 1;
  const pending = new Map();

  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      pending.get(msg.id).resolve(msg.result);
      pending.delete(msg.id);
    } else if (msg.method === "Runtime.consoleAPICalled") {
      console.log(`[CONSOLE ${msg.params.type}]:`, ...msg.params.args.map(a => a.value || a.description));
    } else if (msg.method === "Runtime.exceptionThrown") {
      console.error("[EXCEPTION]:", JSON.stringify(msg.params.exceptionDetails));
    }
  };

  await new Promise(r => ws.onopen = r);
  await send("Runtime.enable");

  // Helper to test a scenario
  async function testScenario(name, actionJs) {
    console.log(`\n=== SCENARIO: ${name} ===`);
    const evalRes = await send("Runtime.evaluate", {
      expression: `(async () => {
        try {
          return await (${actionJs})();
        } catch (err) {
          return { error: err.message, stack: err.stack };
        }
      })()`,
      awaitPromise: true,
      returnByValue: true
    });
    console.log("Result:", evalRes.result.value);
  }

  // Scenario 1: Custom user typing custom name and OTP "9999"
  await testScenario("Custom Name & Custom OTP 9999", `() => {
    document.getElementById("citizen-auth-name").value = "Pratham";
    document.getElementById("citizen-auth-phone").value = "9876543210";
    document.getElementById("citizen-auth-location").value = "New Delhi";
    document.getElementById("citizen-auth-otp").value = "9999";
    const form = document.getElementById("form-user-login-screen");
    form.querySelector('button[type="submit"]').click();
    return {
      loginVisible: document.getElementById("screen-user-login").style.display !== "none",
      appShellVisible: document.getElementById("app-shell").style.display !== "none",
      feedback: document.getElementById("citizen-auth-feedback").innerText
    };
  }`);

  // Scenario 2: Rohan Verma demo click then submit
  await testScenario("Rohan Verma Quick Fill then Submit", `() => {
    quickFillCitizen('Rohan Verma');
    const form = document.getElementById("form-user-login-screen");
    form.querySelector('button[type="submit"]').click();
    return {
      loginVisible: document.getElementById("screen-user-login").style.display !== "none",
      appShellVisible: document.getElementById("app-shell").style.display !== "none",
      customerName: state.currentCustomerName,
      feedback: document.getElementById("citizen-auth-feedback").innerText
    };
  }`);

  // Scenario 3: Vikas Malhotra demo click then submit
  await testScenario("Vikas Malhotra Quick Fill then Submit", `() => {
    // Reset to login screen
    logoutCitizenToLoginScreen();
    quickFillCitizen('Vikas Malhotra');
    const form = document.getElementById("form-user-login-screen");
    form.querySelector('button[type="submit"]').click();
    return {
      loginVisible: document.getElementById("screen-user-login").style.display !== "none",
      appShellVisible: document.getElementById("app-shell").style.display !== "none",
      customerName: state.currentCustomerName
    };
  }`);

  ws.close();
  edgeProc.kill();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  edgeProc.kill();
  process.exit(1);
});
