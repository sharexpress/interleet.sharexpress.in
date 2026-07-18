#!/usr/bin/env python3
"""
seed_10_fetch_api_challenges.py
Creates and populates 10 Fetch API-based Frontend challenges in MongoDB.
Each includes starter code (HTML/CSS/JS), visible test cases, and hidden test cases.
"""

import json
from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["interleet"]

db = get_db()
col = db["problems"]

FETCH_CHALLENGES = [

    # ── 1. Fetch & Display User Profile ──────────────────────────────────────
    {
        "title": "Fetch & Display User Profile",
        "slug": "fetch-display-user-profile",
        "short_description": "Fetch a user from JSONPlaceholder and render their name, email, and city on the page.",
        "description": (
            "### Fetch & Display User Profile\n\n"
            "Use the Fetch API to load user data and render it on the page.\n\n"
            "#### Requirements\n"
            "- On page load, fetch `https://jsonplaceholder.typicode.com/users/1`.\n"
            "- Display the user's **name** in `#user-name`.\n"
            "- Display the user's **email** in `#user-email`.\n"
            "- Display the user's **city** (`address.city`) in `#user-city`.\n"
            "- While fetching, show a loading indicator in `#loading` with text `Loading...`.\n"
            "- Hide `#loading` once data is rendered.\n"
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Fetch API", "Promises", "JSON", "DOM"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "Use fetch().then(r => r.json()).then(data => ...) pattern.",
            "Set textContent of elements after the promise resolves.",
            "Toggle visibility of #loading using style.display.",
        ],
        "concepts": ["Fetch API", "Promises", "Async Data Rendering"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>User Profile</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"card\">\n"
                    "    <p id=\"loading\">Loading...</p>\n"
                    "    <h2 id=\"user-name\"></h2>\n"
                    "    <p id=\"user-email\"></p>\n"
                    "    <p id=\"user-city\"></p>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".card { background: #18181b; border: 1px solid #27272a; padding: 32px; border-radius: 12px; "
                    "min-width: 280px; }\n"
                    "h2 { font-size: 1.4rem; margin-bottom: 8px; color: #a78bfa; }\n"
                    "p { color: #a1a1aa; margin-top: 6px; font-size: 0.9rem; }\n"
                    "#loading { color: #71717a; font-style: italic; }\n"
                ),
                "index.js": (
                    "// TODO: Fetch user data from JSONPlaceholder and render it\n"
                    "// Endpoint: https://jsonplaceholder.typicode.com/users/1\n"
                    "// 1. Show #loading while fetching.\n"
                    "// 2. Populate #user-name, #user-email, #user-city.\n"
                    "// 3. Hide #loading when done.\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "fup-tc-1", "name": "Renders user name in #user-name", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('user-name');"
                    "resolve(el && el.textContent.trim().length > 0 ? 'PASS' : 'FAIL: #user-name is empty');"
                    "}, 1500));"
                )})
            },
            {
                "id": "fup-tc-2", "name": "Renders email containing @", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('user-email');"
                    "resolve(el && el.textContent.includes('@') ? 'PASS' : 'FAIL: #user-email missing or no @');"
                    "}, 1500));"
                )})
            },
            {
                "id": "fup-tc-3", "name": "Hides loading indicator after fetch", "hidden": True,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('loading');"
                    "const hidden = !el || el.style.display === 'none' || el.style.visibility === 'hidden' || el.textContent.trim() === '';"
                    "resolve(hidden ? 'PASS' : 'FAIL: #loading still visible after fetch');"
                    "}, 2000));"
                )})
            },
            {
                "id": "fup-tc-4", "name": "City is Gwenborough", "hidden": True,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('user-city');"
                    "resolve(el && el.textContent.includes('Gwenborough') ? 'PASS' : 'FAIL: expected Gwenborough in #user-city');"
                    "}, 1500));"
                )})
            },
        ]
    },

    # ── 2. Fetch Posts List & Render ──────────────────────────────────────────
    {
        "title": "Fetch Posts List",
        "slug": "fetch-posts-list",
        "short_description": "Fetch the first 5 posts from JSONPlaceholder and render them as a list on the page.",
        "description": (
            "### Fetch Posts List\n\n"
            "Fetch posts from a public API and render them dynamically.\n\n"
            "#### Requirements\n"
            "- On page load, fetch `https://jsonplaceholder.typicode.com/posts?_limit=5`.\n"
            "- For each post, create a `<div class=\"post\">` element inside `#posts-container`.\n"
            "- Inside each `.post`, render an `<h3>` with the post **title** and a `<p>` with the **body**.\n"
            "- When done, `#posts-container` should contain exactly **5** `.post` elements.\n"
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Fetch API", "Promises", "DOM Manipulation", "Lists"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "Use fetch with ?_limit=5 to get 5 posts.",
            "Use forEach to iterate and create DOM elements.",
            "appendChild or innerHTML can both work.",
        ],
        "concepts": ["Fetch API", "Dynamic DOM Creation", "Array Iteration"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Posts List</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div id=\"posts-container\"></div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; padding: 24px; }\n"
                    ".post { background: #18181b; border: 1px solid #27272a; border-radius: 10px; "
                    "padding: 20px; margin-bottom: 14px; }\n"
                    ".post h3 { font-size: 1rem; color: #a78bfa; margin-bottom: 8px; text-transform: capitalize; }\n"
                    ".post p { color: #a1a1aa; font-size: 0.85rem; line-height: 1.5; }\n"
                ),
                "index.js": (
                    "// TODO: Fetch posts and render them\n"
                    "// Endpoint: https://jsonplaceholder.typicode.com/posts?_limit=5\n"
                    "// For each post, create a div.post with h3 (title) and p (body) inside #posts-container\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "fpl-tc-1", "name": "Exactly 5 .post elements rendered", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const posts = document.querySelectorAll('#posts-container .post');"
                    "resolve(posts.length === 5 ? 'PASS' : 'FAIL: expected 5 .post elements, got ' + posts.length);"
                    "}, 1500));"
                )})
            },
            {
                "id": "fpl-tc-2", "name": "Each post has an h3 title", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const h3s = document.querySelectorAll('#posts-container .post h3');"
                    "const allHaveText = Array.from(h3s).every(h => h.textContent.trim().length > 0);"
                    "resolve(h3s.length === 5 && allHaveText ? 'PASS' : 'FAIL: expected 5 h3 titles with text');"
                    "}, 1500));"
                )})
            },
            {
                "id": "fpl-tc-3", "name": "Each post has a p body", "hidden": True,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const ps = document.querySelectorAll('#posts-container .post p');"
                    "const allHaveText = Array.from(ps).every(p => p.textContent.trim().length > 0);"
                    "resolve(ps.length === 5 && allHaveText ? 'PASS' : 'FAIL: expected 5 p body elements with text');"
                    "}, 1500));"
                )})
            },
        ]
    },

    # ── 3. Search GitHub Users ─────────────────────────────────────────────────
    {
        "title": "GitHub User Search",
        "slug": "github-user-search",
        "short_description": "Build a search input that fetches and displays a GitHub user's avatar and bio.",
        "description": (
            "### GitHub User Search\n\n"
            "Build a search box that queries the GitHub API on button click.\n\n"
            "#### Requirements\n"
            "- An `<input id=\"username-input\">` for typing the GitHub username.\n"
            "- A `<button id=\"search-btn\">` that triggers the fetch.\n"
            "- On click, fetch `https://api.github.com/users/{username}`.\n"
            "- Display the user's **avatar** in `<img id=\"avatar\">` (set `src` to `avatar_url`).\n"
            "- Display the user's **name** in `#gh-name`.\n"
            "- Display the user's **bio** in `#gh-bio` (may be null — show `'No bio'` if null).\n"
            "- If the user is not found (404), show `'User not found'` in `#error-msg`.\n"
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Fetch API", "GitHub API", "User Input", "Error Handling"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "Check response.ok before calling response.json().",
            "Use response.status === 404 to detect missing users.",
            "Bio can be null — use the || operator as a fallback.",
        ],
        "concepts": ["Fetch API", "Error Handling", "API Integration"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>GitHub Search</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>GitHub User Search</h1>\n"
                    "    <div class=\"search-bar\">\n"
                    "      <input type=\"text\" id=\"username-input\" placeholder=\"Enter GitHub username\">\n"
                    "      <button id=\"search-btn\">Search</button>\n"
                    "    </div>\n"
                    "    <p id=\"error-msg\"></p>\n"
                    "    <div id=\"result\" style=\"display:none\">\n"
                    "      <img id=\"avatar\" src=\"\" alt=\"avatar\" width=\"80\" height=\"80\">\n"
                    "      <h2 id=\"gh-name\"></h2>\n"
                    "      <p id=\"gh-bio\"></p>\n"
                    "    </div>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { width: 100%; max-width: 400px; }\n"
                    "h1 { font-size: 1.3rem; margin-bottom: 16px; color: #a78bfa; }\n"
                    ".search-bar { display: flex; gap: 8px; margin-bottom: 12px; }\n"
                    "input { flex: 1; padding: 10px 14px; background: #18181b; border: 1px solid #3f3f46; "
                    "border-radius: 8px; color: #f4f4f5; font-size: 0.9rem; }\n"
                    "button { padding: 10px 16px; background: #6366f1; border: none; border-radius: 8px; "
                    "color: white; cursor: pointer; font-size: 0.9rem; }\n"
                    "#error-msg { color: #f87171; font-size: 0.85rem; margin-bottom: 8px; }\n"
                    "#result { background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 20px; "
                    "display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center; }\n"
                    "#avatar { border-radius: 50%; }\n"
                ),
                "index.js": (
                    "// TODO: Implement GitHub User Search\n"
                    "// 1. Listen for #search-btn click\n"
                    "// 2. Fetch https://api.github.com/users/{username-input value}\n"
                    "// 3. On success: populate #avatar src, #gh-name, #gh-bio, show #result\n"
                    "// 4. On 404: show 'User not found' in #error-msg\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "ghs-tc-1", "name": "Search for 'torvalds' renders avatar", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const input = document.getElementById('username-input');"
                    "const btn = document.getElementById('search-btn');"
                    "if(!input||!btn) return 'FAIL: missing #username-input or #search-btn';"
                    "input.value = 'torvalds';"
                    "btn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "const avatar = document.getElementById('avatar');"
                    "resolve(avatar && avatar.src && avatar.src.includes('github') ? 'PASS' : 'FAIL: avatar not loaded');"
                    "}, 2500));"
                )})
            },
            {
                "id": "ghs-tc-2", "name": "Invalid user shows error message", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const input = document.getElementById('username-input');"
                    "const btn = document.getElementById('search-btn');"
                    "input.value = 'this-user-definitely-does-not-exist-xyz999abc';"
                    "btn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "const err = document.getElementById('error-msg');"
                    "resolve(err && err.textContent.trim().length > 0 ? 'PASS' : 'FAIL: #error-msg should show error for invalid user');"
                    "}, 2500));"
                )})
            },
        ]
    },

    # ── 4. Weather App with OpenMeteo ─────────────────────────────────────────
    {
        "title": "Weather Dashboard",
        "slug": "weather-dashboard-fetch",
        "short_description": "Fetch real-time weather for London using the Open-Meteo API and display temperature and wind speed.",
        "description": (
            "### Weather Dashboard\n\n"
            "Build a weather card that fetches live data from the free Open-Meteo API.\n\n"
            "#### Requirements\n"
            "- On page load, fetch the following URL:\n"
            "  ```\n"
            "  https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true\n"
            "  ```\n"
            "- Display `current_weather.temperature` in `#temperature` (append `°C`).\n"
            "- Display `current_weather.windspeed` in `#windspeed` (append ` km/h`).\n"
            "- Show `#loading` with text `Loading...` while fetching, hide it after.\n"
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Fetch API", "REST API", "JSON", "Real Data"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "The response JSON has a current_weather object.",
            "Use textContent to set the values.",
            "Open-Meteo is a free, no-auth API — no key needed.",
        ],
        "concepts": ["Fetch API", "Real API Integration", "Data Display"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Weather</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"card\">\n"
                    "    <h1>London Weather</h1>\n"
                    "    <p id=\"loading\">Loading...</p>\n"
                    "    <p id=\"temperature\"></p>\n"
                    "    <p id=\"windspeed\"></p>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".card { background: #18181b; border: 1px solid #27272a; border-radius: 16px; "
                    "padding: 36px 40px; text-align: center; }\n"
                    "h1 { font-size: 1.4rem; margin-bottom: 20px; color: #60a5fa; }\n"
                    "#temperature { font-size: 3rem; font-weight: bold; color: #fbbf24; }\n"
                    "#windspeed { font-size: 1rem; color: #a1a1aa; margin-top: 8px; }\n"
                    "#loading { color: #71717a; font-style: italic; }\n"
                ),
                "index.js": (
                    "// TODO: Fetch weather data from Open-Meteo\n"
                    "// URL: https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true\n"
                    "// Show #loading while fetching\n"
                    "// Set #temperature to temperature + '°C'\n"
                    "// Set #windspeed to windspeed + ' km/h'\n"
                    "// Hide #loading when done\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "wd-tc-1", "name": "Temperature element contains °C", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('temperature');"
                    "resolve(el && el.textContent.includes('°C') ? 'PASS' : 'FAIL: #temperature should contain °C');"
                    "}, 2000));"
                )})
            },
            {
                "id": "wd-tc-2", "name": "Wind speed contains km/h", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('windspeed');"
                    "resolve(el && el.textContent.includes('km/h') ? 'PASS' : 'FAIL: #windspeed should contain km/h');"
                    "}, 2000));"
                )})
            },
            {
                "id": "wd-tc-3", "name": "Loading indicator hidden after fetch", "hidden": True,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('loading');"
                    "const hidden = !el || el.style.display === 'none' || el.textContent.trim() === '';"
                    "resolve(hidden ? 'PASS' : 'FAIL: #loading still visible');"
                    "}, 2000));"
                )})
            },
        ]
    },

    # ── 5. POST Request — Create a Todo ───────────────────────────────────────
    {
        "title": "Create Todo with POST",
        "slug": "create-todo-post-request",
        "short_description": "Use fetch with POST to submit a new todo and display the server's response.",
        "description": (
            "### Create Todo with POST\n\n"
            "Learn how to send data to an API using `POST` and handle the response.\n\n"
            "#### Requirements\n"
            "- Render an `<input id=\"todo-input\">` and a `<button id=\"submit-btn\">Submit</button>`.\n"
            "- On button click, send a `POST` request to `https://jsonplaceholder.typicode.com/todos` with:\n"
            "  ```json\n  { \"title\": \"<input value>\", \"completed\": false, \"userId\": 1 }\n  ```\n"
            "- Include headers: `Content-Type: application/json`.\n"
            "- Display the returned `id` from the response in `#response-id`.\n"
            "- Display the returned `title` in `#response-title`.\n"
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Fetch API", "POST", "Forms", "API Integration"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "fetch(url, { method: 'POST', headers: {...}, body: JSON.stringify({...}) })",
            "JSONPlaceholder always returns a fake id of 201.",
            "The response body is parsed with response.json().",
        ],
        "concepts": ["POST Requests", "Request Headers", "JSON Stringify"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Create Todo</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>Create Todo</h1>\n"
                    "    <input type=\"text\" id=\"todo-input\" placeholder=\"Enter todo title\">\n"
                    "    <button id=\"submit-btn\">Submit</button>\n"
                    "    <div id=\"result\">\n"
                    "      <p>ID: <span id=\"response-id\"></span></p>\n"
                    "      <p>Title: <span id=\"response-title\"></span></p>\n"
                    "    </div>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { width: 100%; max-width: 360px; }\n"
                    "h1 { font-size: 1.3rem; color: #a78bfa; margin-bottom: 16px; }\n"
                    "input { width: 100%; padding: 10px 14px; background: #18181b; border: 1px solid #3f3f46; "
                    "border-radius: 8px; color: #f4f4f5; font-size: 0.9rem; margin-bottom: 10px; }\n"
                    "button { width: 100%; padding: 10px; background: #6366f1; border: none; border-radius: 8px; "
                    "color: white; cursor: pointer; font-size: 0.9rem; margin-bottom: 14px; }\n"
                    "#result { background: #18181b; border: 1px solid #27272a; border-radius: 10px; padding: 16px; }\n"
                    "#result p { color: #a1a1aa; margin-bottom: 4px; }\n"
                    "span { color: #34d399; font-weight: 600; }\n"
                ),
                "index.js": (
                    "// TODO: Implement POST request on submit-btn click\n"
                    "// POST to: https://jsonplaceholder.typicode.com/todos\n"
                    "// Body: { title: input.value, completed: false, userId: 1 }\n"
                    "// Set #response-id and #response-title from the response\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "ctp-tc-1", "name": "Clicking submit shows response-id", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const input = document.getElementById('todo-input');"
                    "const btn = document.getElementById('submit-btn');"
                    "if(!input||!btn) return 'FAIL: missing elements';"
                    "input.value = 'Test Todo';"
                    "btn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "const id = document.getElementById('response-id');"
                    "resolve(id && id.textContent.trim().length > 0 ? 'PASS' : 'FAIL: #response-id is empty after submit');"
                    "}, 2000));"
                )})
            },
            {
                "id": "ctp-tc-2", "name": "Response title matches input value", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const input = document.getElementById('todo-input');"
                    "const btn = document.getElementById('submit-btn');"
                    "input.value = 'My Fetch Todo';"
                    "btn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "const title = document.getElementById('response-title');"
                    "resolve(title && title.textContent.trim() === 'My Fetch Todo' ? 'PASS' : 'FAIL: #response-title should be \"My Fetch Todo\", got: ' + (title ? title.textContent : 'null'));"
                    "}, 2000));"
                )})
            },
        ]
    },

    # ── 6. Fetch with Async/Await ─────────────────────────────────────────────
    {
        "title": "Async/Await Fetch Todos",
        "slug": "async-await-fetch-todos",
        "short_description": "Fetch a list of todos using async/await and render only the completed ones.",
        "description": (
            "### Async/Await Fetch Todos\n\n"
            "Practice using modern `async/await` syntax with the Fetch API.\n\n"
            "#### Requirements\n"
            "- Fetch `https://jsonplaceholder.typicode.com/todos?userId=1` using `async/await`.\n"
            "- Filter only the todos where `completed === true`.\n"
            "- Render each completed todo as a `<li class=\"todo-item\">` inside `<ul id=\"todos-list\">`.\n"
            "- Show the count of completed todos in `#completed-count`.\n"
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Fetch API", "Async/Await", "Filter", "Lists"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "async function fetchTodos() { const res = await fetch(...); const data = await res.json(); }",
            "Use .filter(t => t.completed === true) to filter.",
            "Completed todos from userId=1 should be around 11.",
        ],
        "concepts": ["Async/Await", "Array Filter", "DOM Lists"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Completed Todos</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>Completed Todos</h1>\n"
                    "    <p>Total: <strong id=\"completed-count\">0</strong></p>\n"
                    "    <ul id=\"todos-list\"></ul>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; padding: 32px; }\n"
                    ".container { max-width: 500px; margin: 0 auto; }\n"
                    "h1 { font-size: 1.4rem; color: #34d399; margin-bottom: 12px; }\n"
                    "p { color: #a1a1aa; margin-bottom: 16px; }\n"
                    "strong { color: #34d399; }\n"
                    "#todos-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }\n"
                    ".todo-item { background: #18181b; border: 1px solid #27272a; border-radius: 8px; "
                    "padding: 12px 16px; color: #e4e4e7; font-size: 0.88rem; }\n"
                ),
                "index.js": (
                    "// TODO: Use async/await to fetch and render completed todos\n"
                    "// Endpoint: https://jsonplaceholder.typicode.com/todos?userId=1\n"
                    "// Filter completed === true\n"
                    "// Render each as <li class='todo-item'> in #todos-list\n"
                    "// Update #completed-count with the total\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "awt-tc-1", "name": "#completed-count is greater than 0", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('completed-count');"
                    "const count = parseInt(el ? el.textContent : '0', 10);"
                    "resolve(count > 0 ? 'PASS' : 'FAIL: #completed-count should be > 0, got ' + count);"
                    "}, 2000));"
                )})
            },
            {
                "id": "awt-tc-2", "name": ".todo-item elements rendered", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const items = document.querySelectorAll('#todos-list .todo-item');"
                    "resolve(items.length > 0 ? 'PASS' : 'FAIL: no .todo-item elements found');"
                    "}, 2000));"
                )})
            },
            {
                "id": "awt-tc-3", "name": "Count matches rendered items", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const items = document.querySelectorAll('#todos-list .todo-item');"
                    "const countEl = document.getElementById('completed-count');"
                    "const count = parseInt(countEl ? countEl.textContent : '-1', 10);"
                    "resolve(items.length === count ? 'PASS' : 'FAIL: count (' + count + ') does not match rendered items (' + items.length + ')');"
                    "}, 2000));"
                )})
            },
        ]
    },

    # ── 7. Fetch with Error Handling ──────────────────────────────────────────
    {
        "title": "Fetch Error Handling",
        "slug": "fetch-error-handling",
        "short_description": "Fetch a resource and gracefully handle 404 and network errors with user-friendly messages.",
        "description": (
            "### Fetch Error Handling\n\n"
            "Learn to handle fetch failures gracefully — a critical real-world skill.\n\n"
            "#### Requirements\n"
            "- Render a `<button id=\"fetch-btn\">Fetch Data</button>` and a `<div id=\"status\">`.\n"
            "- On click, fetch `https://jsonplaceholder.typicode.com/posts/9999` (does not exist).\n"
            "- If `response.ok` is false (404), set `#status` text to `'Error: 404 Not Found'`.\n"
            "- Wrap the fetch in `try/catch`; if the network throws, set `#status` to `'Network error'`.\n"
            "- Add class `error` to `#status` when displaying any error.\n"
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Fetch API", "Error Handling", "Try/Catch", "HTTP Status"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "fetch() itself only rejects on network failure, not on 4xx/5xx.",
            "Check response.ok — if false, throw new Error() to trigger catch.",
            "Use response.status to build the error message.",
        ],
        "concepts": ["Error Handling", "HTTP Status Codes", "Try/Catch"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 130, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Error Handling</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>Fetch Error Handling</h1>\n"
                    "    <button id=\"fetch-btn\">Fetch Data</button>\n"
                    "    <div id=\"status\"></div>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { text-align: center; }\n"
                    "h1 { font-size: 1.2rem; color: #a78bfa; margin-bottom: 20px; }\n"
                    "button { padding: 10px 24px; background: #6366f1; border: none; border-radius: 8px; "
                    "color: white; cursor: pointer; font-size: 0.9rem; margin-bottom: 16px; }\n"
                    "#status { font-size: 0.95rem; padding: 10px 16px; border-radius: 8px; min-height: 40px; }\n"
                    "#status.error { background: #2c0a0a; color: #f87171; border: 1px solid #7f1d1d; }\n"
                    "#status.success { background: #052e16; color: #34d399; border: 1px solid #14532d; }\n"
                ),
                "index.js": (
                    "// TODO: Fetch data on #fetch-btn click with error handling\n"
                    "// URL: https://jsonplaceholder.typicode.com/posts/9999\n"
                    "// If response.ok is false: set #status text to 'Error: 404 Not Found' and add class 'error'\n"
                    "// Wrap in try/catch: if network error, set 'Network error'\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "feh-tc-1", "name": "Status shows error message on 404", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const btn = document.getElementById('fetch-btn');"
                    "if(!btn) return 'FAIL: missing #fetch-btn';"
                    "btn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "const status = document.getElementById('status');"
                    "const text = status ? status.textContent.toLowerCase() : '';"
                    "resolve(text.includes('404') || text.includes('error') || text.includes('not found') ? 'PASS' : 'FAIL: #status should show 404/error message, got: ' + text);"
                    "}, 2500));"
                )})
            },
            {
                "id": "feh-tc-2", "name": "#status has .error class on failure", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const btn = document.getElementById('fetch-btn');"
                    "btn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "const status = document.getElementById('status');"
                    "resolve(status && status.classList.contains('error') ? 'PASS' : 'FAIL: #status should have class error');"
                    "}, 2500));"
                )})
            },
        ]
    },

    # ── 8. Infinite Scroll / Load More ────────────────────────────────────────
    {
        "title": "Load More Posts Button",
        "slug": "load-more-posts-button",
        "short_description": "Build a 'Load More' button that fetches the next batch of posts on each click.",
        "description": (
            "### Load More Posts Button\n\n"
            "Implement a paginated list that loads more items on demand.\n\n"
            "#### Requirements\n"
            "- On page load, fetch the first 5 posts: `https://jsonplaceholder.typicode.com/posts?_start=0&_limit=5`.\n"
            "- Render each post as `<div class=\"post\">` inside `#posts-container`.\n"
            "- A `<button id=\"load-more-btn\">Load More</button>` fetches the **next** 5 posts on each click.\n"
            "- Track the current offset and increment by 5 each time.\n"
            "- When all 100 posts are loaded, disable the `#load-more-btn`.\n"
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Fetch API", "Pagination", "State Management", "Lists"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "Use a `let offset = 0` variable and increment by 5 each click.",
            "Use _start and _limit query params: ?_start=5&_limit=5",
            "JSONPlaceholder has exactly 100 posts total.",
        ],
        "concepts": ["Pagination", "Query Parameters", "State Management"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Load More Posts</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>Posts</h1>\n"
                    "    <div id=\"posts-container\"></div>\n"
                    "    <button id=\"load-more-btn\">Load More</button>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; padding: 24px; }\n"
                    ".container { max-width: 560px; margin: 0 auto; }\n"
                    "h1 { font-size: 1.4rem; color: #a78bfa; margin-bottom: 16px; }\n"
                    ".post { background: #18181b; border: 1px solid #27272a; border-radius: 10px; "
                    "padding: 16px; margin-bottom: 10px; }\n"
                    ".post h3 { font-size: 0.95rem; color: #e4e4e7; margin-bottom: 6px; text-transform: capitalize; }\n"
                    ".post p { color: #71717a; font-size: 0.82rem; }\n"
                    "#load-more-btn { width: 100%; margin-top: 12px; padding: 12px; background: #6366f1; "
                    "border: none; border-radius: 8px; color: white; cursor: pointer; font-size: 0.9rem; }\n"
                    "#load-more-btn:disabled { background: #3f3f46; color: #71717a; cursor: not-allowed; }\n"
                ),
                "index.js": (
                    "// TODO: Implement paginated post loading\n"
                    "// 1. Fetch first 5 posts on load\n"
                    "// 2. #load-more-btn fetches next 5 on each click\n"
                    "// 3. Track offset, increment by 5\n"
                    "// 4. Disable button when offset >= 100\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "lmp-tc-1", "name": "5 posts rendered on page load", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const posts = document.querySelectorAll('#posts-container .post');"
                    "resolve(posts.length === 5 ? 'PASS' : 'FAIL: expected 5 posts on load, got ' + posts.length);"
                    "}, 1500));"
                )})
            },
            {
                "id": "lmp-tc-2", "name": "Load More adds 5 more posts", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const btn = document.getElementById('load-more-btn');"
                    "if(!btn) return resolve('FAIL: missing #load-more-btn');"
                    "btn.click();"
                    "setTimeout(() => {"
                    "const posts = document.querySelectorAll('#posts-container .post');"
                    "resolve(posts.length === 10 ? 'PASS' : 'FAIL: expected 10 posts after Load More, got ' + posts.length);"
                    "}, 1500);"
                    "}, 1500));"
                )})
            },
            {
                "id": "lmp-tc-3", "name": "Button disabled after all posts loaded", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(async resolve => {"
                    "await new Promise(r => setTimeout(r, 1500));"
                    "const btn = document.getElementById('load-more-btn');"
                    "// Click 19 more times to exhaust 100 posts"
                    "for(let i = 0; i < 19; i++) { btn.click(); await new Promise(r => setTimeout(r, 300)); }"
                    "await new Promise(r => setTimeout(r, 1000));"
                    "resolve(btn.disabled ? 'PASS' : 'FAIL: button should be disabled when all posts loaded');"
                    "});"
                )})
            },
        ]
    },

    # ── 9. Parallel Fetch with Promise.all ────────────────────────────────────
    {
        "title": "Parallel Fetch with Promise.all",
        "slug": "parallel-fetch-promise-all",
        "short_description": "Fetch user, posts, and todos simultaneously using Promise.all and display all results.",
        "description": (
            "### Parallel Fetch with Promise.all\n\n"
            "Use `Promise.all` to execute multiple API calls concurrently for better performance.\n\n"
            "#### Requirements\n"
            "- Fetch all three endpoints **simultaneously** using `Promise.all`:\n"
            "  1. `https://jsonplaceholder.typicode.com/users/1` → name in `#user-name`\n"
            "  2. `https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3` → count in `#post-count`\n"
            "  3. `https://jsonplaceholder.typicode.com/todos?userId=1&_limit=3` → count in `#todo-count`\n"
            "- All three fetches must run **in parallel**, not sequentially.\n"
            "- Show `#loading` while fetching, hide it when all are done.\n"
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Promise.all", "Fetch API", "Concurrency", "Async/Await"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "Promise.all([fetch1, fetch2, fetch3]) — pass an array of promises.",
            "Destructure results: const [user, posts, todos] = await Promise.all([...]).",
            "All 3 json() calls also need to be awaited in parallel if possible.",
        ],
        "concepts": ["Promise.all", "Parallel Requests", "Performance"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 160, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Parallel Fetch</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>Dashboard</h1>\n"
                    "    <p id=\"loading\">Fetching data...</p>\n"
                    "    <div class=\"cards\">\n"
                    "      <div class=\"card\"><h2>User</h2><p id=\"user-name\">—</p></div>\n"
                    "      <div class=\"card\"><h2>Posts</h2><p id=\"post-count\">—</p></div>\n"
                    "      <div class=\"card\"><h2>Todos</h2><p id=\"todo-count\">—</p></div>\n"
                    "    </div>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { text-align: center; width: 100%; max-width: 560px; }\n"
                    "h1 { font-size: 1.4rem; color: #a78bfa; margin-bottom: 16px; }\n"
                    "#loading { color: #71717a; font-style: italic; margin-bottom: 16px; }\n"
                    ".cards { display: flex; gap: 12px; justify-content: center; }\n"
                    ".card { background: #18181b; border: 1px solid #27272a; border-radius: 10px; "
                    "padding: 20px 24px; flex: 1; }\n"
                    ".card h2 { font-size: 0.8rem; color: #71717a; text-transform: uppercase; "
                    "letter-spacing: 0.05em; margin-bottom: 8px; }\n"
                    ".card p { font-size: 1.2rem; font-weight: 600; color: #a78bfa; }\n"
                ),
                "index.js": (
                    "// TODO: Use Promise.all to fetch all 3 endpoints in parallel\n"
                    "// 1. https://jsonplaceholder.typicode.com/users/1 → #user-name\n"
                    "// 2. https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3 → #post-count (length)\n"
                    "// 3. https://jsonplaceholder.typicode.com/todos?userId=1&_limit=3 → #todo-count (length)\n"
                    "// Show #loading while fetching, hide when done\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "pfa-tc-1", "name": "#user-name is populated", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('user-name');"
                    "resolve(el && el.textContent.trim().length > 0 && el.textContent !== '—' ? 'PASS' : 'FAIL: #user-name is empty');"
                    "}, 2000));"
                )})
            },
            {
                "id": "pfa-tc-2", "name": "#post-count and #todo-count populated", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const p = document.getElementById('post-count');"
                    "const t = document.getElementById('todo-count');"
                    "const ok = p && t && p.textContent !== '—' && t.textContent !== '—';"
                    "resolve(ok ? 'PASS' : 'FAIL: #post-count or #todo-count still shows —');"
                    "}, 2000));"
                )})
            },
            {
                "id": "pfa-tc-3", "name": "Post count is 3", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "return new Promise(resolve => setTimeout(() => {"
                    "const el = document.getElementById('post-count');"
                    "resolve(el && el.textContent.trim() === '3' ? 'PASS' : 'FAIL: expected 3, got ' + (el ? el.textContent : 'null'));"
                    "}, 2000));"
                )})
            },
        ]
    },

    # ── 10. Fetch with AbortController ────────────────────────────────────────
    {
        "title": "Cancelable Fetch with AbortController",
        "slug": "cancelable-fetch-abortcontroller",
        "short_description": "Use AbortController to cancel an in-flight fetch request when the user clicks Cancel.",
        "description": (
            "### Cancelable Fetch with AbortController\n\n"
            "Learn to cancel network requests — essential for preventing race conditions in real apps.\n\n"
            "#### Requirements\n"
            "- A `<button id=\"start-btn\">Start Fetch</button>` begins a slow fetch.\n"
            "- A `<button id=\"cancel-btn\">Cancel</button>` aborts the ongoing request.\n"
            "- Fetch `https://httpbin.org/delay/3` (3-second delay) with an `AbortController` signal.\n"
            "- Show `'Fetching...'` in `#status` when started.\n"
            "- Show `'Cancelled!'` in `#status` if aborted (catch the `AbortError`).\n"
            "- Show `'Done!'` in `#status` if the fetch completes normally.\n"
        ),
        "domain": "Frontend", "difficulty": "Hard",
        "tags": ["Fetch API", "AbortController", "Race Conditions", "Advanced"],
        "technologies": ["html", "css", "javascript"],
        "hints": [
            "const controller = new AbortController(); fetch(url, { signal: controller.signal })",
            "controller.abort() to cancel.",
            "In catch block: if(err.name === 'AbortError') handle cancellation.",
        ],
        "concepts": ["AbortController", "Race Conditions", "Error Types"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n"
                    "  <title>Cancelable Fetch</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <h1>Cancelable Fetch</h1>\n"
                    "    <div class=\"btns\">\n"
                    "      <button id=\"start-btn\">Start Fetch</button>\n"
                    "      <button id=\"cancel-btn\">Cancel</button>\n"
                    "    </div>\n"
                    "    <p id=\"status\">Idle</p>\n"
                    "  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; "
                    "min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { text-align: center; }\n"
                    "h1 { font-size: 1.2rem; color: #a78bfa; margin-bottom: 20px; }\n"
                    ".btns { display: flex; gap: 10px; justify-content: center; margin-bottom: 16px; }\n"
                    "button { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 0.9rem; }\n"
                    "#start-btn { background: #6366f1; color: white; }\n"
                    "#cancel-btn { background: #ef4444; color: white; }\n"
                    "#status { font-size: 1rem; padding: 10px 20px; border-radius: 8px; background: #18181b; "
                    "border: 1px solid #27272a; color: #a1a1aa; }\n"
                ),
                "index.js": (
                    "// TODO: Implement cancelable fetch using AbortController\n"
                    "// 1. On #start-btn click: create AbortController, fetch https://httpbin.org/delay/3\n"
                    "// 2. Set #status to 'Fetching...'\n"
                    "// 3. On #cancel-btn click: call controller.abort()\n"
                    "// 4. In catch: if AbortError, set #status to 'Cancelled!', else re-throw\n"
                    "// 5. On success: set #status to 'Done!'\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "abc-tc-1", "name": "Start button shows Fetching...", "hidden": False,
                "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const btn = document.getElementById('start-btn');"
                    "if(!btn) return 'FAIL: missing #start-btn';"
                    "btn.click();"
                    "const status = document.getElementById('status');"
                    "return status && status.textContent.toLowerCase().includes('fetch') ? 'PASS' : 'FAIL: #status should show Fetching..., got: ' + (status ? status.textContent : 'null');"
                )})
            },
            {
                "id": "abc-tc-2", "name": "Cancel button shows Cancelled!", "hidden": False,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const startBtn = document.getElementById('start-btn');"
                    "const cancelBtn = document.getElementById('cancel-btn');"
                    "if(!startBtn||!cancelBtn) return 'FAIL: missing buttons';"
                    "startBtn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "cancelBtn.click();"
                    "setTimeout(() => {"
                    "const status = document.getElementById('status');"
                    "const text = status ? status.textContent.toLowerCase() : '';"
                    "resolve(text.includes('cancel') ? 'PASS' : 'FAIL: expected Cancelled!, got: ' + text);"
                    "}, 500);"
                    "}, 200));"
                )})
            },
            {
                "id": "abc-tc-3", "name": "AbortController prevents race on re-fetch", "hidden": True,
                "weight": 3, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": (
                    "const startBtn = document.getElementById('start-btn');"
                    "const cancelBtn = document.getElementById('cancel-btn');"
                    "startBtn.click();"
                    "return new Promise(resolve => setTimeout(() => {"
                    "cancelBtn.click();"
                    "setTimeout(() => {"
                    "startBtn.click();"
                    "const status = document.getElementById('status');"
                    "const text = status ? status.textContent.toLowerCase() : '';"
                    "resolve(text.includes('fetch') ? 'PASS' : 'FAIL: new fetch should show Fetching..., got: ' + text);"
                    "}, 300);"
                    "}, 300));"
                )})
            },
        ]
    },
]


