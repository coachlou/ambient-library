// Capture every still a video needs, driven by a video spec (JSON).
// Each shot becomes <out>/<shot>-<k>.png: frame k carries callout k (an accent ring
// around what the voice names, the rest of the screen softly dimmed) and the caption.
// Shots with `html` are rendered as title/stat/closing cards instead of app pages.
//
// usage:  node capture.mjs SPEC.json [--only shot,shot] [--dry-run]
// needs:  playwright-core (or playwright) installed in the CURRENT folder: npm i playwright-core
// exit:   0 all frames ok · 1 some frames failed (listed as FAIL) · 2 bad args/spec
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const args = process.argv.slice(2);
if (!args.length || args.includes("-h") || args.includes("--help")) {
  console.log(readFileSync(new URL(import.meta.url)).toString().split("\nimport")[0].replace(/^\/\/ ?/gm, ""));
  process.exit(args.length ? 0 : 2);
}
const specPath = resolve(args[0]);
let spec;
try { spec = JSON.parse(readFileSync(specPath, "utf8")); } catch (e) { console.error("bad spec:", e.message); process.exit(2); }
const dry = args.includes("--dry-run");
const oi = args.indexOf("--only"); const only = oi > -1 ? new Set(args[oi + 1].split(",")) : null;
const root = dirname(specPath);
const out = resolve(root, spec.frames || "frames");
const [vw, vh] = spec.viewport || [1440, 900];
const shots = spec.shots.filter((s) => !only || only.has(s.name));

if (dry) {
  for (const s of shots) {
    const n = Math.max(1, (s.callouts || []).filter((c) => c.same === undefined).length);
    console.log(`${s.name}: ${s.html ? "card" : (s.path ?? "/")} -> ${n} frame(s)`);
  }
  process.exit(0);
}

const req = createRequire(process.cwd() + "/");
let pw;
for (const m of ["playwright-core", "playwright"]) { try { pw = req(m); break; } catch {} }
if (!pw) { console.error("playwright-core not found here: run `npm i playwright-core` in this folder"); process.exit(2); }
const macChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const exe = spec.chrome || (existsSync(macChrome) ? macChrome : undefined);
mkdirSync(out, { recursive: true });

const b = await pw.chromium.launch({ executablePath: exe, headless: true });
const p = await (await b.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: spec.dpr || 1.5 })).newPage();
for (const m of spec.mocks || []) await p.route(m.url, (r) => r.fulfill({ status: m.status || 200, json: m.json }));

const accent = spec.accent || "#FF6A1F";
const cap = (text, top) => p.evaluate(([t, top]) => {
  document.getElementById("vcap")?.remove(); if (!t) return;
  const d = document.createElement("div"); d.id = "vcap"; d.textContent = t;
  Object.assign(d.style, { position: "fixed", left: "50%", [top ? "top" : "bottom"]: "18px", transform: "translateX(-50%)", maxWidth: "960px", padding: "12px 24px", borderRadius: "14px", background: "rgba(24,24,24,0.88)", color: "#fff", font: "600 21px/1.35 -apple-system, Helvetica, Arial, sans-serif", textAlign: "center", zIndex: 99999, boxShadow: "0 8px 30px rgba(0,0,0,.25)" });
  document.body.appendChild(d);
}, [text, top]);
// The ring is its own overlay div: a box-shadow on the target itself is clipped or invisible.
const ring = (r, pad) => p.evaluate(([r, pad, accent]) => {
  document.getElementById("vring")?.remove(); if (!r) return;
  const d = document.createElement("div"); d.id = "vring";
  Object.assign(d.style, { position: "fixed", left: r.x - pad + "px", top: r.y - pad + "px", width: r.w + 2 * pad + "px", height: r.h + 2 * pad + "px", border: `4px solid ${accent}`, borderRadius: "14px", boxShadow: `0 0 0 6000px rgba(15,15,15,0.30), 0 0 22px 4px ${accent}8c`, zIndex: 99990, pointerEvents: "none" });
  document.body.appendChild(d);
}, [r, pad, accent]);

