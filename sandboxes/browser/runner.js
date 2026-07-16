/*
 * Copyright 2026 Sharexpress Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const fs = require('fs');
const path = require('path');
const express = require('express');
const { chromium } = require('playwright');

// By default, workspace is mapped to /workspace
const WORKSPACE_DIR = process.env.WORKSPACE_DIR || process.cwd();

async function main() {
    // 1. Read Runtime Config
    let config = {
        entry: 'index.html',
        timeout: 5000,
        captureScreenshot: false,
        captureDOM: true,
        captureConsole: true,
        network: 'enabled',
        evaluationScript: null
    };

    const configPath = path.join(WORKSPACE_DIR, 'runtime.json');
    if (fs.existsSync(configPath)) {
        try {
            const userConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
            config = { ...config, ...userConfig };
        } catch (e) {
            console.error("Failed to parse runtime.json:", e);
        }
    }

    // Read STDIN if present
    let stdinContent = "";
    const stdinPath = path.join(WORKSPACE_DIR, 'stdin.txt');
    if (fs.existsSync(stdinPath)) {
        stdinContent = fs.readFileSync(stdinPath, 'utf8').trim();
    }

    // 2. Start Static Server on dynamic port
    const app = express();
    app.get('/favicon.ico', (req, res) => res.status(204).end());
    app.use(express.static(WORKSPACE_DIR));
    
    const server = await new Promise((resolve) => {
        const s = app.listen(0, '127.0.0.1', () => resolve(s));
    });
    const port = server.address().port;
    const baseUrl = `http://127.0.0.1:${port}`;

    // 3. Launch Playwright Chromium
    const browserArgs = ['--no-sandbox', '--disable-setuid-sandbox'];
    if (config.network === 'disabled') {
        // We still need local access, but this blocks external
        // Not perfectly enforced by playwright args alone, but Docker handles the real network isolation.
    }

    const launchOptions = { args: browserArgs };
    const browser = await chromium.launch({ args: browserArgs });
    const context = await browser.newContext();
    const page = await context.newPage();

    // Setup Capture Objects
    const result = {
        status: "success",
        console: [],
        dom: "",
        errors: [],
        performance: {},
        network: [],
        screenshot: null,
        stdout: "" // Used for legacy output matching
    };

    // Intercept Console
    if (config.captureConsole) {
        page.on('console', msg => {
            const type = msg.type();
            const text = msg.text();
            result.console.push({ type, text });
            
            // For legacy evaluators that console.log their result
            if (type === 'log') {
                result.stdout += text + "\n";
            } else if (type === 'error') {
                result.errors.push(text);
            }
        });
    }

    // Intercept Page Errors
    page.on('pageerror', error => {
        result.errors.push(`Page Error: ${error.message}`);
    });
    
    // Intercept Network
    page.on('request', request => {
        result.network.push({
            method: request.method(),
            url: request.url(),
            type: request.resourceType()
        });
    });

    try {
        // Inject STDIN
        await page.addInitScript((stdin) => {
            window.STDIN_CONTENT = stdin;
        }, stdinContent);

        // 4. Navigate
        const entryUrl = `${baseUrl}/${config.entry}`;
        await page.goto(entryUrl, { waitUntil: 'load', timeout: config.timeout });

        // Extract Performance (basic)
        const perfTiming = JSON.parse(await page.evaluate(() => JSON.stringify(window.performance.timing)));
        result.performance.domContentLoaded = perfTiming.domContentLoadedEventEnd - perfTiming.navigationStart;
        result.performance.load = perfTiming.loadEventEnd - perfTiming.navigationStart;

        // 5. Execute Custom Evaluation Script (if provided)
        if (config.evaluationScript) {
            const evalRes = await page.evaluate(async (scriptStr) => {
                // Async function wrapper to allow await inside evaluation script
                const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
                const fn = new AsyncFunction(scriptStr);
                return await fn();
            }, config.evaluationScript);
            
            if (evalRes !== undefined) {
                // Some legacy scripts returned the result instead of logging
                // Or maybe the executor wants the return value.
                // We'll append it to stdout so the backend Judge can compare it.
                if (typeof evalRes === 'object') {
                    result.stdout += JSON.stringify(evalRes) + "\n";
                } else {
                    result.stdout += evalRes + "\n";
                }
            }
        }

        // 6. Capture Final DOM
        if (config.captureDOM) {
            result.dom = await page.evaluate(() => document.documentElement.outerHTML);
        }

        // 7. Capture Screenshot
        if (config.captureScreenshot) {
            const buffer = await page.screenshot({ fullPage: true });
            result.screenshot = buffer.toString('base64');
        }

    } catch (e) {
        result.status = "error";
        result.errors.push(e.message);
    } finally {
        // Cleanup
        await browser.close();
        server.close();
    }

    // Output strictly the JSON result
    console.log(JSON.stringify(result));
}

main().catch(err => {
    console.error(JSON.stringify({
        status: "error",
        errors: [err.message]
    }));
    process.exit(1);
});
