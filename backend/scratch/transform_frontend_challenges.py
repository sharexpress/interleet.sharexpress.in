"""
Transform Frontend Challenges — Migration Script
==================================================
Replaces all 10 Frontend domain challenges with beginner-friendly,
properly executable problems. Each challenge:
  - Has clear markdown descriptions with examples
  - Includes JavaScript AND TypeScript starter code
  - Has 3-5 test cases (visible + hidden)
  - Reads JSON from stdin, writes result to stdout
  - Removes Python/Go from starter_code
"""

import asyncio
from datetime import datetime
from app.core.db import get_db


# ═══════════════════════════════════════════════════════════════════════════════
#  CHALLENGE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

CHALLENGES = [

    # ──────────────────────────────────────────────────────────────────────────
    # 1. MARKDOWN TO HTML PARSER
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "markdown-to-html-parser",
        "updates": {
            "title": "Markdown to HTML Parser",
            "short_description": "Convert basic Markdown syntax (headings, bold, italic) into valid HTML strings.",
            "description": """### 🎯 What You'll Build
Build a function that converts basic **Markdown** syntax into valid **HTML**.

### 📋 Supported Syntax
| Markdown | HTML Output |
|----------|-------------|
| `# text` | `<h1>text</h1>` |
| `## text` | `<h2>text</h2>` |
| `### text` | `<h3>text</h3>` |
| `**text**` | `<strong>text</strong>` |
| `*text*` | `<em>text</em>` |
| plain text | `<p>plain text</p>` |

### 💡 Example
**Input:** `"# Hello **World**"`
**Output:** `"<h1>Hello <strong>World</strong></h1>"`

### 🚀 Step-by-Step Approach
1. Split the markdown into lines (by `\\n`)
2. For each line, replace `**text**` with `<strong>text</strong>`
3. Then replace `*text*` with `<em>text</em>` (do this AFTER bold replacement)
4. Check if the line starts with `#`, `##`, or `###` — wrap in the matching heading tag
5. If the line isn't a heading, wrap it in `<p>` tags
6. Join all processed lines back together with `\\n`
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["String Parsing", "Regex", "HTML"],
            "estimated_time_minutes": 25,
            "xp_reward": 200,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  MARKDOWN TO HTML PARSER
//  Convert basic Markdown syntax into valid HTML.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Convert a markdown string to HTML.
 *
 * Rules:
 *   # heading     →  <h1>heading</h1>
 *   ## heading    →  <h2>heading</h2>
 *   ### heading   →  <h3>heading</h3>
 *   **bold**      →  <strong>bold</strong>
 *   *italic*      →  <em>italic</em>
 *   plain text    →  <p>plain text</p>
 *
 * @param {string} markdown - The raw markdown text
 * @returns {string} The converted HTML
 */
function parseMarkdown(markdown) {
  // TODO: Split markdown into lines
  // TODO: For each line, replace **text** with <strong>text</strong>
  // TODO: Then replace *text* with <em>text</em>
  // TODO: Check if line starts with ### , ## , or # and wrap accordingly
  // TODO: Wrap all other lines in <p> tags
  // TODO: Join lines with '\\n' and return

  return '';
}

// ── Output (do not modify) ─────────────────────────────────
console.log(parseMarkdown(input.markdown));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  MARKDOWN TO HTML PARSER
//  Convert basic Markdown syntax into valid HTML.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface Input { markdown: string; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Convert a markdown string to HTML.
 *
 * Rules:
 *   # heading     →  <h1>heading</h1>
 *   ## heading    →  <h2>heading</h2>
 *   ### heading   →  <h3>heading</h3>
 *   **bold**      →  <strong>bold</strong>
 *   *italic*      →  <em>italic</em>
 *   plain text    →  <p>plain text</p>
 */
function parseMarkdown(markdown: string): string {
  // TODO: Split markdown into lines
  // TODO: For each line, replace **text** with <strong>text</strong>
  // TODO: Then replace *text* with <em>text</em>
  // TODO: Check if line starts with ### , ## , or # and wrap accordingly
  // TODO: Wrap all other lines in <p> tags
  // TODO: Join lines with '\\n' and return

  return '';
}

// ── Output (do not modify) ─────────────────────────────────
console.log(parseMarkdown(input.markdown));
""",
            },
            "test_cases": [
                {
                    "id": "md-html-tc1",
                    "name": "H1 heading",
                    "stdin": '{"markdown":"# Hello World"}\n',
                    "expected_output": "<h1>Hello World</h1>\n",
                    "hidden": False,
                    "weight": 1,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "md-html-tc2",
                    "name": "Bold and italic inline",
                    "stdin": '{"markdown":"This is **bold** and *italic* text"}\n',
                    "expected_output": "<p>This is <strong>bold</strong> and <em>italic</em> text</p>\n",
                    "hidden": False,
                    "weight": 1,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "md-html-tc3",
                    "name": "H2 heading",
                    "stdin": '{"markdown":"## Getting Started"}\n',
                    "expected_output": "<h2>Getting Started</h2>\n",
                    "hidden": False,
                    "weight": 1,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "md-html-tc4",
                    "name": "H3 heading",
                    "stdin": '{"markdown":"### Details"}\n',
                    "expected_output": "<h3>Details</h3>\n",
                    "hidden": True,
                    "weight": 2,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "md-html-tc5",
                    "name": "Plain text paragraph",
                    "stdin": '{"markdown":"No formatting here"}\n',
                    "expected_output": "<p>No formatting here</p>\n",
                    "hidden": True,
                    "weight": 2,
                    "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 2. TOAST QUEUE MANAGER
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "toast-queue-manager",
        "updates": {
            "title": "Toast Notification Queue",
            "short_description": "Build a notification toast queue with max-capacity eviction logic.",
            "description": """### 🎯 What You'll Build
Build a **Toast Notification Queue Manager** — a system that manages popup notifications with a maximum display limit.

### 📋 Requirements
- Maintain an **ordered queue** of active toasts (FIFO order)
- Support `add` and `dismiss` commands
- When `add` exceeds `maxToasts`, **evict the oldest** toast first
- `dismiss` removes a toast by ID (ignore if ID doesn't exist)

### 💡 Example
**Input:**
```json
{"maxToasts": 2, "commands": [
  {"action": "add", "id": "t1"},
  {"action": "add", "id": "t2"},
  {"action": "add", "id": "t3"}
]}
```
**Output:** `["t2","t3"]` ← t1 was evicted when t3 was added

### 🚀 Approach
1. Use an array to track active toasts in insertion order
2. On `add`: if at capacity, remove the first (oldest) element, then push the new one
3. On `dismiss`: filter out the matching ID
4. Return the final array of active IDs
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["Queue", "State Management", "Data Structures"],
            "estimated_time_minutes": 20,
            "xp_reward": 180,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  TOAST NOTIFICATION QUEUE
//  Manage a capped queue of notification toasts.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

class ToastManager {
  constructor(maxToasts) {
    // TODO: Store maxToasts and initialize an empty queue array
  }

  /**
   * Add a toast with the given ID.
   * If the queue is full (length >= maxToasts), remove the oldest toast first.
   */
  add(id) {
    // TODO: Check if queue is at capacity → remove first element
    // TODO: Push new id to the queue
  }

  /**
   * Dismiss (remove) a toast by ID.
   * If the ID doesn't exist, do nothing.
   */
  dismiss(id) {
    // TODO: Filter out the toast with the matching ID
  }

  /**
   * Return the array of active toast IDs in order.
   */
  getActive() {
    // TODO: Return the queue array
    return [];
  }
}

// ── Process and output (do not modify) ─────────────────────
const manager = new ToastManager(input.maxToasts);
for (const cmd of input.commands) {
  if (cmd.action === 'add') manager.add(cmd.id);
  else if (cmd.action === 'dismiss') manager.dismiss(cmd.id);
}
console.log(JSON.stringify(manager.getActive()));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  TOAST NOTIFICATION QUEUE
//  Manage a capped queue of notification toasts.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface Command { action: 'add' | 'dismiss'; id: string; }
interface Input { maxToasts: number; commands: Command[]; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

class ToastManager {
  private queue: string[] = [];
  private maxToasts: number;

  constructor(maxToasts: number) {
    // TODO: Store maxToasts
    this.maxToasts = maxToasts;
  }

  add(id: string): void {
    // TODO: Check if queue is at capacity → remove first element
    // TODO: Push new id to the queue
  }

  dismiss(id: string): void {
    // TODO: Filter out the toast with the matching ID
  }

  getActive(): string[] {
    // TODO: Return the queue array
    return [];
  }
}

// ── Process and output (do not modify) ─────────────────────
const manager = new ToastManager(input.maxToasts);
for (const cmd of input.commands) {
  if (cmd.action === 'add') manager.add(cmd.id);
  else if (cmd.action === 'dismiss') manager.dismiss(cmd.id);
}
console.log(JSON.stringify(manager.getActive()));
""",
            },
            "test_cases": [
                {
                    "id": "toast-tc1",
                    "name": "Add two toasts under limit",
                    "stdin": '{"maxToasts":3,"commands":[{"action":"add","id":"t1"},{"action":"add","id":"t2"}]}\n',
                    "expected_output": '["t1","t2"]\n',
                    "hidden": False,
                    "weight": 1,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "toast-tc2",
                    "name": "Evict oldest on overflow",
                    "stdin": '{"maxToasts":2,"commands":[{"action":"add","id":"t1"},{"action":"add","id":"t2"},{"action":"add","id":"t3"}]}\n',
                    "expected_output": '["t2","t3"]\n',
                    "hidden": False,
                    "weight": 1,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "toast-tc3",
                    "name": "Dismiss a toast by ID",
                    "stdin": '{"maxToasts":5,"commands":[{"action":"add","id":"t1"},{"action":"add","id":"t2"},{"action":"dismiss","id":"t1"}]}\n',
                    "expected_output": '["t2"]\n',
                    "hidden": False,
                    "weight": 1,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "toast-tc4",
                    "name": "Max capacity of 1",
                    "stdin": '{"maxToasts":1,"commands":[{"action":"add","id":"a"},{"action":"add","id":"b"},{"action":"add","id":"c"}]}\n',
                    "expected_output": '["c"]\n',
                    "hidden": True,
                    "weight": 2,
                    "comparison_mode": "trimmed",
                },
                {
                    "id": "toast-tc5",
                    "name": "Dismiss nonexistent ID",
                    "stdin": '{"maxToasts":3,"commands":[{"action":"add","id":"t1"},{"action":"dismiss","id":"t99"}]}\n',
                    "expected_output": '["t1"]\n',
                    "hidden": True,
                    "weight": 2,
                    "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 3. STAR RATING STATE ENGINE
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "star-rating-feedback-engine",
        "updates": {
            "title": "Star Rating State Engine",
            "short_description": "Track hover and click state for an interactive star rating widget.",
            "description": """### 🎯 What You'll Build
Build the **state logic** for a star rating widget — tracking which star is selected (clicked) and which star is being hovered over.

### 📋 Requirements
- Track two values: `selected` (the locked-in rating) and `hovered` (the currently hovered star)
- `click` on a star **sets** the selected rating. Clicking the same star again **toggles it off** (sets to 0)
- `hover` sets the hovered value. `hover 0` means the mouse left (reset hovered to 0)

### 💡 Example
**Input:**
```json
{"totalStars": 5, "events": [{"type": "click", "star": 3}]}
```
**Output:** `{"selected":3,"hovered":0}`

### 🚀 Approach
1. Initialize `selected = 0` and `hovered = 0`
2. For each event, update the appropriate value
3. For `click`: if the star equals current selected, reset to 0; otherwise set it
4. Return the final state as `{selected, hovered}`
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["State Machine", "Events", "UI Logic"],
            "estimated_time_minutes": 20,
            "xp_reward": 150,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  STAR RATING STATE ENGINE
//  Track hover and click state for a rating widget.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Process rating events and return the final state.
 *
 * Events: { type: "click" | "hover", star: number }
 *   - click: sets selected. Clicking same star again toggles it off (sets to 0)
 *   - hover: sets hovered value. hover 0 = mouse leave
 *
 * @param {object[]} events - Array of rating events
 * @returns {{ selected: number, hovered: number }}
 */
function processRatingEvents(events) {
  let selected = 0;
  let hovered = 0;

  for (const event of events) {
    // TODO: If event.type is 'click':
    //   - If event.star equals current selected → set selected to 0
    //   - Otherwise → set selected to event.star
    // TODO: If event.type is 'hover':
    //   - Set hovered to event.star
  }

  return { selected, hovered };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(processRatingEvents(input.events)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  STAR RATING STATE ENGINE
//  Track hover and click state for a rating widget.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface RatingEvent { type: 'click' | 'hover'; star: number; }
interface Input { totalStars: number; events: RatingEvent[]; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

interface RatingState { selected: number; hovered: number; }

function processRatingEvents(events: RatingEvent[]): RatingState {
  let selected = 0;
  let hovered = 0;

  for (const event of events) {
    // TODO: If event.type is 'click':
    //   - If event.star equals current selected → set selected to 0
    //   - Otherwise → set selected to event.star
    // TODO: If event.type is 'hover':
    //   - Set hovered to event.star
  }

  return { selected, hovered };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(processRatingEvents(input.events)));
""",
            },
            "test_cases": [
                {
                    "id": "star-tc1",
                    "name": "Click a star",
                    "stdin": '{"totalStars":5,"events":[{"type":"click","star":3}]}\n',
                    "expected_output": '{"selected":3,"hovered":0}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "star-tc2",
                    "name": "Hover over a star",
                    "stdin": '{"totalStars":5,"events":[{"type":"hover","star":4}]}\n',
                    "expected_output": '{"selected":0,"hovered":4}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "star-tc3",
                    "name": "Click then hover",
                    "stdin": '{"totalStars":5,"events":[{"type":"click","star":2},{"type":"hover","star":5}]}\n',
                    "expected_output": '{"selected":2,"hovered":5}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "star-tc4",
                    "name": "Toggle off by clicking same star",
                    "stdin": '{"totalStars":5,"events":[{"type":"click","star":4},{"type":"click","star":4}]}\n',
                    "expected_output": '{"selected":0,"hovered":0}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "star-tc5",
                    "name": "Hover then mouse leave",
                    "stdin": '{"totalStars":5,"events":[{"type":"hover","star":3},{"type":"hover","star":0}]}\n',
                    "expected_output": '{"selected":0,"hovered":0}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 4. DEBOUNCE SIMULATOR
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "debounced-suggestions-hook",
        "updates": {
            "title": "Debounce Event Simulator",
            "short_description": "Simulate debounce behavior: given timestamped events and a delay, find which events fire.",
            "description": """### 🎯 What You'll Build
Implement a **debounce simulator**. Given a series of timestamped events and a delay, determine which events would actually trigger.

### 📋 How Debounce Works
Debounce **delays** executing a callback until a "quiet period" has passed. Each new event **resets** the timer. An event only fires if no new event arrives within `delayMs` after it.

### 💡 Example
```
delayMs = 300
Events: a@0ms, b@100ms, c@500ms
```
- `a` at 0ms → `b` arrives at 100ms (within 300ms) → **a is cancelled**
- `b` at 100ms → `c` arrives at 500ms (400ms gap > 300ms) → **b fires** ✅
- `c` at 500ms → no more events → **c fires** ✅
- **Result: `["b", "c"]`**

### 🚀 Approach
1. Sort events by time (they should already be sorted)
2. For each event, check if the NEXT event arrives within `delayMs`
3. If yes → this event is cancelled (debounced away)
4. If no → this event fires
5. The last event always fires (no next event to cancel it)
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["Closures", "Timing", "Performance"],
            "estimated_time_minutes": 25,
            "xp_reward": 200,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  DEBOUNCE EVENT SIMULATOR
//  Find which events fire after debounce filtering.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Simulate debounce on a list of timestamped events.
 *
 * An event fires only if no subsequent event arrives within delayMs.
 * The last event always fires.
 *
 * @param {number} delayMs - The debounce delay in milliseconds
 * @param {{ time: number, value: string }[]} events - Sorted by time
 * @returns {string[]} - Values of events that would fire
 */
function simulateDebounce(delayMs, events) {
  const fired = [];

  // TODO: Loop through each event
  // TODO: Check if the NEXT event's time is within delayMs
  //   - If (nextEvent.time - currentEvent.time) < delayMs → skip (cancelled)
  //   - Otherwise → push currentEvent.value to fired
  // TODO: The last event always fires (no next event to cancel it)

  return fired;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(simulateDebounce(input.delayMs, input.events)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  DEBOUNCE EVENT SIMULATOR
//  Find which events fire after debounce filtering.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface TimedEvent { time: number; value: string; }
interface Input { delayMs: number; events: TimedEvent[]; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

function simulateDebounce(delayMs: number, events: TimedEvent[]): string[] {
  const fired: string[] = [];

  // TODO: Loop through each event
  // TODO: Check if NEXT event's time is within delayMs
  //   - If (nextEvent.time - currentEvent.time) < delayMs → skip
  //   - Otherwise → push currentEvent.value to fired
  // TODO: The last event always fires

  return fired;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(simulateDebounce(input.delayMs, input.events)));
""",
            },
            "test_cases": [
                {
                    "id": "debounce-tc1",
                    "name": "Mixed: some cancelled, some fire",
                    "stdin": '{"delayMs":300,"events":[{"time":0,"value":"a"},{"time":100,"value":"b"},{"time":500,"value":"c"}]}\n',
                    "expected_output": '["b","c"]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "debounce-tc2",
                    "name": "All events fire (gaps > delay)",
                    "stdin": '{"delayMs":500,"events":[{"time":0,"value":"x"},{"time":1000,"value":"y"}]}\n',
                    "expected_output": '["x","y"]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "debounce-tc3",
                    "name": "Only last event fires (rapid burst)",
                    "stdin": '{"delayMs":200,"events":[{"time":0,"value":"a"},{"time":50,"value":"b"},{"time":100,"value":"c"},{"time":150,"value":"d"}]}\n',
                    "expected_output": '["d"]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "debounce-tc4",
                    "name": "Single event always fires",
                    "stdin": '{"delayMs":100,"events":[{"time":0,"value":"only"}]}\n',
                    "expected_output": '["only"]\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "debounce-tc5",
                    "name": "Chain of near-miss cancellations",
                    "stdin": '{"delayMs":1000,"events":[{"time":0,"value":"a"},{"time":999,"value":"b"},{"time":1998,"value":"c"}]}\n',
                    "expected_output": '["c"]\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 5. FORM VALIDATION ENGINE
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "custom-form-validator-engine",
        "updates": {
            "title": "Form Validation Engine",
            "short_description": "Build a schema-based form validator that checks types, required fields, and constraints.",
            "description": """### 🎯 What You'll Build
Build a **form validation engine** that validates data against a set of rules — similar to how libraries like Zod or Yup work.

### 📋 Supported Rules
| Rule | Description |
|------|-------------|
| `required: true` | Field must exist and not be null/undefined |
| `type: "string"` | Value must be a string |
| `type: "number"` | Value must be a number |
| `minLength: n` | String must be at least n characters |
| `min: n` | Number must be ≥ n |
| `max: n` | Number must be ≤ n |

### 💡 Error Message Format
- `"fieldName is required"`
- `"fieldName must be a string"`
- `"fieldName must be a number"`
- `"fieldName must be at least N characters"` (for string minLength)
- `"fieldName must be at least N"` (for number min)
- `"fieldName must be at most N"` (for number max)

### 💡 Example
**Input:**
```json
{"rules": {"name": {"type": "string", "required": true, "minLength": 3}}, "data": {"name": "Jo"}}
```
**Output:** `{"valid":false,"errors":["name must be at least 3 characters"]}`

### 🚀 Approach
1. Loop through each field in `rules`
2. Check `required` first (is the value missing?)
3. Check `type` (does the value match the expected type?)
4. Check constraints (`minLength`, `min`, `max`)
5. Collect all error strings, return `{valid, errors}`
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["Validation", "Schema", "Error Handling"],
            "estimated_time_minutes": 30,
            "xp_reward": 220,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  FORM VALIDATION ENGINE
//  Validate data against schema rules.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Validate data against a rules schema.
 *
 * @param {Object} rules - { fieldName: { type, required, minLength, min, max } }
 * @param {Object} data  - The data to validate
 * @returns {{ valid: boolean, errors: string[] }}
 */
function validate(rules, data) {
  const errors = [];

  for (const [field, rule] of Object.entries(rules)) {
    const value = data[field];

    // TODO: Check if required and value is undefined or null
    //   → push "fieldName is required" and continue to next field

    // TODO: If value exists, check type:
    //   rule.type === 'string' → typeof value !== 'string' → push error
    //   rule.type === 'number' → typeof value !== 'number' → push error

    // TODO: String constraints:
    //   rule.minLength → value.length < rule.minLength → push error

    // TODO: Number constraints:
    //   rule.min → value < rule.min → push error
    //   rule.max → value > rule.max → push error
  }

  return { valid: errors.length === 0, errors };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(validate(input.rules, input.data)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  FORM VALIDATION ENGINE
//  Validate data against schema rules.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface Rule { type?: 'string' | 'number'; required?: boolean; minLength?: number; min?: number; max?: number; }
interface Input { rules: Record<string, Rule>; data: Record<string, any>; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

interface ValidationResult { valid: boolean; errors: string[]; }

function validate(rules: Record<string, Rule>, data: Record<string, any>): ValidationResult {
  const errors: string[] = [];

  for (const [field, rule] of Object.entries(rules)) {
    const value = data[field];

    // TODO: Check required → push "{field} is required"
    // TODO: Check type mismatch → push "{field} must be a {type}"
    // TODO: Check minLength → push "{field} must be at least {n} characters"
    // TODO: Check min → push "{field} must be at least {n}"
    // TODO: Check max → push "{field} must be at most {n}"
  }

  return { valid: errors.length === 0, errors };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(validate(input.rules, input.data)));
""",
            },
            "test_cases": [
                {
                    "id": "form-tc1",
                    "name": "All fields valid",
                    "stdin": '{"rules":{"name":{"type":"string","required":true,"minLength":2}},"data":{"name":"John"}}\n',
                    "expected_output": '{"valid":true,"errors":[]}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "form-tc2",
                    "name": "String too short",
                    "stdin": '{"rules":{"name":{"type":"string","required":true,"minLength":3}},"data":{"name":"Jo"}}\n',
                    "expected_output": '{"valid":false,"errors":["name must be at least 3 characters"]}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "form-tc3",
                    "name": "Missing required field",
                    "stdin": '{"rules":{"name":{"type":"string","required":true},"email":{"type":"string","required":true}},"data":{"name":"John"}}\n',
                    "expected_output": '{"valid":false,"errors":["email is required"]}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "form-tc4",
                    "name": "Number out of range (max)",
                    "stdin": '{"rules":{"age":{"type":"number","required":true,"min":0,"max":120}},"data":{"age":150}}\n',
                    "expected_output": '{"valid":false,"errors":["age must be at most 120"]}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "form-tc5",
                    "name": "Type mismatch (number expected)",
                    "stdin": '{"rules":{"count":{"type":"number","required":true}},"data":{"count":"hello"}}\n',
                    "expected_output": '{"valid":false,"errors":["count must be a number"]}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 6. RESPONSIVE BREAKPOINT RESOLVER
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "responsive-breakpoint-helper",
        "updates": {
            "title": "Responsive Breakpoint Resolver",
            "short_description": "Map viewport widths to Tailwind-style breakpoints with column and gutter values.",
            "description": """### 🎯 What You'll Build
Build a function that maps a viewport width to a **responsive breakpoint** — similar to how CSS frameworks like Tailwind determine layout behavior.

### 📋 Breakpoint Table
| Breakpoint | Min Width | Columns | Gutter (px) |
|-----------|-----------|---------|-------------|
| `xs` | 0 | 4 | 16 |
| `sm` | 640 | 6 | 20 |
| `md` | 768 | 8 | 24 |
| `lg` | 1024 | 12 | 24 |
| `xl` | 1280 | 12 | 32 |
| `2xl` | 1536 | 12 | 32 |

### 💡 Example
**Input:** `{"width": 800}`
**Output:** `{"breakpoint":"md","columns":8,"gutter":24}`
(800 ≥ 768 but < 1024 → `md`)

### 🚀 Approach
1. Define the breakpoints as an array sorted by min width (descending)
2. Find the first breakpoint where `width >= minWidth`
3. Return the matching breakpoint name, columns, and gutter
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["Responsive Design", "Conditionals", "Configuration"],
            "estimated_time_minutes": 15,
            "xp_reward": 150,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  RESPONSIVE BREAKPOINT RESOLVER
//  Map viewport widths to grid breakpoints.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

// Breakpoint definitions (from largest to smallest)
const BREAKPOINTS = [
  { name: '2xl', minWidth: 1536, columns: 12, gutter: 32 },
  { name: 'xl',  minWidth: 1280, columns: 12, gutter: 32 },
  { name: 'lg',  minWidth: 1024, columns: 12, gutter: 24 },
  { name: 'md',  minWidth: 768,  columns: 8,  gutter: 24 },
  { name: 'sm',  minWidth: 640,  columns: 6,  gutter: 20 },
  { name: 'xs',  minWidth: 0,    columns: 4,  gutter: 16 },
];

/**
 * Resolve the breakpoint for a given viewport width.
 *
 * @param {number} width - The viewport width in pixels
 * @returns {{ breakpoint: string, columns: number, gutter: number }}
 */
function resolveBreakpoint(width) {
  // TODO: Loop through BREAKPOINTS (they are sorted largest-first)
  // TODO: Find the first breakpoint where width >= minWidth
  // TODO: Return { breakpoint: name, columns, gutter }

  return { breakpoint: 'xs', columns: 4, gutter: 16 };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(resolveBreakpoint(input.width)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  RESPONSIVE BREAKPOINT RESOLVER
//  Map viewport widths to grid breakpoints.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface Input { width: number; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

interface Breakpoint { name: string; minWidth: number; columns: number; gutter: number; }
interface Result { breakpoint: string; columns: number; gutter: number; }

const BREAKPOINTS: Breakpoint[] = [
  { name: '2xl', minWidth: 1536, columns: 12, gutter: 32 },
  { name: 'xl',  minWidth: 1280, columns: 12, gutter: 32 },
  { name: 'lg',  minWidth: 1024, columns: 12, gutter: 24 },
  { name: 'md',  minWidth: 768,  columns: 8,  gutter: 24 },
  { name: 'sm',  minWidth: 640,  columns: 6,  gutter: 20 },
  { name: 'xs',  minWidth: 0,    columns: 4,  gutter: 16 },
];

function resolveBreakpoint(width: number): Result {
  // TODO: Find the first breakpoint where width >= minWidth
  return { breakpoint: 'xs', columns: 4, gutter: 16 };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(resolveBreakpoint(input.width)));
""",
            },
            "test_cases": [
                {
                    "id": "bp-tc1",
                    "name": "Medium breakpoint (800px)",
                    "stdin": '{"width":800}\n',
                    "expected_output": '{"breakpoint":"md","columns":8,"gutter":24}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "bp-tc2",
                    "name": "Extra small (375px mobile)",
                    "stdin": '{"width":375}\n',
                    "expected_output": '{"breakpoint":"xs","columns":4,"gutter":16}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "bp-tc3",
                    "name": "Extra large (1280px)",
                    "stdin": '{"width":1280}\n',
                    "expected_output": '{"breakpoint":"xl","columns":12,"gutter":32}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "bp-tc4",
                    "name": "Exact boundary (640px = sm)",
                    "stdin": '{"width":640}\n',
                    "expected_output": '{"breakpoint":"sm","columns":6,"gutter":20}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "bp-tc5",
                    "name": "2xl ultrawide (1920px)",
                    "stdin": '{"width":1920}\n',
                    "expected_output": '{"breakpoint":"2xl","columns":12,"gutter":32}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 7. FILE PATH TO TREE CONVERTER
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "nested-file-directory-tree",
        "updates": {
            "title": "File Path to Tree Converter",
            "short_description": "Convert an array of flat file paths into a nested folder/file tree structure.",
            "description": """### 🎯 What You'll Build
Build a function that converts a **flat list of file paths** into a **nested tree structure** — like a file explorer sidebar.

### 📋 Requirements
- The root node has `name: "root"` and contains top-level children
- Each folder node has `name` and `children` (array)
- Each file node (leaf) has only `name` (no children key)
- Paths use `/` as separator
- If two paths share a folder, they share the same tree node

### 💡 Example
**Input:** `{"paths": ["src/index.js", "src/utils.js"]}`
**Output:**
```json
{"name":"root","children":[{"name":"src","children":[{"name":"index.js"},{"name":"utils.js"}]}]}
```

### 🚀 Approach
1. Create a root node: `{ name: "root", children: [] }`
2. For each path, split by `/` to get segments
3. Walk through segments, creating folder nodes as needed
4. The last segment is a file (leaf node, no children)
5. Return the root node
""",
            "domain": "Frontend",
            "difficulty": "Medium",
            "tags": ["Recursion", "Tree", "Data Transformation"],
            "estimated_time_minutes": 35,
            "xp_reward": 300,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  FILE PATH TO TREE CONVERTER
//  Convert flat file paths into a nested tree.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Convert an array of file paths into a nested tree structure.
 *
 * @param {string[]} paths - Array of file paths like ["src/index.js", "src/utils.js"]
 * @returns {Object} A tree with { name: "root", children: [...] }
 */
function buildFileTree(paths) {
  const root = { name: 'root', children: [] };

  for (const path of paths) {
    const segments = path.split('/');
    // TODO: Start at the root node
    // TODO: For each segment (except the last), find or create a folder node
    //   - Look for an existing child with matching name and children array
    //   - If not found, create { name: segment, children: [] } and push it
    // TODO: For the last segment, create a leaf node { name: segment } (no children)
  }

  return root;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(buildFileTree(input.paths)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  FILE PATH TO TREE CONVERTER
//  Convert flat file paths into a nested tree.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface Input { paths: string[]; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

interface TreeNode { name: string; children?: TreeNode[]; }

function buildFileTree(paths: string[]): TreeNode {
  const root: TreeNode = { name: 'root', children: [] };

  for (const path of paths) {
    const segments = path.split('/');
    // TODO: Walk the tree, creating folder and file nodes
  }

  return root;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(buildFileTree(input.paths)));
""",
            },
            "test_cases": [
                {
                    "id": "tree-tc1",
                    "name": "Two files in same folder",
                    "stdin": '{"paths":["src/index.js","src/utils.js"]}\n',
                    "expected_output": '{"name":"root","children":[{"name":"src","children":[{"name":"index.js"},{"name":"utils.js"}]}]}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "tree-tc2",
                    "name": "Single root-level file",
                    "stdin": '{"paths":["README.md"]}\n',
                    "expected_output": '{"name":"root","children":[{"name":"README.md"}]}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "tree-tc3",
                    "name": "Nested and sibling paths",
                    "stdin": '{"paths":["a/b/c.txt","a/d.txt"]}\n',
                    "expected_output": '{"name":"root","children":[{"name":"a","children":[{"name":"b","children":[{"name":"c.txt"}]},{"name":"d.txt"}]}]}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "tree-tc4",
                    "name": "Multiple root-level files",
                    "stdin": '{"paths":["x.js","y.js","z.js"]}\n',
                    "expected_output": '{"name":"root","children":[{"name":"x.js"},{"name":"y.js"},{"name":"z.js"}]}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "tree-tc5",
                    "name": "Deeply nested single file",
                    "stdin": '{"paths":["a/b/c/d/e.txt"]}\n',
                    "expected_output": '{"name":"root","children":[{"name":"a","children":[{"name":"b","children":[{"name":"c","children":[{"name":"d","children":[{"name":"e.txt"}]}]}]}]}]}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 8. VIRTUAL SCROLL INDEX CALCULATOR
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "virtual-scrolling-list-component",
        "updates": {
            "title": "Virtual Scroll Index Calculator",
            "short_description": "Calculate the visible item range for a virtual scrolling list given scroll position and viewport size.",
            "description": """### 🎯 What You'll Build
Build the **math engine** behind virtual scrolling — a performance technique where only visible list items are rendered (instead of thousands of DOM nodes).

### 📋 Parameters
| Parameter | Description |
|-----------|-------------|
| `totalItems` | Total number of items in the list |
| `itemHeight` | Height of each item in pixels |
| `scrollTop` | Current scroll position (pixels from top) |
| `viewportHeight` | Height of the visible viewport |
| `overscan` | Number of extra items to render above/below viewport |

### 📋 Output Fields
| Field | Formula |
|-------|---------|
| `startIndex` | `max(0, floor(scrollTop / itemHeight) - overscan)` |
| `endIndex` | `min(totalItems-1, ceil((scrollTop + viewportHeight) / itemHeight) - 1 + overscan)` |
| `visibleCount` | `endIndex - startIndex + 1` |
| `offsetY` | `startIndex * itemHeight` |

### 💡 Example
```
totalItems=100, itemHeight=50, scrollTop=0, viewportHeight=300, overscan=2
firstVisible = floor(0/50) = 0 → startIndex = max(0, 0-2) = 0
lastVisible = ceil(300/50)-1 = 5 → endIndex = min(99, 5+2) = 7
```
**Output:** `{"startIndex":0,"endIndex":7,"visibleCount":8,"offsetY":0}`
""",
            "domain": "Frontend",
            "difficulty": "Medium",
            "tags": ["Math", "Windowing", "Performance"],
            "estimated_time_minutes": 30,
            "xp_reward": 320,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  VIRTUAL SCROLL INDEX CALCULATOR
//  Calculate visible item range for virtual scrolling.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Calculate the visible range for virtual scrolling.
 *
 * Formulas:
 *   firstVisible = Math.floor(scrollTop / itemHeight)
 *   lastVisible  = Math.ceil((scrollTop + viewportHeight) / itemHeight) - 1
 *   startIndex   = Math.max(0, firstVisible - overscan)
 *   endIndex     = Math.min(totalItems - 1, lastVisible + overscan)
 *   visibleCount = endIndex - startIndex + 1
 *   offsetY      = startIndex * itemHeight
 */
function calculateVisibleRange(config) {
  const { totalItems, itemHeight, scrollTop, viewportHeight, overscan } = config;

  // TODO: Calculate firstVisible using Math.floor
  // TODO: Calculate lastVisible using Math.ceil
  // TODO: Apply overscan buffer to get startIndex and endIndex
  // TODO: Clamp values: startIndex >= 0, endIndex <= totalItems - 1
  // TODO: Calculate visibleCount and offsetY

  return { startIndex: 0, endIndex: 0, visibleCount: 0, offsetY: 0 };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(calculateVisibleRange(input)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  VIRTUAL SCROLL INDEX CALCULATOR
//  Calculate visible item range for virtual scrolling.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface ScrollConfig { totalItems: number; itemHeight: number; scrollTop: number; viewportHeight: number; overscan: number; }
const input: ScrollConfig = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

interface VisibleRange { startIndex: number; endIndex: number; visibleCount: number; offsetY: number; }

function calculateVisibleRange(config: ScrollConfig): VisibleRange {
  const { totalItems, itemHeight, scrollTop, viewportHeight, overscan } = config;

  // TODO: Implement the virtual scroll formulas
  return { startIndex: 0, endIndex: 0, visibleCount: 0, offsetY: 0 };
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(calculateVisibleRange(input)));
""",
            },
            "test_cases": [
                {
                    "id": "vscroll-tc1",
                    "name": "Scroll at top with overscan",
                    "stdin": '{"totalItems":100,"itemHeight":50,"scrollTop":0,"viewportHeight":300,"overscan":2}\n',
                    "expected_output": '{"startIndex":0,"endIndex":7,"visibleCount":8,"offsetY":0}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "vscroll-tc2",
                    "name": "Scrolled partway down",
                    "stdin": '{"totalItems":100,"itemHeight":40,"scrollTop":200,"viewportHeight":400,"overscan":1}\n',
                    "expected_output": '{"startIndex":4,"endIndex":15,"visibleCount":12,"offsetY":160}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "vscroll-tc3",
                    "name": "Near bottom of list",
                    "stdin": '{"totalItems":10,"itemHeight":100,"scrollTop":500,"viewportHeight":300,"overscan":0}\n',
                    "expected_output": '{"startIndex":5,"endIndex":7,"visibleCount":3,"offsetY":500}\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "vscroll-tc4",
                    "name": "Viewport larger than total list",
                    "stdin": '{"totalItems":5,"itemHeight":50,"scrollTop":0,"viewportHeight":1000,"overscan":0}\n',
                    "expected_output": '{"startIndex":0,"endIndex":4,"visibleCount":5,"offsetY":0}\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 9. MODAL STATE MACHINE
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "modal-transitions-animator",
        "updates": {
            "title": "Modal Transition State Machine",
            "short_description": "Implement a state machine that tracks modal lifecycle phases: CLOSED → OPENING → OPEN → CLOSING → CLOSED.",
            "description": """### 🎯 What You'll Build
Build a **state machine** that manages modal transition lifecycle — tracking whether a modal is closed, opening, open, or closing.

### 📋 State Transitions
| Current State | Event | Next State |
|--------------|-------|------------|
| `CLOSED` | `OPEN` | `OPENING` |
| `OPENING` | `ANIMATION_END` | `OPEN` |
| `OPEN` | `CLOSE` | `CLOSING` |
| `CLOSING` | `ANIMATION_END` | `CLOSED` |
| Any | Invalid event | **Stay in current state** |

### 💡 Example
**Input:** `{"events": ["OPEN", "ANIMATION_END", "CLOSE", "ANIMATION_END"]}`
**Output:** `["CLOSED","OPENING","OPEN","CLOSING","CLOSED"]`
(includes initial state + state after each event)

### 🚀 Approach
1. Start with state = `"CLOSED"`
2. Record the initial state in the output array
3. For each event, look up the valid transition
4. If valid → update state; if invalid → keep current state
5. Record the state after each event
""",
            "domain": "Frontend",
            "difficulty": "Easy",
            "tags": ["State Machine", "Lifecycle", "Transitions"],
            "estimated_time_minutes": 20,
            "xp_reward": 180,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  MODAL TRANSITION STATE MACHINE
//  Track modal lifecycle: CLOSED → OPENING → OPEN → CLOSING
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

// Valid state transitions: { currentState: { event: nextState } }
const TRANSITIONS = {
  CLOSED:  { OPEN: 'OPENING' },
  OPENING: { ANIMATION_END: 'OPEN' },
  OPEN:    { CLOSE: 'CLOSING' },
  CLOSING: { ANIMATION_END: 'CLOSED' },
};

/**
 * Process a list of events through the modal state machine.
 * Returns an array of states: [initialState, stateAfterEvent1, stateAfterEvent2, ...]
 *
 * @param {string[]} events - Array of event names
 * @returns {string[]} - Array of states (length = events.length + 1)
 */
function processTransitions(events) {
  let state = 'CLOSED';
  const states = [state]; // Start with initial state

  for (const event of events) {
    // TODO: Look up TRANSITIONS[state][event]
    // TODO: If a valid next state exists → update state
    // TODO: If not (invalid transition) → keep current state
    // TODO: Push the current state to the states array
  }

  return states;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(processTransitions(input.events)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  MODAL TRANSITION STATE MACHINE
//  Track modal lifecycle: CLOSED → OPENING → OPEN → CLOSING
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface Input { events: string[]; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

const TRANSITIONS: Record<string, Record<string, string>> = {
  CLOSED:  { OPEN: 'OPENING' },
  OPENING: { ANIMATION_END: 'OPEN' },
  OPEN:    { CLOSE: 'CLOSING' },
  CLOSING: { ANIMATION_END: 'CLOSED' },
};

function processTransitions(events: string[]): string[] {
  let state = 'CLOSED';
  const states: string[] = [state];

  for (const event of events) {
    // TODO: Look up transition and update state
    // TODO: Push state to states array
  }

  return states;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(processTransitions(input.events)));
""",
            },
            "test_cases": [
                {
                    "id": "modal-tc1",
                    "name": "Open a modal",
                    "stdin": '{"events":["OPEN"]}\n',
                    "expected_output": '["CLOSED","OPENING"]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "modal-tc2",
                    "name": "Full open cycle",
                    "stdin": '{"events":["OPEN","ANIMATION_END"]}\n',
                    "expected_output": '["CLOSED","OPENING","OPEN"]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "modal-tc3",
                    "name": "Complete open and close lifecycle",
                    "stdin": '{"events":["OPEN","ANIMATION_END","CLOSE","ANIMATION_END"]}\n',
                    "expected_output": '["CLOSED","OPENING","OPEN","CLOSING","CLOSED"]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "modal-tc4",
                    "name": "Invalid event ignored",
                    "stdin": '{"events":["CLOSE"]}\n',
                    "expected_output": '["CLOSED","CLOSED"]\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "modal-tc5",
                    "name": "Close during opening (invalid)",
                    "stdin": '{"events":["OPEN","CLOSE"]}\n',
                    "expected_output": '["CLOSED","OPENING","OPENING"]\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },

    # ──────────────────────────────────────────────────────────────────────────
    # 10. CSS GRID PLACEMENT SIMULATOR
    # ──────────────────────────────────────────────────────────────────────────
    {
        "slug": "css-grid-autoplacement-calc",
        "updates": {
            "title": "CSS Grid Placement Simulator",
            "short_description": "Simulate CSS Grid auto-placement: position items with column spans on a grid.",
            "description": """### 🎯 What You'll Build
Simulate the **CSS Grid auto-placement algorithm** — placing items left-to-right, top-to-bottom on a grid, respecting column spans.

### 📋 Rules
- Grid has a fixed number of columns
- Items are placed left-to-right, then wrap to the next row
- Each item has a `colSpan` (how many columns it occupies)
- An item fits at position `(row, col)` if all cells from `col` to `col + colSpan - 1` are empty
- Items must fit within the column count (no overflow past the last column)

### 💡 Example
```
columns = 3
items: a(1col), b(2col), c(1col)
```
Row 0: `[a][b][b]` — a at col 0, b spans cols 1-2
Row 1: `[c][ ][ ]` — c wraps to next row

**Output:** `[{"id":"a","row":0,"col":0},{"id":"b","row":0,"col":1},{"id":"c","row":1,"col":0}]`

### 🚀 Approach
1. Track occupied cells using a Set or 2D grid
2. For each item, scan positions left-to-right, top-to-bottom
3. Check if all cells for the span are empty
4. Place the item at the first valid position
""",
            "domain": "Frontend",
            "difficulty": "Medium",
            "tags": ["Grid Layout", "Algorithm", "Collision Detection"],
            "estimated_time_minutes": 45,
            "xp_reward": 350,
            "recommended_for_beginner": True,
            "starter_code": {
                "javascript": """\
// ═══════════════════════════════════════════════════════════════
//  CSS GRID PLACEMENT SIMULATOR
//  Place items on a grid respecting column spans.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
const input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

/**
 * Place items on a grid with the given number of columns.
 * Each item has an id and colSpan.
 * Returns array of placements: { id, row, col }
 *
 * @param {number} columns - Number of grid columns
 * @param {{ id: string, colSpan: number }[]} items
 * @returns {{ id: string, row: number, col: number }[]}
 */
function placeGridItems(columns, items) {
  const occupied = new Set(); // Store occupied cells as "row,col" strings
  const placements = [];

  for (const item of items) {
    let placed = false;

    // TODO: Scan rows starting from 0
    // TODO: For each row, scan columns from 0 to (columns - item.colSpan)
    // TODO: Check if ALL cells from col to col+colSpan-1 are empty
    //   (use occupied.has(`${row},${c}`) to check each cell)
    // TODO: If all empty → place the item:
    //   - Mark cells as occupied: occupied.add(`${row},${c}`)
    //   - Push { id: item.id, row, col } to placements
    //   - Break out of both loops
    // TODO: If col doesn't fit, move to next row
  }

  return placements;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(placeGridItems(input.columns, input.items)));
""",
                "typescript": """\
// ═══════════════════════════════════════════════════════════════
//  CSS GRID PLACEMENT SIMULATOR
//  Place items on a grid respecting column spans.
// ═══════════════════════════════════════════════════════════════

// ── Read input (do not modify) ─────────────────────────────
declare function require(id: string): any;
interface GridItem { id: string; colSpan: number; }
interface Input { columns: number; items: GridItem[]; }
const input: Input = JSON.parse(require('fs').readFileSync(0, 'utf8').trim());

interface Placement { id: string; row: number; col: number; }

function placeGridItems(columns: number, items: GridItem[]): Placement[] {
  const occupied = new Set<string>();
  const placements: Placement[] = [];

  for (const item of items) {
    // TODO: Find the first valid position and place the item
  }

  return placements;
}

// ── Output (do not modify) ─────────────────────────────────
console.log(JSON.stringify(placeGridItems(input.columns, input.items)));
""",
            },
            "test_cases": [
                {
                    "id": "grid-tc1",
                    "name": "Three 1-col items in a row",
                    "stdin": '{"columns":3,"items":[{"id":"a","colSpan":1},{"id":"b","colSpan":1},{"id":"c","colSpan":1}]}\n',
                    "expected_output": '[{"id":"a","row":0,"col":0},{"id":"b","row":0,"col":1},{"id":"c","row":0,"col":2}]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "grid-tc2",
                    "name": "Span-2 items cause wrapping",
                    "stdin": '{"columns":3,"items":[{"id":"a","colSpan":2},{"id":"b","colSpan":2}]}\n',
                    "expected_output": '[{"id":"a","row":0,"col":0},{"id":"b","row":1,"col":0}]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "grid-tc3",
                    "name": "Mixed sizes with gap filling",
                    "stdin": '{"columns":4,"items":[{"id":"a","colSpan":1},{"id":"b","colSpan":3},{"id":"c","colSpan":2}]}\n',
                    "expected_output": '[{"id":"a","row":0,"col":0},{"id":"b","row":0,"col":1},{"id":"c","row":1,"col":0}]\n',
                    "hidden": False, "weight": 1, "comparison_mode": "trimmed",
                },
                {
                    "id": "grid-tc4",
                    "name": "Full-width item",
                    "stdin": '{"columns":3,"items":[{"id":"full","colSpan":3}]}\n',
                    "expected_output": '[{"id":"full","row":0,"col":0}]\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
                {
                    "id": "grid-tc5",
                    "name": "Items wrapping to second row",
                    "stdin": '{"columns":2,"items":[{"id":"a","colSpan":1},{"id":"b","colSpan":1},{"id":"c","colSpan":1}]}\n',
                    "expected_output": '[{"id":"a","row":0,"col":0},{"id":"b","row":0,"col":1},{"id":"c","row":1,"col":0}]\n',
                    "hidden": True, "weight": 2, "comparison_mode": "trimmed",
                },
            ],
        },
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  MIGRATION LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    db = get_db()
    now = datetime.utcnow()

    print("=" * 60)
    print("  FRONTEND CHALLENGES TRANSFORMATION")
    print("=" * 60)

    for ch in CHALLENGES:
        slug = ch["slug"]
        updates = ch["updates"]
        updates["updated_at"] = now

        # Update the problems document
        result = await db.problems.update_one(
            {"slug": slug},
            {"$set": updates}
        )
        status = "✅ updated" if result.modified_count else "⚠️  no changes (already up to date?)"
        print(f"\n{status}: {slug}")
        print(f"   Title: {updates['title']}")
        print(f"   Difficulty: {updates['difficulty']}")
        print(f"   Languages: {list(updates['starter_code'].keys())}")

        # Sync test_cases collection
        tc_list = updates.get("test_cases", [])
        await db.test_cases.delete_many({"problem_slug": slug})
        if tc_list:
            docs = []
            for tc in tc_list:
                doc = dict(tc)
                doc["problem_slug"] = slug
                docs.append(doc)
            await db.test_cases.insert_many(docs)
        print(f"   Test cases: {len(tc_list)} ({sum(1 for t in tc_list if not t.get('hidden'))} visible, {sum(1 for t in tc_list if t.get('hidden'))} hidden)")

    # Verify
    print("\n" + "=" * 60)
    print("  VERIFICATION")
    print("=" * 60)
    cursor = db.problems.find({"domain": "Frontend"})
    count = 0
    async for p in cursor:
        sc_keys = list(p.get("starter_code", {}).keys())
        tc_count = len(p.get("test_cases", []))
        has_backend_langs = any(k in sc_keys for k in ["python", "go", "cpp", "rust", "java"])
        flag = "⚠️  HAS BACKEND LANGS!" if has_backend_langs else "✅"
        print(f"  {flag} {p['slug']} | langs: {sc_keys} | test_cases: {tc_count}")
        count += 1
    print(f"\nTotal Frontend challenges: {count}")
    print("Done! 🎉")


if __name__ == "__main__":
    asyncio.run(main())
