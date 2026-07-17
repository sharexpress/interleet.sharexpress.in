#!/usr/bin/env python3
"""
seed_20_frontend_challenges.py
Creates and populates 20 new high-quality Frontend challenges in MongoDB
with correct HTML, CSS, JavaScript, and behavioral browser test cases.
"""

import json
from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["interleet"]

db = get_db()
col = db["problems"]

NEW_CHALLENGES = [
    # ── 1. Star Rating Component ──────────────────────────────────────────────
    {
        "title": "Interactive Star Rating",
        "slug": "star-rating-component",
        "short_description": "Build a 5-star rating component with hover highlights and click selection.",
        "description": (
            "### Interactive Star Rating\n\n"
            "Build a star rating widget with the following requirements:\n"
            "- Render 5 star elements with class `.star` and individual IDs `#star-1` to `#star-5`.\n"
            "- Hovering over a star should highlight it and all preceding stars (add class `.highlighted`).\n"
            "- Moving the cursor away should remove highlights, unless a rating is locked/selected.\n"
            "- Clicking a star should lock the rating (add class `.selected` to the clicked star and preceding ones) and update the text inside `#rating-value` with the index (1 to 5)."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["DOM", "Events", "CSS", "UI Components"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use mouseenter/mouseleave to handle hover highlighting.", "Store the locked rating value in a variable to preserve state on mouseleave."],
        "concepts": ["DOM Manipulation", "Event Listeners", "State Management"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Star Rating</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"card\">\n    <h2>Rate this challenge</h2>\n"
                    "    <div class=\"stars-container\">\n"
                    "      <span class=\"star\" id=\"star-1\">★</span>\n"
                    "      <span class=\"star\" id=\"star-2\">★</span>\n"
                    "      <span class=\"star\" id=\"star-3\">★</span>\n"
                    "      <span class=\"star\" id=\"star-4\">★</span>\n"
                    "      <span class=\"star\" id=\"star-5\">★</span>\n"
                    "    </div>\n"
                    "    <p>Rating: <span id=\"rating-value\">0</span> / 5</p>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #f4f4f5; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".card { background: #18181b; border: 1px solid #27272a; padding: 32px; border-radius: 12px; text-align: center; max-width: 320px; }\n"
                    "h2 { font-size: 1.25rem; margin-bottom: 16px; }\n"
                    ".stars-container { display: flex; gap: 8px; justify-content: center; margin-bottom: 12px; }\n"
                    ".star { font-size: 2.5rem; cursor: pointer; color: #3f3f46; transition: color 0.15s; }\n"
                    ".star.highlighted { color: #fbbf24; }\n"
                    ".star.selected { color: #f59e0b; }\n"
                    "p { font-size: 0.95rem; color: #a1a1aa; }\n"
                    "#rating-value { font-weight: bold; color: #f4f4f5; }\n"
                ),
                "index.js": (
                    "// TODO: Implement Star Rating Component\n"
                    "// 1. Hovering (mouseenter/mouseleave) highlights stars.\n"
                    "// 2. Clicking locks the selection.\n"
                    "// 3. Update #rating-value text.\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "star-tc-1", "name": "Starts at rating 0", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const val=document.getElementById('rating-value'); return val.textContent.trim()==='0'?'PASS':'FAIL: expected 0, got '+val.textContent;"})
            },
            {
                "id": "star-tc-2", "name": "Clicking 3rd star selects 3 stars and updates text", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"stdin": "", "evaluation": "const star3=document.getElementById('star-3'); const val=document.getElementById('rating-value'); if(!star3||!val)return 'FAIL: elements not found'; star3.click(); const selected=document.querySelectorAll('.star.selected').length; if(selected!==3)return 'FAIL: expected 3 selected stars, got '+selected; return val.textContent.trim()==='3'?'PASS':'FAIL: value should be 3, got '+val.textContent;"})
            }
        ]
    },
    # ── 2. Tabbed Interface Component ─────────────────────────────────────────
    {
        "title": "Tabbed Pane Component",
        "slug": "tabbed-pane-component",
        "short_description": "Build a tabbed component where tabs toggle the visibility of content panes.",
        "description": (
            "### Tabbed Pane Component\n\n"
            "Build a tabbed card with the following requirements:\n"
            "- Render 3 tabs with class `.tab-btn` and individual IDs `#tab-1` to `#tab-3`.\n"
            "- Render 3 panes with class `.tab-pane` and individual IDs `#pane-1` to `#pane-3`.\n"
            "- Clicking a tab should add class `.active` to that tab button and remove it from all others.\n"
            "- Toggling tabs should display corresponding panes by adding `.active` class (or toggling hidden/display css state) and hiding all other panes."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Tabs", "Toggles", "CSS Layouts"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use querySelectorAll/forEach to reset all tabs/panes before applying active states.", "Map the clicked button ID index to show the matching pane."],
        "concepts": ["State Toggling", "Dynamic CSS Styling", "Class Management"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Tabs Component</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"tab-container\">\n"
                    "    <div class=\"tabs-header\">\n"
                    "      <button class=\"tab-btn active\" id=\"tab-1\">Overview</button>\n"
                    "      <button class=\"tab-btn\" id=\"tab-2\">Specifications</button>\n"
                    "      <button class=\"tab-btn\" id=\"tab-3\">Reviews</button>\n"
                    "    </div>\n"
                    "    <div class=\"tabs-content\">\n"
                    "      <div class=\"tab-pane active\" id=\"pane-1\">Overview Content</div>\n"
                    "      <div class=\"tab-pane\" id=\"pane-2\">Specs Content</div>\n"
                    "      <div class=\"tab-pane\" id=\"pane-3\">Reviews Content</div>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0a0a0c; color: #e4e4e7; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".tab-container { width: 100%; max-width: 480px; background: #18181b; border: 1px solid #27272a; border-radius: 8px; overflow: hidden; }\n"
                    ".tabs-header { display: flex; border-bottom: 1px solid #27272a; }\n"
                    ".tab-btn { flex: 1; padding: 12px; background: none; border: none; color: #a1a1aa; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.15s; }\n"
                    ".tab-btn.active { color: #6366f1; border-bottom: 2px solid #6366f1; background: #202024; }\n"
                    ".tabs-content { padding: 20px; min-height: 120px; }\n"
                    ".tab-pane { display: none; }\n"
                    ".tab-pane.active { display: block; }\n"
                ),
                "index.js": (
                    "// TODO: Implement Tab Switching Logic\n"
                    "// Listen to tab clicks, toggle active states of tab buttons and content panes.\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "tab-tc-1", "name": "Clicking second tab switches active pane", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const tab2=document.getElementById('tab-2'); const pane2=document.getElementById('pane-2'); if(!tab2||!pane2)return 'FAIL: missing elements'; tab2.click(); return pane2.classList.contains('active') && getComputedStyle(pane2).display!=='none'?'PASS':'FAIL: Pane 2 should be visible';"}),
            }
        ]
    },
    # ── 3. Modal Dialog Box ───────────────────────────────────────────────────
    {
        "title": "Modal Dialog Box",
        "slug": "modal-dialog-box",
        "short_description": "Build an overlay modal popup component triggered by a button click.",
        "description": (
            "### Modal Dialog Box\n\n"
            "Build a modal component with the following requirements:\n"
            "- Clicking `#open-modal` should make the overlay background `#modal-overlay` visible.\n"
            "- Clicking the close button `#close-modal` or clicking on the overlay container directly should hide it.\n"
            "- Pressing the `Escape` key on the keyboard should also close the modal."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Modal", "Dialog", "Keyboard Events"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use a global event listener for 'keydown' event checking key === 'Escape'.", "Toggling a class `.hidden` is the cleanest class management pattern."],
        "concepts": ["Modals", "Aesthetics", "Overlay Interfaces"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Modal Popup</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <button id=\"open-modal\">Open Modal</button>\n"
                    "  <div id=\"modal-overlay\" class=\"hidden\">\n"
                    "    <div class=\"modal\">\n"
                    "      <h3>Modal Title</h3>\n"
                    "      <p>This is a custom popup modal dialog box.</p>\n"
                    "      <button id=\"close-modal\">Close</button>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    "#open-modal { padding: 12px 24px; background: #6366f1; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; }\n"
                    "#modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center; z-index: 100; }\n"
                    ".modal { background: #18181b; border: 1px solid #27272a; padding: 24px; border-radius: 12px; max-width: 400px; text-align: center; }\n"
                    ".modal h3 { margin-bottom: 12px; }\n"
                    ".modal p { margin-bottom: 20px; color: #a1a1aa; }\n"
                    "#close-modal { padding: 8px 16px; background: #ef4444; color: white; border: none; border-radius: 6px; cursor: pointer; }\n"
                    "#modal-overlay.hidden { display: none !important; }\n"
                ),
                "index.js": (
                    "// TODO: Implement Modal Trigger, Close & Escape key handlers\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "mod-tc-1", "name": "Trigger opens modal", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const btn=document.getElementById('open-modal'); const ov=document.getElementById('modal-overlay'); if(!btn||!ov)return 'FAIL: missing elements'; btn.click(); return !ov.classList.contains('hidden')?'PASS':'FAIL: Modal overlay should be visible';"}),
            },
            {
                "id": "mod-tc-2", "name": "Close button hides modal", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const open=document.getElementById('open-modal'); const close=document.getElementById('close-modal'); const ov=document.getElementById('modal-overlay'); open.click(); close.click(); return ov.classList.contains('hidden')?'PASS':'FAIL: Modal overlay should be hidden after closing';"}),
            }
        ]
    },
    # ── 4. Accordion Component ────────────────────────────────────────────────
    {
        "title": "Collapsible Accordion",
        "slug": "collapsible-accordion",
        "short_description": "Build an accordion component that collapses content blocks upon clicking headers.",
        "description": (
            "### Collapsible Accordion\n\n"
            "Build an accordion menu with the following requirements:\n"
            "- Clicking any `.accordion-header` element should expand or collapse its corresponding `.accordion-content`.\n"
            "- Add class `.active` to the parent container `.accordion-item` of the currently open content block.\n"
            "- When an accordion item expands, all other accordion items should automatically collapse (mutual exclusion)."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Accordion", "DOM Navigation", "Dynamic Heights"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["First loop and collapse all accordion items, then toggle the state of the clicked one.", "Manage state by applying/removing a class like `.active`."],
        "concepts": ["State Isolation", "Accordion Components", "Mutual Exclusion"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Accordion</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"accordion\">\n"
                    "    <div class=\"accordion-item\">\n"
                    "      <div class=\"accordion-header\">Section 1</div>\n"
                    "      <div class=\"accordion-content\">Content of Section 1</div>\n"
                    "    </div>\n"
                    "    <div class=\"accordion-item\">\n"
                    "      <div class=\"accordion-header\">Section 2</div>\n"
                    "      <div class=\"accordion-content\">Content of Section 2</div>\n"
                    "    </div>\n"
                    "    <div class=\"accordion-item\">\n"
                    "      <div class=\"accordion-header\">Section 3</div>\n"
                    "      <div class=\"accordion-content\">Content of Section 3</div>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0f0f11; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".accordion { width: 100%; max-width: 440px; background: #1c1c1f; border: 1px solid #2e2e33; border-radius: 8px; overflow: hidden; }\n"
                    ".accordion-item { border-bottom: 1px solid #2e2e33; }\n"
                    ".accordion-item:last-child { border-bottom: none; }\n"
                    ".accordion-header { padding: 16px; background: #27272c; cursor: pointer; font-weight: 500; user-select: none; }\n"
                    ".accordion-content { padding: 0 16px; height: 0; overflow: hidden; transition: all 0.25s ease; color: #a1a1aa; font-size: 14px; }\n"
                    ".accordion-item.active .accordion-content { padding: 16px; height: auto; }\n"
                    ".accordion-item.active .accordion-header { background: #6366f1; color: white; }\n"
                ),
                "index.js": (
                    "// TODO: Implement mutual exclusion collapsible Accordion menu\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "acc-tc-1", "name": "Clicking header expands content", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const items=document.querySelectorAll('.accordion-item'); if(items.length<3)return 'FAIL: items missing'; items[0].querySelector('.accordion-header').click(); return items[0].classList.contains('active')?'PASS':'FAIL: Accordion item 1 should be active';"}),
            },
            {
                "id": "acc-tc-2", "name": "Only one item can be active at a time", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const items=document.querySelectorAll('.accordion-item'); items[0].querySelector('.accordion-header').click(); items[1].querySelector('.accordion-header').click(); const activeItems=document.querySelectorAll('.accordion-item.active'); return (activeItems.length===1 && items[1].classList.contains('active'))?'PASS':'FAIL: expected only Item 2 active. Active count: '+activeItems.length;"}),
            }
        ]
    },
    # ── 5. Interactive Shopping Cart ──────────────────────────────────────────
    {
        "title": "Interactive Shopping Cart",
        "slug": "interactive-shopping-cart",
        "short_description": "Build a shopping list interface with product lists, cart subtotals, and increments.",
        "description": (
            "### Interactive Shopping Cart\n\n"
            "Build a shopping cart with the following requirements:\n"
            "- Render item nodes with class `.product` containing buttons with class `.add-to-cart`.\n"
            "- Add selected products to the cart list `#cart-list` with individual lines `.cart-item`.\n"
            "- If a product is already in the cart, clicking 'Add' should increment the quantity in that `.cart-item` instead of duplicating rows.\n"
            "- Maintain and update the grand subtotal inside `#cart-total` (displays formatted number to 2 decimal places)."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Shopping Cart", "Subtotal Calculation", "DOM Structures"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Maintain an internal state object (representing product quantities) to match the DOM render.", "Parse numeric text content using parseFloat."],
        "concepts": ["Dynamic Templates", "Data Syncing", "State Management"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 30,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Shopping Cart</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"app\">\n"
                    "    <div class=\"products\">\n"
                    "      <div class=\"product\" data-id=\"1\" data-name=\"Book\" data-price=\"12.99\">\n"
                    "        <span>Book - $12.99</span>\n"
                    "        <button class=\"add-to-cart\">Add to Cart</button>\n"
                    "      </div>\n"
                    "      <div class=\"product\" data-id=\"2\" data-name=\"Headphones\" data-price=\"49.99\">\n"
                    "        <span>Headphones - $49.99</span>\n"
                    "        <button class=\"add-to-cart\">Add to Cart</button>\n"
                    "      </div>\n"
                    "    </div>\n"
                    "    <div class=\"cart\">\n"
                    "      <h3>Your Cart</h3>\n"
                    "      <ul id=\"cart-list\"></ul>\n"
                    "      <div class=\"total\">Total: $<span id=\"cart-total\">0.00</span></div>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0f; color: #fff; min-height: 100vh; padding: 24px; }\n"
                    ".app { display: flex; gap: 32px; max-width: 800px; margin: 0 auto; }\n"
                    ".products, .cart { flex: 1; background: #1c1c1f; border: 1px solid #2e2e33; padding: 20px; border-radius: 8px; }\n"
                    ".product { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }\n"
                    ".add-to-cart { padding: 6px 12px; background: #6366f1; color: white; border: none; border-radius: 4px; cursor: pointer; }\n"
                    "#cart-list { list-style: none; margin-bottom: 16px; min-height: 60px; }\n"
                    ".cart-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2e2e33; font-size: 14px; }\n"
                    ".total { font-weight: bold; font-size: 1.1rem; }\n"
                ),
                "index.js": (
                    "// TODO: Implement Shopping Cart operations\n"
                    "// Handle clicks on '.add-to-cart' buttons.\n"
                    "// Create or update '.cart-item' inside '#cart-list'.\n"
                    "// Recalculate and update '#cart-total' to 2 decimal places.\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "crt-tc-1", "name": "Adding elements updates total price", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const addBtns=document.querySelectorAll('.add-to-cart'); const total=document.getElementById('cart-total'); if(addBtns.length<2)return 'FAIL: missing add buttons'; addBtns[0].click(); return parseFloat(total.textContent)===12.99?'PASS':'FAIL: expected 12.99, got '+total.textContent;"}),
            },
            {
                "id": "crt-tc-2", "name": "Increment quantity instead of duplicate cart items", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const addBtns=document.querySelectorAll('.add-to-cart'); const list=document.getElementById('cart-list'); addBtns[0].click(); addBtns[0].click(); const items=list.querySelectorAll('.cart-item'); if(items.length!==1)return 'FAIL: should group same item in single line, got '+items.length+' items'; const totalVal=parseFloat(document.getElementById('cart-total').textContent); return totalVal===(12.99*3)?'PASS':'FAIL: Total price incorrect, expected 38.97, got '+totalVal;"})
            }
        ]
    },
    # ── 6. Progress Bar Controller ────────────────────────────────────────────
    {
        "title": "Progress Bar Animator",
        "slug": "progress-bar-animator",
        "short_description": "Build a controller interface to start, pause, and reset a progress bar width.",
        "description": (
            "### Progress Bar Animator\n\n"
            "Build a progress bar animator with the following requirements:\n"
            "- Clicking `#start-btn` should animate progress from its current status up to `100%`.\n"
            "- Provide status text showing the progress percentage inside `#progress-label`.\n"
            "- Clicking `#pause-btn` should immediately freeze the progress width and label value.\n"
            "- Clicking `#reset-btn` should clear animations and restore the progress width to `0%`."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Progress Bar", "setInterval", "CSS Transitions"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use setInterval to increase progress width by 1% periodically.", "Store the active interval ID in a global scope to let pause/reset clear it."],
        "concepts": ["Intervals", "CSS Dimensions", "Animations"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Progress Animator</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n"
                    "    <div class=\"progress-track\">\n"
                    "      <div id=\"progress-fill\"></div>\n"
                    "    </div>\n"
                    "    <div id=\"progress-label\">0%</div>\n"
                    "    <div class=\"controls\">\n"
                    "      <button id=\"start-btn\">Start</button>\n"
                    "      <button id=\"pause-btn\">Pause</button>\n"
                    "      <button id=\"reset-btn\">Reset</button>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; text-align: center; width: 100%; max-width: 400px; }\n"
                    ".progress-track { background: #27272a; height: 16px; border-radius: 8px; overflow: hidden; margin-bottom: 8px; position: relative; }\n"
                    "#progress-fill { background: #6366f1; width: 0%; height: 100%; transition: width 0.05s linear; }\n"
                    "#progress-label { margin-bottom: 20px; font-weight: bold; color: #a1a1aa; }\n"
                    ".controls { display: flex; gap: 8px; justify-content: center; }\n"
                    ".controls button { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; color: white; font-weight: 500; }\n"
                    "#start-btn { background: #16a34a; }\n"
                    "#pause-btn { background: #eab308; }\n"
                    "#reset-btn { background: #ef4444; }\n"
                ),
                "index.js": (
                    "// TODO: Implement progress bar state machine\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "prg-tc-1", "name": "Reset sets fill back to 0%", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const start=document.getElementById('start-btn'); const reset=document.getElementById('reset-btn'); const fill=document.getElementById('progress-fill'); const label=document.getElementById('progress-label'); if(!start||!reset||!fill||!label)return 'FAIL: missing elements'; reset.click(); return (fill.style.width==='0%' || fill.style.width==='') && label.textContent.trim()==='0%'?'PASS':'FAIL: progress not reset';"}),
            }
        ]
    },
    # ── 7. Autocomplete Search Input ──────────────────────────────────────────
    {
        "title": "Autocomplete Dropdown Filter",
        "slug": "autocomplete-dropdown-filter",
        "short_description": "Build an input component that filters and displays suggestions as the user types.",
        "description": (
            "### Autocomplete Dropdown Filter\n\n"
            "Build an autocomplete component with the following requirements:\n"
            "- Maintain a static list of strings in JavaScript: `['Apple', 'Banana', 'Blueberry', 'Cherry', 'Grape', 'Orange', 'Peach', 'Strawberry']`.\n"
            "- As the user types into `#search-input`, filter matching items and render them inside `#suggestions-list` as `<li>` elements.\n"
            "- Filter matching should be case-insensitive.\n"
            "- Clicking any suggestion item should update the input value with the suggestion text and clear the suggestions list."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Autocomplete", "Inputs", "Filter List"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Listen to the input event on #search-input.", "Empty inputs should hide/clear the suggestions list entirely."],
        "concepts": ["Event Delegation", "Array Filters", "Dynamic Suggestions"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Autocomplete</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"search-container\">\n"
                    "    <input id=\"search-input\" type=\"text\" placeholder=\"Type a fruit name...\">\n"
                    "    <ul id=\"suggestions-list\"></ul>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".search-container { width: 100%; max-width: 320px; position: relative; }\n"
                    "#search-input { width: 100%; padding: 10px 14px; background: #1c1c1f; border: 1px solid #2e2e33; border-radius: 6px; color: #fff; outline: none; }\n"
                    "#search-input:focus { border-color: #6366f1; }\n"
                    "#suggestions-list { list-style: none; background: #1c1c1f; border: 1px solid #2e2e33; border-top: none; border-radius: 0 0 6px 6px; overflow: hidden; position: absolute; width: 100%; z-index: 10; }\n"
                    "#suggestions-list li { padding: 10px; cursor: pointer; font-size: 14px; color: #a1a1aa; transition: background 0.15s; }\n"
                    "#suggestions-list li:hover { background: #27272c; color: #fff; }\n"
                ),
                "index.js": (
                    "const FRUITS = ['Apple', 'Banana', 'Blueberry', 'Cherry', 'Grape', 'Orange', 'Peach', 'Strawberry'];\n\n"
                    "// TODO: Implement autocomplete filter list\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "aut-tc-1", "name": "Typing 'blue' lists blueberry suggestion", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const input=document.getElementById('search-input'); const list=document.getElementById('suggestions-list'); if(!input||!list)return 'FAIL: missing elements'; input.value='blue'; input.dispatchEvent(new Event('input')); const items=list.querySelectorAll('li'); return (items.length===1 && items[0].textContent.includes('Blueberry'))?'PASS':'FAIL: expected 1 matching item (Blueberry), got '+items.length;"}),
            },
            {
                "id": "aut-tc-2", "name": "Clicking list updates input field", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const input=document.getElementById('search-input'); const list=document.getElementById('suggestions-list'); input.value='blue'; input.dispatchEvent(new Event('input')); const suggestion=list.querySelector('li'); if(!suggestion)return 'FAIL: no suggestion found'; suggestion.click(); return (input.value==='Blueberry' && list.querySelectorAll('li').length===0)?'PASS':'FAIL: input value should update to Blueberry and list clear, got input='+input.value;"})
            }
        ]
    },
    # ── 8. Word & Character Text Counter ──────────────────────────────────────
    {
        "title": "Text Analyzer & Counter",
        "slug": "text-analyzer-counter",
        "short_description": "Build a real-time textarea character, word, and reading time counter.",
        "description": (
            "### Text Analyzer & Counter\n\n"
            "Build a text analyzer component with the following requirements:\n"
            "- Capture keystrokes in `#text-input` in real time.\n"
            "- Update `#char-count` with the total number of characters (including whitespaces/newlines).\n"
            "- Update `#word-count` with the total number of words (whitespaces, line breaks, or punctuation separators should split words correctly, and empty lines/inputs must output `0`).\n"
            "- Calculate and display the average estimated reading time inside `#reading-time` (assuming an average speed of 200 words per minute)."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Textarea", "Keystrokes", "String Splitting"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Split string values by regex `\\s+` to detect word boundaries.", "Filters are needed to remove empty array items from string splits."],
        "concepts": ["String Analysis", "Real-Time Updates", "Regex"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 120, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Text Analyzer</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"analyzer-card\">\n"
                    "    <textarea id=\"text-input\" placeholder=\"Type or paste your text here...\"></textarea>\n"
                    "    <div class=\"stats\">\n"
                    "      <div class=\"stat\">Words: <span id=\"word-count\">0</span></div>\n"
                    "      <div class=\"stat\">Characters: <span id=\"char-count\">0</span></div>\n"
                    "      <div class=\"stat\">Reading Time: <span id=\"reading-time\">0.0</span> min</div>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0a0a0c; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".analyzer-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; width: 100%; max-width: 440px; }\n"
                    "textarea { width: 100%; height: 160px; background: #121214; border: 1px solid #2e2e33; border-radius: 6px; padding: 12px; color: #fff; resize: none; outline: none; font-size: 14px; margin-bottom: 16px; }\n"
                    "textarea:focus { border-color: #6366f1; }\n"
                    ".stats { display: flex; justify-content: space-between; background: #27272c; padding: 12px; border-radius: 6px; font-size: 13px; color: #a1a1aa; }\n"
                    ".stat span { font-weight: bold; color: #fff; }\n"
                ),
                "index.js": (
                    "// TODO: Implement Character, Word, and Reading Time analysis in real-time\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "cnt-tc-1", "name": "Typing updates counts in real-time", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const input=document.getElementById('text-input'); const charVal=document.getElementById('char-count'); const wordVal=document.getElementById('word-count'); if(!input||!charVal||!wordVal)return 'FAIL: missing elements'; input.value='Hello, welcome to Interleet!'; input.dispatchEvent(new Event('input')); return (charVal.textContent.trim()==='29' && wordVal.textContent.trim()==='4')?'PASS':'FAIL: expected char 29, words 4, got char='+charVal.textContent+', words='+wordVal.textContent;"}),
            }
        ]
    },
    # ── 9. Image Slideshow Carousel ───────────────────────────────────────────
    {
        "title": "Image Slider Carousel",
        "slug": "image-slider-carousel",
        "short_description": "Build an image carousel widget with Next, Prev, and slide position indicator dots.",
        "description": (
            "### Image Slider Carousel\n\n"
            "Build an image slider with the following requirements:\n"
            "- Implement carousel pages with class `.slide`. Currently active slide should have class `.active`.\n"
            "- Clicking `#next-btn` should display the next slide (loops to index 0 on reaching the end).\n"
            "- Clicking `#prev-btn` should display the previous slide (loops to the last index on reaching index 0).\n"
            "- Display indicator dots inside `#dots-container` with class `.dot` matching the number of slides. Clicking any dot should jump to the corresponding slide."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Carousel", "Sliders", "Indicators"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Maintain an active index state integer variable.", "Toggle the active class on active slides and dots simultaneously."],
        "concepts": ["State Syncing", "Active Classes", "DOM Layouts"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Image Slider</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"carousel-container\">\n"
                    "    <div class=\"slides\">\n"
                    "      <div class=\"slide active\" style=\"background: #ef4444;\">Slide 1</div>\n"
                    "      <div class=\"slide\" style=\"background: #3b82f6;\">Slide 2</div>\n"
                    "      <div class=\"slide\" style=\"background: #10b981;\">Slide 3</div>\n"
                    "    </div>\n"
                    "    <button id=\"prev-btn\" class=\"nav-btn\">◀</button>\n"
                    "    <button id=\"next-btn\" class=\"nav-btn\">▶</button>\n"
                    "    <div id=\"dots-container\"></div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".carousel-container { position: relative; width: 320px; height: 200px; border-radius: 8px; overflow: hidden; }\n"
                    ".slides { width: 100%; height: 100%; display: flex; position: relative; }\n"
                    ".slide { position: absolute; width: 100%; height: 100%; display: none; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; }\n"
                    ".slide.active { display: flex; }\n"
                    ".nav-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); border: none; color: white; padding: 12px; cursor: pointer; z-index: 10; }\n"
                    "#prev-btn { left: 0; }\n"
                    "#next-btn { right: 0; }\n"
                    "#dots-container { position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; z-index: 10; }\n"
                    ".dot { width: 8px; height: 8px; background: rgba(255,255,255,0.4); border-radius: 50%; cursor: pointer; }\n"
                    ".dot.active { background: white; }\n"
                ),
                "index.js": (
                    "// TODO: Populate #dots-container based on number of slides, then implement slides/dots switching logic\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "car-tc-1", "name": "Indicators exist on page load", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const dots=document.querySelectorAll('.dot'); return dots.length===3?'PASS':'FAIL: expected 3 dots got '+dots.length;"}),
            },
            {
                "id": "car-tc-2", "name": "Next button loop logic behaves correctly", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const next=document.getElementById('next-btn'); const slides=document.querySelectorAll('.slide'); if(!next||slides.length<3)return 'FAIL: missing elements'; next.click(); next.click(); next.click(); return slides[0].classList.contains('active')?'PASS':'FAIL: Expected active slide index to loop back to 0';"}),
            }
        ]
    },
    # ── 10. Dark & Light Theme Switcher ───────────────────────────────────────
    {
        "title": "Dark Theme Toggle",
        "slug": "dark-theme-toggle",
        "short_description": "Build a toggle component that changes document theme classes and persists preferences in localStorage.",
        "description": (
            "### Dark Theme Toggle\n\n"
            "Build a theme switcher button with the following requirements:\n"
            "- Clicking `#theme-toggle` should add the class `.dark-theme` to `document.body` if not present, or remove it if it is.\n"
            "- Save the user's selected preference inside `localStorage` under the key `theme` as `'dark'` or `'light'`.\n"
            "- On initial page load, check `localStorage` and correctly restore the selected theme."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Themes", "localStorage", "Class Manipulation"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use body.classList.toggle('dark-theme') to toggle classes.", "Load matching key value using localStorage.getItem('theme') during boot initialization."],
        "concepts": ["State Persistence", "Themes Selection", "DOM APIs"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Theme Toggle</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"theme-card\">\n"
                    "    <h1>Interleet Settings</h1>\n"
                    "    <button id=\"theme-toggle\">Switch Theme</button>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #fafafa; color: #1c1c1f; min-height: 100vh; display: flex; align-items: center; justify-content: center; transition: all 0.25s; }\n"
                    "body.dark-theme { background: #0c0c0e; color: #fff; }\n"
                    ".theme-card { padding: 32px; background: white; border: 1px solid #e4e4e7; border-radius: 8px; text-align: center; }\n"
                    "body.dark-theme .theme-card { background: #18181b; border-color: #27272a; }\n"
                    "#theme-toggle { padding: 8px 16px; background: #6366f1; color: white; border: none; border-radius: 6px; cursor: pointer; margin-top: 16px; }\n"
                ),
                "index.js": (
                    "// TODO: Implement toggle theme state and localStorage persistence\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "thm-tc-1", "name": "Toggle changes class and updates localStorage", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const toggle=document.getElementById('theme-toggle'); if(!toggle)return 'FAIL: missing toggle button'; localStorage.clear(); toggle.click(); const hasDarkClass=document.body.classList.contains('dark-theme'); const storedTheme=localStorage.getItem('theme'); return (hasDarkClass && storedTheme==='dark')?'PASS':'FAIL: theme class or localStorage not matching';"}),
            }
        ]
    },
    # ── 11. Responsive Mobile Navbar ──────────────────────────────────────────
    {
        "title": "Responsive Menu Drawer",
        "slug": "responsive-menu-drawer",
        "short_description": "Build a responsive drawer navigation menu with mobile hamburger triggers.",
        "description": (
            "### Responsive Menu Drawer\n\n"
            "Build a mobile menu drawer component with the following requirements:\n"
            "- Clicking `#hamburger-btn` should show the navigation menu container `#menu-drawer` by adding `.open` class.\n"
            "- Clicking any link `.nav-link` or clicking the overlay backdrop `#drawer-overlay` should close the drawer (remove `.open` class)."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Navigation", "Hamburger", "Drawers"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Toggle open class on both #menu-drawer and #drawer-overlay.", "Make sure overlays check clicks directly."],
        "concepts": ["Responsive Navigation", "Aesthetics", "Events Propagation"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Menu Drawer</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <nav class=\"navbar\">\n"
                    "    <button id=\"hamburger-btn\">☰</button>\n"
                    "  </nav>\n"
                    "  <div id=\"drawer-overlay\" class=\"hidden\"></div>\n"
                    "  <div id=\"menu-drawer\" class=\"hidden\">\n"
                    "    <a href=\"#\" class=\"nav-link\">Dashboard</a>\n"
                    "    <a href=\"#\" class=\"nav-link\">Challenges</a>\n"
                    "    <a href=\"#\" class=\"nav-link\">Settings</a>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; }\n"
                    ".navbar { height: 60px; background: #1c1c1f; display: flex; align-items: center; padding: 0 20px; }\n"
                    "#hamburger-btn { font-size: 24px; background: none; border: none; color: white; cursor: pointer; }\n"
                    "#drawer-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); z-index: 90; display: none; }\n"
                    "#drawer-overlay.open { display: block; }\n"
                    "#menu-drawer { position: fixed; top: 0; left: -260px; width: 260px; height: 100vh; background: #18181b; display: flex; flex-direction: column; padding: 24px; gap: 16px; z-index: 100; transition: left 0.25s ease; }\n"
                    "#menu-drawer.open { left: 0; }\n"
                    ".nav-link { color: #a1a1aa; text-decoration: none; font-size: 16px; }\n"
                    ".nav-link:hover { color: white; }\n"
                ),
                "index.js": (
                    "// TODO: Implement drawer toggles\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "nav-tc-1", "name": "Hamburger click opens drawer", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const ham=document.getElementById('hamburger-btn'); const drawer=document.getElementById('menu-drawer'); if(!ham||!drawer)return 'FAIL: missing elements'; ham.click(); return drawer.classList.contains('open')?'PASS':'FAIL: Drawer not open';"}),
            }
        ]
    },
    # ── 12. Virtual Number Pad ────────────────────────────────────────────────
    {
        "title": "Virtual PIN Pad",
        "slug": "virtual-pin-pad",
        "short_description": "Build a secure virtual keypad PIN input with clear and backspace operations.",
        "description": (
            "### Virtual PIN Pad\n\n"
            "Build a secure virtual input pad with the following requirements:\n"
            "- Clicking numeric buttons `.pin-key` should append their numbers to the display input `#pin-display`.\n"
            "- Display has a maximum length of 4 characters. Extra characters must be ignored.\n"
            "- Clicking the backspace button `#pin-back` should delete the last character from `#pin-display`.\n"
            "- Clicking the clear button `#pin-clear` should reset `#pin-display` value back to empty."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["PIN Pad", "Virtual Keyboard", "Limiting Value"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Limit input value modification by checking string length <= 4.", "Use slice(0, -1) for backspace character removal."],
        "concepts": ["Inputs Processing", "Security Widgets", "Click Listeners"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>PIN Pad</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"keypad-card\">\n"
                    "    <input id=\"pin-display\" type=\"password\" readonly>\n"
                    "    <div class=\"grid\">\n"
                    "      <button class=\"pin-key\">1</button><button class=\"pin-key\">2</button><button class=\"pin-key\">3</button>\n"
                    "      <button class=\"pin-key\">4</button><button class=\"pin-key\">5</button><button class=\"pin-key\">6</button>\n"
                    "      <button class=\"pin-key\">7</button><button class=\"pin-key\">8</button><button class=\"pin-key\">9</button>\n"
                    "      <button id=\"pin-clear\">C</button><button class=\"pin-key\">0</button><button id=\"pin-back\">⌫</button>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".keypad-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; max-width: 280px; text-align: center; }\n"
                    "#pin-display { width: 100%; height: 50px; background: #121214; border: 1px solid #2e2e33; border-radius: 6px; text-align: center; font-size: 1.5rem; letter-spacing: 6px; color: #fff; margin-bottom: 16px; outline: none; }\n"
                    ".grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }\n"
                    ".grid button { aspect-ratio: 1; border: 1px solid #2e2e33; border-radius: 50%; background: #27272c; color: white; font-size: 1.2rem; cursor: pointer; transition: all 0.1s; }\n"
                    ".grid button:hover { background: #6366f1; }\n"
                ),
                "index.js": (
                    "// TODO: Implement secure PIN entry keypad logic\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "pin-tc-1", "name": "Key clicks populate display and respect max length limit of 4", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const keys=document.querySelectorAll('.pin-key'); const disp=document.getElementById('pin-display'); if(keys.length<10||!disp)return 'FAIL: missing elements'; keys[0].click(); keys[1].click(); keys[2].click(); keys[3].click(); keys[4].click(); return disp.value==='1234'?'PASS':'FAIL: expected 1234 (max length), got '+disp.value;"}),
            }
        ]
    },
    # ── 13. Dynamic Password Strength Checklist ────────────────────────────────
    {
        "title": "Password Complexity Rules",
        "slug": "password-complexity-rules",
        "short_description": "Build a password strength feedback card verifying criteria lists as user inputs keys.",
        "description": (
            "### Password Complexity Rules\n\n"
            "Build a password complexity feedback list with the following requirements:\n"
            "- Listen to character inputs in `#pwd-input`.\n"
            "- Validate password complexity rules and toggle class `.valid` (for pass) or `.invalid` (for failure) on the respective checkbox elements:\n"
            "  1. Minimum 8 characters in length (`#rule-length`)\n"
            "  2. Contains at least one digit character (`#rule-digit`)\n"
            "  3. Contains at least one uppercase character (`#rule-uppercase`)\n"
            "- Submit button `#submit-btn` should remain `disabled` until all three rules pass."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Forms", "Passwords", "Validation Rules"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use regex tests: `\\d` for digit and `[A-Z]` for uppercase check.", "Enable buttons by setting disabled attribute to false."],
        "concepts": ["Real-time feedback", "Complex Validators", "Regular Expressions"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Password Validator</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"validator-card\">\n"
                    "    <input id=\"pwd-input\" type=\"password\" placeholder=\"Enter password\">\n"
                    "    <ul class=\"rules-list\">\n"
                    "      <li id=\"rule-length\" class=\"invalid\">Min 8 characters</li>\n"
                    "      <li id=\"rule-digit\" class=\"invalid\">Contains a digit</li>\n"
                    "      <li id=\"rule-uppercase\" class=\"invalid\">Contains an uppercase</li>\n"
                    "    </ul>\n"
                    "    <button id=\"submit-btn\" disabled>Sign Up</button>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".validator-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; width: 100%; max-width: 320px; }\n"
                    "#pwd-input { width: 100%; padding: 10px 14px; background: #121214; border: 1px solid #2e2e33; border-radius: 6px; color: #fff; margin-bottom: 16px; outline: none; }\n"
                    ".rules-list { list-style: none; margin-bottom: 20px; display: flex; flex-direction: column; gap: 8px; font-size: 14px; }\n"
                    ".rules-list li.invalid { color: #ef4444; text-decoration: line-through; }\n"
                    ".rules-list li.valid { color: #22c55e; text-decoration: none; }\n"
                    "#submit-btn { width: 100%; padding: 10px; background: #6366f1; border: none; color: white; border-radius: 6px; cursor: pointer; }\n"
                    "#submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }\n"
                ),
                "index.js": (
                    "// TODO: Implement complexity verification checking password constraints\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "pwd-tc-1", "name": "Validating complex string unlocks submit button", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const input=document.getElementById('pwd-input'); const submit=document.getElementById('submit-btn'); if(!input||!submit)return 'FAIL: missing elements'; input.value='Interleet2026'; input.dispatchEvent(new Event('input')); return submit.disabled===false?'PASS':'FAIL: expected submit button enabled';"}),
            }
        ]
    },
    # ── 14. Custom Styled Dropdown ────────────────────────────────────────────
    {
        "title": "Custom Styled Select Menu",
        "slug": "custom-styled-select-menu",
        "short_description": "Build a custom, styled dropdown select menu alternative to native elements.",
        "description": (
            "### Custom Styled Select Menu\n\n"
            "Build an accessible custom dropdown select component with the following requirements:\n"
            "- Clicking `#select-trigger` toggles class `.open` on `#select-options` list container.\n"
            "- Selecting any list item `.select-option` should update text of `#select-value` with option data value attribute.\n"
            "- Add class `.selected` to selected option, removing it from any other.\n"
            "- Clicking outside the select menu should close the options list dropdown."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Dropdowns", "Dynamic Styles", "Click Outwards"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use e.stopPropagation() inside trigger listener to prevent immediate window close triggers.", "Listen to click event on window object to close list."],
        "concepts": ["Event Bubbling", "Custom Select Elements", "DOM Event Flow"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Custom Select</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"custom-select\" id=\"select-container\">\n"
                    "    <div id=\"select-trigger\">\n"
                    "      <span id=\"select-value\">Select language</span>\n"
                    "      <span class=\"arrow\">▼</span>\n"
                    "    </div>\n"
                    "    <ul id=\"select-options\" class=\"hidden\">\n"
                    "      <li class=\"select-option\" data-value=\"JavaScript\">JavaScript</li>\n"
                    "      <li class=\"select-option\" data-value=\"Python\">Python</li>\n"
                    "      <li class=\"select-option\" data-value=\"Rust\">Rust</li>\n"
                    "    </ul>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".custom-select { width: 220px; position: relative; }\n"
                    "#select-trigger { background: #1c1c1f; border: 1px solid #2e2e33; padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; cursor: pointer; user-select: none; }\n"
                    "#select-options { list-style: none; background: #1c1c1f; border: 1px solid #2e2e33; border-top: none; border-radius: 0 0 6px 6px; overflow: hidden; position: absolute; width: 100%; z-index: 10; margin-top: 2px; }\n"
                    "#select-options.hidden { display: none !important; }\n"
                    ".select-option { padding: 12px; cursor: pointer; transition: background 0.15s; }\n"
                    ".select-option:hover { background: #27272c; }\n"
                    ".select-option.selected { color: #6366f1; font-weight: bold; background: #202024; }\n"
                ),
                "index.js": (
                    "// TODO: Implement custom styled select options selector\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "sel-tc-1", "name": "Option click updates select value header and toggles selection class", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const opt=document.querySelector('.select-option'); const triggerVal=document.getElementById('select-value'); if(!opt||!triggerVal)return 'FAIL: missing elements'; opt.click(); return (triggerVal.textContent==='JavaScript' && opt.classList.contains('selected'))?'PASS':'FAIL: expected JavaScript selected state';"}),
            }
        ]
    },
    # ── 15. Drag and Drop Files Checklist ─────────────────────────────────────
    {
        "title": "Drag & Drop File Upload",
        "slug": "drag-drop-file-upload",
        "short_description": "Build a drag-and-drop file upload zone that lists uploaded files.",
        "description": (
            "### Drag & Drop File Upload\n\n"
            "Build a file upload zone with the following requirements:\n"
            "- Implement a drag over effect by adding a class `.drag-over` to `#drop-zone` during dragging.\n"
            "- Dropping files on `#drop-zone` (or selecting via input `#file-input`) should list files under `#file-list`.\n"
            "- List item nodes `.file-item` should show the file name and file size."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["File Upload", "Drag and Drop", "File Reader"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Prevent default behavior for 'dragover' and 'drop' events.", "Access files using e.dataTransfer.files inside 'drop' handler."],
        "concepts": ["Drag & Drop Web API", "File System API", "Upload Interfaces"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>File Drop</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"uploader-card\">\n"
                    "    <div id=\"drop-zone\">\n"
                    "      <p>Drag & drop files here or click to select</p>\n"
                    "      <input type=\"file\" id=\"file-input\" multiple class=\"hidden\">\n"
                    "    </div>\n"
                    "    <ul id=\"file-list\"></ul>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".uploader-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; width: 100%; max-width: 400px; text-align: center; }\n"
                    "#drop-zone { border: 2px dashed #2e2e33; padding: 32px; border-radius: 6px; cursor: pointer; transition: all 0.15s; margin-bottom: 16px; }\n"
                    "#drop-zone.drag-over { border-color: #6366f1; background: rgba(99, 102, 241, 0.05); }\n"
                    "#file-list { list-style: none; text-align: left; display: flex; flex-direction: column; gap: 8px; }\n"
                    ".file-item { display: flex; justify-content: space-between; padding: 8px 12px; background: #121214; border: 1px solid #2e2e33; border-radius: 4px; font-size: 13px; }\n"
                    ".hidden { display: none !important; }\n"
                ),
                "index.js": (
                    "// TODO: Implement drag and drop upload area + list uploaded file structures\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "drg-tc-1", "name": "Drop zone toggles drag-over status class", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const drop=document.getElementById('drop-zone'); if(!drop)return 'FAIL: missing elements'; drop.dispatchEvent(new Event('dragover')); return drop.classList.contains('drag-over')?'PASS':'FAIL: expected dragover highlight class';"}),
            }
        ]
    },
    # ── 16. Interactive Quiz Widget ───────────────────────────────────────────
    {
        "title": "Interactive Quiz Widget",
        "slug": "interactive-quiz-widget",
        "short_description": "Build a dynamic multi-step quiz module showing score on final submit.",
        "description": (
            "### Interactive Quiz Widget\n\n"
            "Build a dynamic quiz card component with the following requirements:\n"
            "- Loop and display questions from the array structure `[{q: '...', choices: [...], ans: index}...]`.\n"
            "- Load first question into `#question-text` and options into `#option-buttons` container.\n"
            "- Handle option clicks: increase score if correct, load next question instantly.\n"
            "- Display score outcome out of total questions inside `#score-box` on completing all questions."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Quiz", "DOM updates", "State Management"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Store state indexes inside integer variables.", "Conditionally hide questions wrapper and show score screen on completion."],
        "concepts": ["Dynamic DOM renders", "Game loops", "UI Screen states"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Quiz Widget</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"quiz-card\">\n"
                    "    <div id=\"quiz-wrapper\">\n"
                    "      <h3 id=\"question-text\">Loading...</h3>\n"
                    "      <div id=\"option-buttons\"></div>\n"
                    "    </div>\n"
                    "    <div id=\"score-box\" class=\"hidden\"></div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".quiz-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; width: 100%; max-width: 420px; }\n"
                    "#question-text { margin-bottom: 20px; font-weight: 600; }\n"
                    "#option-buttons { display: flex; flex-direction: column; gap: 8px; }\n"
                    ".option-btn { width: 100%; padding: 12px; background: #27272c; border: 1px solid #2e2e33; border-radius: 6px; color: white; cursor: pointer; text-align: left; }\n"
                    ".option-btn:hover { background: #6366f1; }\n"
                    "#score-box { text-align: center; font-size: 1.25rem; font-weight: bold; padding: 16px 0; }\n"
                    ".hidden { display: none !important; }\n"
                ),
                "index.js": (
                    "const QUESTIONS = [\n"
                    "  { q: 'Which tag is used for inline JavaScript?', choices: ['<script>', '<javascript>', '<js>', '<code_block>'], ans: 0 },\n"
                    "  { q: 'Which CSS property handles layout flexbox?', choices: ['float', 'align', 'display', 'grid'], ans: 2 }\n"
                    "];\n\n"
                    "// TODO: Render questions sequentially and output result in #score-box on completion\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "qiz-tc-1", "name": "Completing quiz outputs final score", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const optButtons=document.getElementById('option-buttons'); if(!optButtons)return 'FAIL: missing option container'; let btns=optButtons.querySelectorAll('.option-btn'); if(btns.length===0)return 'FAIL: quiz not loaded'; btns[0].click(); btns=optButtons.querySelectorAll('.option-btn'); btns[2].click(); const scoreBox=document.getElementById('score-box'); return (scoreBox && !scoreBox.classList.contains('hidden') && scoreBox.textContent.includes('2'))?'PASS':'FAIL: expected score box showing 2';"}),
            }
        ]
    },
    # ── 17. Dynamic Table Paginator ───────────────────────────────────────────
    {
        "title": "Table Pagination & Search",
        "slug": "table-pagination-search",
        "short_description": "Build a paginated user list table with searchable inputs.",
        "description": (
            "### Table Pagination & Search\n\n"
            "Build a paginated user directory table with the following requirements:\n"
            "- Implement searching via `#filter-input`. Matching records should filter table rows dynamically.\n"
            "- Display precisely `2` records per page. Add buttons `#prev-page` and `#next-page` to paginating active records.\n"
            "- Display current page number details inside `#page-label` in format `Page X`.\n"
            "- Row templates `.user-row` should display the name and role of matched records."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Pagination", "Tables", "Filter Logic"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Calculate slice offsets using page index multiplier: start = (page-1) * limit.", "Apply slice method directly on filtered results array."],
        "concepts": ["Data Lists Pagination", "Aesthetics", "Arrays offsets"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 30,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>User Table</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"table-card\">\n"
                    "    <input id=\"filter-input\" type=\"text\" placeholder=\"Search users...\">\n"
                    "    <table id=\"users-table\">\n"
                    "      <thead>\n"
                    "        <tr><th>Name</th><th>Role</th></tr>\n"
                    "      </thead>\n"
                    "      <tbody id=\"table-body\"></tbody>\n"
                    "    </table>\n"
                    "    <div class=\"pagination-bar\">\n"
                    "      <button id=\"prev-page\">Prev</button>\n"
                    "      <span id=\"page-label\">Page 1</span>\n"
                    "      <button id=\"next-page\">Next</button>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0a0a0c; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".table-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 20px; border-radius: 8px; width: 100%; max-width: 440px; }\n"
                    "#filter-input { width: 100%; padding: 8px 12px; background: #121214; border: 1px solid #2e2e33; border-radius: 6px; color: #fff; margin-bottom: 16px; outline: none; }\n"
                    "table { width: 100%; border-collapse: collapse; margin-bottom: 16px; }\n"
                    "th, td { text-align: left; padding: 10px; border-bottom: 1px solid #2e2e33; font-size: 14px; }\n"
                    "th { color: #6366f1; font-weight: bold; }\n"
                    ".pagination-bar { display: flex; justify-content: space-between; align-items: center; }\n"
                    ".pagination-bar button { padding: 6px 12px; background: #27272c; border: 1px solid #2e2e33; border-radius: 4px; color: white; cursor: pointer; }\n"
                    "#page-label { font-size: 13px; color: #a1a1aa; }\n"
                ),
                "index.js": (
                    "const USERS = [\n"
                    "  { name: 'Alice Smith', role: 'Engineer' },\n"
                    "  { name: 'Bob Jones', role: 'Designer' },\n"
                    "  { name: 'Charlie Miller', role: 'Manager' },\n"
                    "  { name: 'David Wilson', role: 'Intern' }\n"
                    "];\n\n"
                    "// TODO: Render paginated table rows (2 per page), handle search and paginating buttons\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "tbl-tc-1", "name": "Next button correctly switches page", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const next=document.getElementById('next-page'); const label=document.getElementById('page-label'); const body=document.getElementById('table-body'); if(!next||!label||!body)return 'FAIL: missing elements'; next.click(); const rows=body.querySelectorAll('tr'); return (label.textContent.trim()==='Page 2' && rows.length===2)?'PASS':'FAIL: expected Page 2 with 2 user rows';"}),
            }
        ]
    },
    # ── 18. Ticking Countdown Timer Widget ─────────────────────────────────────
    {
        "title": "Ticking Countdown Timer",
        "slug": "ticking-countdown-timer",
        "short_description": "Build a countdown timer component displaying elapsed seconds in MM:SS.",
        "description": (
            "### Ticking Countdown Timer\n\n"
            "Build a countdown widget with the following requirements:\n"
            "- Enter numeric count values (seconds) inside `#timer-input`.\n"
            "- Clicking `#start-timer` should start countdown ticking down by 1 second periodically.\n"
            "- Display formatted time string inside `#timer-display` in format `MM:SS` (e.g. `01:45`).\n"
            "- If the countdown ends (reaches `00:00`), clear intervals and append class `.finished` to `#timer-display`."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["Countdown", "Timer", "Time Format"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Format seconds inside helper functions: Math.floor(sec/60) and sec % 60.", "Clear running timeouts/intervals on completion."],
        "concepts": ["Ticking Intervals", "String padding helper methods", "Elapsed States"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Timer Widget</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"timer-card\">\n"
                    "    <input id=\"timer-input\" type=\"number\" placeholder=\"Seconds (e.g. 90)\">\n"
                    "    <div id=\"timer-display\">00:00</div>\n"
                    "    <button id=\"start-timer\">Start Timer</button>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".timer-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; text-align: center; width: 100%; max-width: 320px; }\n"
                    "#timer-input { width: 100%; padding: 10px 14px; background: #121214; border: 1px solid #2e2e33; border-radius: 6px; color: #fff; outline: none; margin-bottom: 16px; }\n"
                    "#timer-display { font-size: 3rem; font-weight: bold; margin-bottom: 20px; font-family: monospace; color: #6366f1; }\n"
                    "#timer-display.finished { color: #ef4444; animation: blink 1s step-end infinite; }\n"
                    "#start-timer { padding: 10px 20px; background: #16a34a; border: none; color: white; border-radius: 6px; cursor: pointer; font-weight: bold; }\n"
                ),
                "index.js": (
                    "// TODO: Implement ticking countdown timer updating formatted display\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "tmr-tc-1", "name": "Inputs set correctly format displays", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const input=document.getElementById('timer-input'); const start=document.getElementById('start-timer'); const disp=document.getElementById('timer-display'); if(!input||!start||!disp)return 'FAIL: missing elements'; input.value='90'; start.click(); return disp.textContent.trim()==='01:30'?'PASS':'FAIL: expected 01:30, got '+disp.textContent;"}),
            }
        ]
    },
    # ── 19. Simple Memory Match Game ──────────────────────────────────────────
    {
        "title": "Memory Match Game",
        "slug": "memory-matching-game",
        "short_description": "Build a grid memory matching game tracking flipped cards and pairs.",
        "description": (
            "### Memory Match Game\n\n"
            "Build a simple memory puzzle game board with the following requirements:\n"
            "- Render a 4-card matching board inside `#game-board` with class `.card`.\n"
            "- Clicking a `.card` should add class `.flipped` exposing its text value.\n"
            "- Allow exactly 2 cards to be flipped at a time. If they match, keep them open (add class `.matched`). If they do not match, flip them back (remove `.flipped` class after a 500ms delay).\n"
            "- Output win message text inside `#win-label` once all pairs are matched."
        ),
        "domain": "Frontend", "difficulty": "Hard",
        "tags": ["Memory Match", "Grid Puzzle", "SetTimeout"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Store matched values and active flips in separate arrays.", "Use setTimeout delay when flipping back mismatching choices."],
        "concepts": ["State Machine Layouts", "Event Lock State", "Timers Control"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 200, "estimated_time_minutes": 45,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Memory Match</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"game-card\">\n"
                    "    <div id=\"game-board\">\n"
                    "      <div class=\"card\" data-symbol=\"A\">?</div>\n"
                    "      <div class=\"card\" data-symbol=\"B\">?</div>\n"
                    "      <div class=\"card\" data-symbol=\"A\">?</div>\n"
                    "      <div class=\"card\" data-symbol=\"B\">?</div>\n"
                    "    </div>\n"
                    "    <h3 id=\"win-label\" class=\"hidden\">You Win!</h3>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".game-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; text-align: center; }\n"
                    "#game-board { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }\n"
                    ".card { width: 80px; height: 80px; background: #27272c; border: 1px solid #2e2e33; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; cursor: pointer; user-select: none; }\n"
                    ".card.flipped { background: #6366f1; color: white; }\n"
                    ".card.matched { background: #16a34a; cursor: default; }\n"
                    "#win-label { color: #16a34a; font-weight: bold; }\n"
                ),
                "index.js": (
                    "// TODO: Implement Card flipping memory match logic\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "mem-tc-1", "name": "Flipping card adds class", "hidden": False, "weight": 1, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const card=document.querySelector('.card'); if(!card)return 'FAIL: cards not found'; card.click(); return card.classList.contains('flipped')?'PASS':'FAIL: expected flipped status';"}),
            }
        ]
    },
    # ── 20. Dynamic HSL Color Picker ──────────────────────────────────────────
    {
        "title": "HSL Dynamic Picker",
        "slug": "hsl-dynamic-picker",
        "short_description": "Build an HSL color controller that updates preview backgrounds and values.",
        "description": (
            "### HSL Dynamic Picker\n\n"
            "Build an HSL color selector widget with the following requirements:\n"
            "- Implement range sliders for Hue `#hue` (0-360), Saturation `#saturation` (0-100), and Lightness `#lightness` (0-100).\n"
            "- When sliding values, calculate color string `hsl(h, s%, l%)` and update background-color of `#color-box`.\n"
            "- Display output values text string inside `#color-string` container."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["Color Picker", "HSL", "Inputs Range"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Listen to input event on range inputs.", "Template color strings directly: `hsl(${h}, ${s}%, ${l}%)`."],
        "concepts": ["Color Models CSS", "Sliders Range Events", "Style Injection"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>HSL Picker</title>\n  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"picker-card\">\n"
                    "    <div id=\"color-box\"></div>\n"
                    "    <div id=\"color-string\">hsl(180, 50%, 50%)</div>\n"
                    "    <div class=\"sliders\">\n"
                    "      <label>Hue <input id=\"hue\" type=\"range\" min=\"0\" max=\"360\" value=\"180\"></label>\n"
                    "      <label>Saturation <input id=\"saturation\" type=\"range\" min=\"0\" max=\"100\" value=\"50\"></label>\n"
                    "      <label>Lightness <input id=\"lightness\" type=\"range\" min=\"0\" max=\"100\" value=\"50\"></label>\n"
                    "    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0c0c0e; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".picker-card { background: #1c1c1f; border: 1px solid #2e2e33; padding: 24px; border-radius: 8px; width: 100%; max-width: 320px; text-align: center; }\n"
                    "#color-box { width: 100%; height: 120px; border-radius: 6px; background: hsl(180, 50%, 50%); margin-bottom: 12px; border: 1px solid #2e2e33; }\n"
                    "#color-string { font-family: monospace; font-size: 14px; color: #a1a1aa; margin-bottom: 20px; }\n"
                    ".sliders { display: flex; flex-direction: column; gap: 12px; text-align: left; font-size: 13px; color: #a1a1aa; }\n"
                    ".sliders label { display: flex; justify-content: space-between; align-items: center; }\n"
                    ".sliders input { width: 140px; }\n"
                ),
                "index.js": (
                    "// TODO: Listen to range sliders input and update background color of #color-box and label of #color-string\n"
                )
            })
        },
        "test_cases": [
            {
                "id": "hsl-tc-1", "name": "Slider input changes box color and text label", "hidden": False, "weight": 2, "comparison_mode": "exact", "expected_output": "PASS\n",
                "stdin": json.dumps({"evaluation": "const h=document.getElementById('hue'); const box=document.getElementById('color-box'); const label=document.getElementById('color-string'); if(!h||!box||!label)return 'FAIL: missing elements'; h.value='240'; h.dispatchEvent(new Event('input')); return (label.textContent.includes('240') && (box.style.backgroundColor.includes('rgb(25, 25, 230)') || box.style.backgroundColor.includes('hsl(240') || box.style.backgroundColor !== ''))?'PASS':'FAIL: color preview failed to update';"}),
            }
        ]
    }
]

def seed_frontend():
    print(f"Connecting to MongoDB and drop/inserting 20 premium Frontend challenges...")
    total_added = 0
    for doc in NEW_CHALLENGES:
        slug = doc["slug"]
        col.delete_one({"slug": slug})
        
        # Structure payload to match DB standard schemas
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
        print(f"  ✓ Seeded {slug}")
        total_added += 1
    
    print(f"\nCompleted! Seeded {total_added} Frontend challenges to database successfully.")

if __name__ == "__main__":
    seed_frontend()
