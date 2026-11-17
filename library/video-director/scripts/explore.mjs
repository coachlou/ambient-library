// Scout an app before writing the shot list: screenshot each page and map what is on it.
// For every page: <out>/<slug>.png plus <out>/<slug>.json listing the visible text items
// (text, tag, role, box) and the same-origin links found, so you can pick screens and copy
// exact target text into the video spec. With no paths given, it visits / and then every
// same-origin link found there (up to --max pages).
// Screens that only open on a click (a menu, a selector, a folded group) go in a --states JSON
// file: [{"name": "menu", "path": "/", "steps": [{"click": "Menu"}]}]; each step is
// {click|hover: visible text} {press: key} {wait: ms}. Each state is mapped like a page.
//
// usage:  node explore.mjs BASE_URL [path ...] [--states states.json] [--out explore] [--max 20]
//                          [--viewport 1440x900] [--chrome /path/to/chrome]
// needs:  playwright-core (or playwright) installed in the CURRENT folder: npm i playwright-core
// exit:   0 ok · 1 some pages failed · 2 bad args
import { createRequire } from "node:module";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const args = process.argv.slice(2);
if (!args.length || args.includes("-h") || args.includes("--help")) {
  console.log(readFileSync(new URL(import.meta.url)).toString().split("\nimport")[0].replace(/^\/\/ ?/gm, ""));
  process.exit(args.length ? 0 : 2);
}
const opt = (k, d) => { const i = args.indexOf(k); if (i < 0) return d; const v = args[i + 1]; args.splice(i, 2); return v; };
const out = resolve(opt("--out", "explore"));
const max = +opt("--max", 20);
const [vw, vh] = opt("--viewport", "1440x900").split("x").map(Number);
const statesFile = opt("--states", null);
const chrome = opt("--chrome", null);
const [base, ...given] = args;
if (!/^https?:\/\//.test(base || "")) { console.error("first argument must be the app's base URL"); process.exit(2); }

const req = createRequire(process.cwd() + "/");
let pw;
for (const m of ["playwright-core", "playwright"]) { try { pw = req(m); break; } catch {} }
if (!pw) { console.error("playwright-core not found here: run `npm i playwright-core` in this folder"); process.exit(2); }
const macChrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
mkdirSync(out, { recursive: true });

const b = await pw.chromium.launch({ executablePath: chrome || (existsSync(macChrome) ? macChrome : undefined), headless: true });
const p = await (await b.newContext({ viewport: { width: vw, height: vh } })).newPage();
const origin = new URL(base).origin;
const queue = given.length ? [...given] : ["/"];
const seen = new Set();
const snap = async (slug, href) => {
    await p.screenshot({ path: `${out}/${slug}.png` });
  const map = await p.evaluate(() => {
      const vis = (e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && r.bottom > 0 && r.top < innerHeight && s.visibility !== "hidden" && s.opacity !== "0"; };
      const items = [];
      for (const e of document.querySelectorAll("body *")) {
        const own = [...e.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(" ").trim();
        if (!own || own.length > 120 || !vis(e)) continue;
        const r = e.getBoundingClientRect();
        items.push({ text: own, tag: e.tagName.toLowerCase(), role: e.getAttribute("role") || undefined, box: [r.x, r.y, r.width, r.height].map(Math.round) });
      }
      const links = [...document.querySelectorAll("a[href]")].map((a) => a.getAttribute("href"));
      return { title: document.title, items, links };
    });
    writeFileSync(`${out}/${slug}.json`, JSON.stringify({ url: href, ...map }).replace(/},{/g, "},\n{"));
  return map;
};
let failed = 0;

while (queue.length && seen.size < max) {
  const path = queue.shift();
  const url = new URL(path, base);
  const key = url.pathname + url.search + url.hash;
  if (seen.has(key)) continue;
  seen.add(key);
  const slug = key.replace(/[^\w]+/g, "-").replace(/^-|-$/g, "") || "home";
  try {
    await p.goto(url.href); await p.waitForTimeout(1500);
    const map = await snap(slug, url.href);
    console.log("ok", slug, map.items.length, "items");
    if (!given.length) for (const h of map.links) { try { const u = new URL(h, url); if (u.origin === origin) queue.push(u.pathname + u.search + u.hash); } catch {} }
  } catch (e) { failed++; console.log("FAIL", key, e.message.split("\n")[0]); }
}
let states = [];
if (statesFile) { try { states = JSON.parse(readFileSync(statesFile, "utf8")); } catch (e) { console.error("bad --states:", e.message); process.exit(2); } }
for (const st of states) {
  try {
    await p.goto(new URL(st.path ?? "/", base).href); await p.waitForTimeout(1500);
    for (const s of st.steps || []) {
      if (s.click) await p.getByText(s.click, { exact: true }).first().click();
      else if (s.hover) await p.getByText(s.hover, { exact: true }).first().hover();
      else if (s.press) await p.keyboard.press(s.press);
      if (s.wait) await p.waitForTimeout(s.wait); else await p.waitForTimeout(400);
    }
    const map = await snap(st.name, p.url());
    console.log("ok", st.name, map.items.length, "items");
  } catch (e) { failed++; console.log("FAIL", st.name, e.message.split("\n")[0]); }
}
await b.close();
process.exit(failed ? 1 : 0);