def seed_fetch_challenges():
    print("Connecting to MongoDB and seeding 10 Fetch API challenges...")
    total_added = 0
    for doc in FETCH_CHALLENGES:
        slug = doc["slug"]
        col.delete_one({"slug": slug})
        col.insert_one({
            "challenge_id": doc["slug"],
            "id": doc["slug"],
            "slug": doc["slug"],
            "title": doc["title"],
            "domain": doc["domain"],
            "difficulty": doc["difficulty"],
            "tags": doc["tags"],
            "technologies": doc["technologies"],
            "short_description": doc["short_description"],
            "description": doc["description"],
            "hints": doc["hints"],
            "concepts": doc["concepts"],
            "runtime": doc["runtime"],
            "execution_mode": doc["execution_mode"],
            "xp_reward": doc["xp_reward"],
            "estimated_time_minutes": doc["estimated_time_minutes"],
            "starter_code": doc["starter_code"],
            "test_cases": doc["test_cases"],
            "is_published": True,
            "is_featured": False,
            "is_premium": False,
        })
        visible = len([t for t in doc["test_cases"] if not t["hidden"]])
        hidden  = len([t for t in doc["test_cases"] if t["hidden"]])
        print(f"  ✓ Seeded: {slug}  ({visible} visible + {hidden} hidden test cases)")
        total_added += 1

    print(f"\n✅ Done! Seeded {total_added} Fetch API challenges.")


if __name__ == "__main__":
    seed_fetch_challenges()
