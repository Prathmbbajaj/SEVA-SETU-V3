const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const edge = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
const port = 9444;
const profileDir = path.resolve("scratch/temp_edge_node");

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
  const page = targets.find(t => t.url && t.url.includes('frontend/index.html')) || targets.find(t => t.type === 'page');
  console.log("Connecting to:", page.url, page.webSocketDebuggerUrl);

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
      console.log(`[BROWSER CONSOLE ${msg.params.type}]:`, ...msg.params.args.map(a => a.value || a.description));
    } else if (msg.method === "Runtime.exceptionThrown") {
      console.error("[BROWSER EXCEPTION]:", JSON.stringify(msg.params.exceptionDetails));
    }
  };

  await new Promise(r => ws.onopen = r);
  console.log("WebSocket open!");

  await send("Runtime.enable");
  await send("Page.enable");
  await send("DOM.enable");

  // Check state of the page
  let evalRes = await send("Runtime.evaluate", {
    expression: `({
      url: window.location.href,
      title: document.title,
      readyState: document.readyState,
      formExists: !!document.getElementById("form-user-login-screen"),
      bodySnippet: document.body ? document.body.innerHTML.substring(0, 200) : null
    })`,
    returnByValue: true
  });
  console.log("Initial state:", evalRes.result.value);

  // Now trigger form submit or click the button!
  console.log("Triggering login click...");
  evalRes = await send("Runtime.evaluate", {
    expression: `(() => {
      try {
        const form = document.getElementById("form-user-login-screen");
        const btn = form.querySelector('button[type="submit"]');
        console.log("Button found:", !!btn);
        btn.click();
        return {
          clicked: true,
          loginVisible: !document.getElementById("screen-user-login").classList.contains("hidden") && document.getElementById("screen-user-login").style.display !== "none",
          appShellVisible: !document.getElementById("app-shell").classList.contains("hidden") && document.getElementById("app-shell").style.display !== "none",
          feedback: document.getElementById("citizen-auth-feedback") ? document.getElementById("citizen-auth-feedback").innerText : null,
          feedbackClass: document.getElementById("citizen-auth-feedback") ? document.getElementById("citizen-auth-feedback").className : null
        };
      } catch (err) {
        return { error: err.message, stack: err.stack };
      }
    })()`,
    returnByValue: true
  });
  console.log("After click result:", evalRes.result.value);

  await sleep(1500);

  // Check state after 1.5 seconds
  evalRes = await send("Runtime.evaluate", {
    expression: `({
      url: window.location.href,
      loginVisible: !document.getElementById("screen-user-login").classList.contains("hidden") && document.getElementById("screen-user-login").style.display !== "none",
      appShellVisible: !document.getElementById("app-shell").classList.contains("hidden") && document.getElementById("app-shell").style.display !== "none"
    })`,
    returnByValue: true
  });
  console.log("Final state after 1.5s:", evalRes.result.value);

  ws.close();
  edgeProc.kill();
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  edgeProc.kill();
  process.exit(1);
});