// A target names one element: {text, exact?, within?, nth?} | {regex, flags?, within?, last?} |
// {selector, nth?, last?} | {role, name, exact?, last?} | {climb: text, minW, minH}.
const loc = (t, scope = p) => {
  const sc = t.within ? scope.locator(t.within).first() : scope;
  let l;
  if (t.selector) l = sc.locator(t.selector);
  else if (t.role) l = sc.getByRole(t.role, { name: t.name, exact: t.exact ?? true });
  else if (t.regex) l = sc.getByText(new RegExp(t.regex, t.flags || ""));
  else l = sc.getByText(t.text, { exact: t.exact ?? true });
  return t.last ? l.last() : t.nth !== undefined ? l.nth(t.nth) : l.first();
};
const box = async (t) => {
  if (t.climb) return p.evaluate(([s, mw, mh]) => {
    let e = [...document.querySelectorAll("*")].find((x) => x.childElementCount === 0 && x.textContent.trim() === s);
    if (!e) throw new Error("climb text not found: " + s);
    while (e.parentElement && (e.getBoundingClientRect().width < mw || e.getBoundingClientRect().height < mh)) e = e.parentElement;
    const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height };
  }, [t.climb, t.minW || 0, t.minH || 0]);
  const bb = await loc(t).boundingBox({ timeout: 5000 });
  if (!bb) throw new Error("not visible: " + JSON.stringify(t));
  return bb;
};
// ring: a target, or {union: [targets], widen?: selector} — widen stretches the ring to that
// element's x-range (use the side nav so a group's ring is not ragged).
const rect = async (rg) => {
  const ts = rg.union || [rg];
  const bs = []; for (const t of ts) bs.push(await box(t));
  let x0 = Math.min(...bs.map((q) => q.x)), y0 = Math.min(...bs.map((q) => q.y));
  let x1 = Math.max(...bs.map((q) => q.x + q.width)), y1 = Math.max(...bs.map((q) => q.y + q.height));
  if (rg.widen) { const w = await p.locator(rg.widen).first().boundingBox(); x0 = w.x + 10; x1 = w.x + w.width - 10; }
  return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
};
// steps: {goto: path} {click: target} {hover: target} {fill: [target, text]} {press: key}
//        {wait: ms} {scroll: target} {eval: "js expression"}
const run = async (steps = []) => {
  for (const s of steps) {
    if (s.goto !== undefined) { await p.goto(new URL(s.goto, spec.baseUrl).href); await p.waitForTimeout(spec.settleMs ?? 1500); }
    else if (s.click) { await loc(s.click).click(); await p.waitForTimeout(400); }
    else if (s.hover) await loc(s.hover).hover();
    else if (s.fill) await loc(s.fill[0]).fill(s.fill[1]);
    else if (s.press) await p.keyboard.press(s.press);
    else if (s.wait) await p.waitForTimeout(s.wait);
    else if (s.scroll) await loc(s.scroll).scrollIntoViewIfNeeded();
    else if (s.eval) await p.evaluate(s.eval);
  }
};

const card = (body) => `<!doctype html><html><body style="margin:0;height:${vh}px;display:flex;align-items:center;justify-content:center;background:${spec.cardBackground || "#f4f3ef"};color:${spec.cardColor || "#1c1c1c"};font-family:-apple-system,Helvetica,Arial,sans-serif"><div style="text-align:center;max-width:1100px">${body}</div></body></html>`;

let failed = 0;
for (const s of shots) {
  try {
    if (s.html) { await p.setContent(card(s.html)); await p.screenshot({ path: `${out}/${s.name}-0.png` }); console.log("ok", `${s.name}-0`); continue; }
    if (s.fresh !== false) await run([{ goto: s.path ?? "/" }]);
    await run(s.setup);
    const cs = s.callouts?.length ? s.callouts : [{}];
    let k = 0;
    for (const c of cs) {
      if (c.same !== undefined) continue; // reuses an earlier frame; build.py handles it
      const name = `${s.name}-${k++}`;
      try {
        await run(c.setup);
        await p.waitForTimeout(500);
        const r = c.ring ? await rect(c.ring) : null;
        await ring(r, c.pad ?? 8);
        await cap(c.caption ?? s.caption ?? "", c.captionTop ?? (r ? r.y + r.h > vh * 0.78 : false));
        await p.screenshot({ path: `${out}/${name}.png` });
        await ring(null); await cap("");
        await run(c.after);
        console.log("ok", name);
      } catch (e) { failed++; console.log("FAIL", name, e.message.split("\n")[0]); await ring(null); await cap(""); }
    }
    await run(s.after);
  } catch (e) { failed++; console.log("FAIL", s.name, e.message.split("\n")[0]); }
}
await b.close();
process.exit(failed ? 1 : 0);
