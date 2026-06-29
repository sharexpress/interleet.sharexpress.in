#!/usr/bin/env node
/**
 * prerender.mjs — Lightweight post-build prerenderer for SEO.
 *
 * After `vite build`, this script spins up a local server, opens each
 * public route in Puppeteer, snapshots the rendered DOM, and writes it
 * back to dist/ so crawlers get full HTML without executing JS.
 *
 * Usage:  node prerender.mjs
 * Runs automatically via:  npm run build  (see package.json scripts)
 */

import { execSync } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { createServer } from "http";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DIST = join(__dirname, "dist");
const PORT = 4173;

/** Routes to prerender (public, SEO-important pages) */
const ROUTES = ["/", "/login", "/signup", "/recruiter"];

/**
 * Minimal static file server for the dist folder.
 * Falls back to index.html for SPA routes (like Nginx try_files).
 */
function createStaticServer() {
  const mime = {
    ".html": "text/html",
    ".js": "application/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
  };

  return createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    let filePath = join(DIST, url.pathname);

    if (!existsSync(filePath) || filePath === DIST || filePath.endsWith("/")) {
      filePath = join(DIST, "index.html");
    }

    const ext = "." + filePath.split(".").pop();
    const contentType = mime[ext] || "application/octet-stream";

    try {
      const content = readFileSync(filePath);
      res.writeHead(200, { "Content-Type": contentType });
      res.end(content);
    } catch {
      const fallback = readFileSync(join(DIST, "index.html"));
      res.writeHead(200, { "Content-Type": "text/html" });
      res.end(fallback);
    }
  });
}

async function prerender() {
  // Check if puppeteer is available
  let puppeteer;
  try {
    puppeteer = await import("puppeteer");
  } catch {
    console.log("⚠️  Puppeteer not installed — skipping prerender.");
    console.log("   Install with: npm i -D puppeteer");
    console.log("   SEO still works via <noscript> fallback + JSON-LD in <head>.");
    process.exit(0);
  }

  if (!existsSync(DIST)) {
    console.error("❌ dist/ not found. Run `vite build` first.");
    process.exit(1);
  }

  // Start local server
  const server = createStaticServer();
  await new Promise((resolve) => server.listen(PORT, resolve));
  console.log(`🌐 Prerender server on http://localhost:${PORT}`);

  // Launch headless browser
  const browser = await puppeteer.default.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  for (const route of ROUTES) {
    const url = `http://localhost:${PORT}${route}`;
    console.log(`📄 Prerendering ${route}...`);

    const page = await browser.newPage();

    // Block unnecessary requests for speed
    await page.setRequestInterception(true);
    page.on("request", (req) => {
      const type = req.resourceType();
      if (["image", "font", "media"].includes(type)) {
        req.abort();
      } else {
        req.continue();
      }
    });

    await page.goto(url, { waitUntil: "networkidle0", timeout: 15000 });

    // Wait for prerender-ready event or timeout after 5s
    await page
      .evaluate(() => {
        return new Promise((resolve) => {
          if (document.querySelector("#root")?.children?.length > 0) {
            resolve();
          } else {
            document.addEventListener("prerender-ready", resolve, { once: true });
            setTimeout(resolve, 5000);
          }
        });
      })
      .catch(() => {});

    // Get the rendered HTML
    let html = await page.content();

    // Inject a marker so we know this page was prerendered
    html = html.replace(
      "</head>",
      '  <meta name="prerender-status" content="200" />\n  </head>'
    );

    // Write to correct path
    const outPath =
      route === "/"
        ? join(DIST, "index.html")
        : join(DIST, route.slice(1), "index.html");

    // Ensure directory exists
    const outDir = dirname(outPath);
    if (!existsSync(outDir)) {
      mkdirSync(outDir, { recursive: true });
    }

    writeFileSync(outPath, html, "utf-8");
    console.log(`  ✅ ${outPath.replace(DIST, "dist")}`);

    await page.close();
  }

  await browser.close();
  server.close();

  console.log(`\n🎉 Prerendered ${ROUTES.length} routes successfully!`);
}

prerender().catch((err) => {
  console.error("❌ Prerender failed:", err.message);
  console.log("   Build still succeeded — SPA will work normally.");
  process.exit(0); // Don't fail the build
});
