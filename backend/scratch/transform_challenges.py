# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import re
from app.core.db import get_db

# Pre-packaged beginner friendly content for selected key challenges
CUSTOM_PROBLEM_HELPERS = {
    "lru-cache-implementation": {
        "description": """### 🎯 Objective
Implement a Least Recently Used (LRU) cache class that stores key-value pairs and automatically removes the oldest accessed item when capacity is exceeded.

### 💡 Beginner Friendly Context
Think of an LRU cache like a bookshelf that holds a limited number of books:
- When you read a book (either lookup or add), you place it on the far right.
- If the bookshelf is full and you want to add a new book, you throw away the book on the far left (the one that hasn't been touched for the longest time).

### 📋 Detailed Example
- **LRUCache(2)** (initialize capacity to 2)
- **put(1, 1)** -> Cache contains [1]
- **put(2, 2)** -> Cache contains [2, 1]
- **get(1)** -> Returns 1, moves key 1 to most recent: [1, 2]
- **put(3, 3)** -> Cache is full! Evicts key 2 (least recently used). Cache contains [3, 1]
- **get(2)** -> Returns -1 (not found)

### 🚀 Step-by-Step Implementation Guide
1. **Initialize State**: Setup your capacity and storage (a JavaScript `Map` is perfect because it preserves insertion order!).
2. **Implement get(key)**: Check if key exists. If not, return `-1`. If yes, refresh the key's position (delete and re-insert) and return the value.
3. **Implement put(key, val)**: If key exists, delete it first. If size is at capacity, delete the oldest item (in JS Map: `this.cache.keys().next().value`). Then insert the new value.""",
        "starter_code": {
            "javascript": """class LRUCache {
  constructor(capacity) {
    // STEP 1: Save the capacity limit
    this.capacity = capacity;
    // STEP 2: Use Map since it preserves key insertion order
    this.cache = new Map();
  }

  get(key) {
    // STEP 3: If key is not in cache, return -1
    if (!this.cache.has(key)) return -1;
    
    // STEP 4: Key was accessed! Refresh its position by deleting and re-inserting
    const val = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, val);
    
    return val;
  }

  put(key, value) {
    // STEP 5: If key already exists, delete the old position to refresh it
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.capacity) {
      // STEP 6: Cache is full! Identify and delete the oldest key (the first key in Map)
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }
    // STEP 7: Insert the updated key-value pair
    this.cache.set(key, value);
  }
}
""",
            "python": """class LRUCache:
    def __init__(self, capacity: int):
        # STEP 1: Store capacity limit
        self.capacity = capacity
        # STEP 2: Dictionary to store key-value mapping
        self.cache = {}
        # STEP 3: List to track access order (least recent at start, most recent at end)
        self.order = []

    def get(self, key: int) -> int:
        # STEP 4: Return -1 if key does not exist
        if key not in self.cache:
            return -1
        # STEP 5: Move key to the end of order list to mark as most recently used
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        # STEP 6: If key exists, remove old order tracking
        if key in self.cache:
            self.order.remove(key)
        # STEP 7: If cache is full, evict the oldest key (the first element in order list)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        # STEP 8: Store the key-value pair and record new order
        self.cache[key] = value
        self.order.append(key)
"""
        }
    },
    "thread-safe-kv-store": {
        "description": """### 🎯 Objective
Design a simple in-memory key-value store class where keys can expire after a specific time-to-live (TTL) duration.

### 💡 Beginner Friendly Context
Think of this like a temporary cache:
- You save a username like "john" and set a TTL of 3000ms.
- If you request "john" within 3 seconds, you get the username.
- If you request it after 3 seconds, it will have expired and return `null`.

### 📋 Detailed Example
- **set("session", "abc", 1000)** -> Stores session with 1s expiry
- **get("session")** within 500ms -> Returns `"abc"`
- Wait 1200ms
- **get("session")** -> Returns `null` (since it expired)

### 🚀 Step-by-Step Implementation Guide
1. **Initialize Storage**: Use a standard `Map` to keep records.
2. **Implement set(key, val, ttl_ms)**: Calculate the absolute expiration timestamp (`Date.now() + ttl_ms`). Store the value and the expiration timestamp.
3. **Implement get(key)**: Lookup the entry. If not found, return `null`. If the current time (`Date.now()`) is greater than the expiration timestamp, delete the key from storage and return `null`.""",
        "starter_code": {
            "javascript": """class KVStore {
  constructor() {
    // STEP 1: Use a Map to hold our key-value entries
    this.store = new Map();
  }

  set(key, val, ttl) {
    // STEP 2: Calculate absolute expiration time if TTL is provided
    const expiresAt = ttl ? Date.now() + ttl : null;
    this.store.set(key, { val, expiresAt });
  }

  get(key) {
    // STEP 3: If key doesn't exist, return null
    if (!this.store.has(key)) return null;

    const entry = this.store.get(key);
    // STEP 4: Check if the entry has expired
    if (entry.expiresAt && entry.expiresAt < Date.now()) {
      // Clean up the expired entry
      this.store.delete(key);
      return null;
    }
    return entry.val;
  }
}
"""
        }
    },
    "circular-ring-buffer": {
        "description": """### 🎯 Objective
Implement a circular queue buffer of a fixed size. When writing items, it stores them in a ring.

### 💡 Beginner Friendly Context
A circular buffer is like a circular conveyor belt with a fixed number of slots:
- You add items to the back of the belt, and read them from the front.
- If the belt is full, you cannot add more items unless you read some, or overwrite.

### 📋 Detailed Example
- **CircularBuffer(3)** (initialize capacity to 3)
- **write("A")** -> Buffer holds ["A"]
- **write("B")** -> Buffer holds ["A", "B"]
- **read()** -> Returns "A", buffer now holds ["B"]
- **write("C")**, **write("D")** -> Buffer holds ["B", "C", "D"]

### 🚀 Step-by-Step Implementation Guide
1. **Pointers**: Setup `head` (for reading), `tail` (for writing), and `size` counters.
2. **write(item)**: Check if buffer is full. If not, add `item` at `tail` index, update `tail` using modulo arithmetic (`(this.tail + 1) % this.capacity`), and increase `size`.
3. **read()**: Check if empty. If not, get `item` at `head`, update `head` (`(this.head + 1) % this.capacity`), and decrease `size`.""",
        "starter_code": {
            "javascript": """class CircularBuffer {
  constructor(capacity) {
    // STEP 1: Initialize fixed size storage array
    this.capacity = capacity;
    this.buffer = new Array(capacity);
    this.head = 0; // Pointer for read
    this.tail = 0; // Pointer for write
    this.size = 0; // Current count of items
  }

  write(item) {
    // STEP 2: Check if buffer is full
    if (this.size >= this.capacity) {
      throw new Error("Queue is full");
    }
    // STEP 3: Write item to the tail position
    this.buffer[this.tail] = item;
    // STEP 4: Update tail index wrapping around if capacity is reached
    this.tail = (this.tail + 1) % this.capacity;
    this.size++;
    return true;
  }

  read() {
    // STEP 5: Check if empty
    if (this.size === 0) {
      return null;
    }
    // STEP 6: Retrieve item from head position
    const item = this.buffer[this.head];
    // STEP 7: Clear the slot and update head index wrapping around
    this.buffer[this.head] = undefined;
    this.head = (this.head + 1) % this.capacity;
    this.size--;
    return item;
  }
}
"""
        }
    },
    "debounced-suggestions-hook": {
        "description": """### 🎯 Objective
Implement a custom hook `useDebounce` that delays updating a state value until a specified timeout duration has elapsed since the last change.

### 💡 Beginner Friendly Context
Think of debouncing like an elevator:
- The elevator door doesn't close as soon as you step in. It waits for 5 seconds.
- If someone else steps in within that 5 seconds, the timer resets and it waits another 5 seconds.
- In search bars, this prevents sending a search API request for every keypress.

### 📋 Detailed Example
- User types "a" -> Debounce timer starts
- User types "ab" at 100ms -> Old timer is cancelled, new timer starts
- User stops typing -> Timer finishes at 600ms, value updates to "ab"

### 🚀 Step-by-Step Implementation Guide
1. **State Tracking**: Create a local state to hold the debounced value.
2. **Effect Listener**: Setup a `useEffect` that listens for changes to the input `value` and `delayMs`.
3. **Timer Delay**: Inside the effect, start a timer (`setTimeout`) that updates the local state to the latest value.
4. **Cleanup**: Return a cleanup function inside `useEffect` that runs `clearTimeout(handler)` to cancel the timer if `value` changes again before the delay completes!""",
        "starter_code": {
            "javascript": """import { useState, useEffect } from 'react';

function useDebounce(value, delayMs) {
  // STEP 1: Set up state to hold the debounced value
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // STEP 2: Start a timer to update the debounced value after the delay
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delayMs);

    // STEP 3: Cleanup function clears the timer if value or delay changes
    return () => {
      clearTimeout(handler);
    };
  }, [value, delayMs]); // Run whenever value or delay changes

  return debouncedValue;
}
"""
        }
    },
    "star-rating-feedback-engine": {
        "description": """### 🎯 Objective
Implement a star rating widget class that manages rating select state and hover states.

### 💡 Beginner Friendly Context
Star widgets let users choose a score:
- Hovering over star 3 highlights stars 1, 2, and 3.
- Clicking star 4 permanently locks the score to 4.

### 📋 Detailed Example
- **StarRatingWidget(5)** (5 stars)
- **hover(3)** -> Stars 1, 2, and 3 highlight
- **click(4)** -> Rating locks to 4
- **hoverOut()** -> Highlights revert to active rating (4)

### 🚀 Step-by-Step Implementation Guide
1. **Initialize State**: Save rating and hover rating states.
2. **hover(starIndex)**: Set hover rating to `starIndex`.
3. **click(starIndex)**: Set permanent rating to `starIndex`.
4. **hoverOut()**: Reset hover rating back to `0`.""",
        "starter_code": {
            "javascript": """class StarRatingWidget {
  constructor(totalStars = 5) {
    // STEP 1: Store total star capacity
    this.totalStars = totalStars;
    // STEP 2: Current locked rating
    this.rating = 0;
    // STEP 3: Current temporary hover rating
    this.hoverRating = 0;
  }

  hover(starIndex) {
    // STEP 4: Set the temporary hover index (1-indexed)
    this.hoverRating = starIndex;
  }

  click(starIndex) {
    // STEP 5: Lock in the rating permanently
    this.rating = starIndex;
  }

  hoverOut() {
    // STEP 6: Clear hover state
    this.hoverRating = 0;
  }

  getActiveStarsCount() {
    // STEP 7: Prefer hover score if hovering, otherwise locked score
    return this.hoverRating || this.rating;
  }
}
"""
        }
    },
    "url-query-string-parser": {
        "description": """### 🎯 Objective
Implement a helper function that parses a URL query parameter string (e.g. `?name=alex&tags=dev&tags=ops`) into a clean object representation.

### 💡 Beginner Friendly Context
A query string passes parameters in a URL:
- It starts with `?` (optional).
- Key-value pairs are separated by `&`.
- Equal signs `=` separate keys and values.
- Keys appearing multiple times should collect their values into an array!

### 📋 Detailed Example
- **Input:** `"name=john&role=admin&tag=js&tag=node"`
- **Output:** `{ name: "john", role: "admin", tag: ["js", "node"] }`

### 🚀 Step-by-Step Implementation Guide
1. **Cleanup**: Remove leading `?` if present.
2. **Splitting**: Split the string by `&` to isolate each key-value pair.
3. **Parsing**: For each pair, split by `=` to get the key and value (decode URL characters if necessary).
4. **Aggregation**: Save to object. If key exists, convert to array or push to array.""",
        "starter_code": {
            "javascript": """function parseQuery(queryString) {
  const result = {};
  if (!queryString) return result;

  // STEP 1: Remove optional leading '?'
  const cleanStr = queryString.startsWith('?') ? queryString.slice(1) : queryString;
  if (!cleanStr) return result;

  // STEP 2: Split parameters by '&'
  const pairs = cleanStr.split('&');

  for (const pair of pairs) {
    // STEP 3: Split into key and value
    const parts = pair.split('=');
    const key = decodeURIComponent(parts[0]);
    const value = parts[1] !== undefined ? decodeURIComponent(parts[1]) : '';

    // STEP 4: Save to results mapping array list if keys are duplicated
    if (result[key] !== undefined) {
      if (Array.isArray(result[key])) {
        result[key].push(value);
      } else {
        result[key] = [result[key], value];
      }
    } else {
      result[key] = value;
    }
  }

  return result;
}
"""
        }
    },
    "jwt-token-claims-decoder": {
        "description": """### 🎯 Objective
Implement a function to decode and validate the claims (payload data) inside a JSON Web Token (JWT) string.

### 💡 Beginner Friendly Context
A JWT is a string made of three parts separated by dots `.`:
1. **Header** (defines metadata like algorithm).
2. **Payload** (stores actual token claims like user_id and expiration).
3. **Signature** (verifies authenticity).
Each part is encoded using Base64Url encoding. Decodability simply requires base64 decoding the payload (the middle part).

### 📋 Detailed Example
- **Input:** `"header_b64.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.signature"`
- **Output:** `{ valid: true, payload: { sub: "1234567890", name: "John Doe", iat: 1516239022 } }`

### 🚀 Step-by-Step Implementation Guide
1. **Splitting**: Split the token by dot `.`. It must have exactly 3 parts.
2. **Extracting Payload**: Take the second part (index 1).
3. **Base64 Decoding**: Decode the Base64Url string into a raw JSON string. (Replace `-` with `+` and `_` with `/` to normalize it).
4. **JSON Parsing**: Parse the JSON string into an object and return it.""",
        "starter_code": {
            "javascript": """function decodeAndValidateJWT(tokenStr) {
  const result = { valid: false, payload: {} };
  if (!tokenStr) return result;

  // STEP 1: Split JWT into header, payload, and signature
  const parts = tokenStr.split('.');
  if (parts.length !== 3) return result;

  try {
    // STEP 2: Extract base64url payload
    let base64Url = parts[1];
    
    // STEP 3: Convert base64url to standard base64 encoding format
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    
    // STEP 4: Add base64 padding if needed
    const pad = base64.length % 4;
    if (pad) {
      base64 += '='.repeat(4 - pad);
    }

    // STEP 5: Decode base64 to string
    const jsonStr = atob(base64);
    
    // STEP 6: Parse JSON payload object
    result.payload = JSON.parse(jsonStr);
    result.valid = true;
  } catch (err) {
    result.valid = false;
  }

  return result;
}
"""
        }
    },
    "api-link-header-pagination": {
        "description": """### 🎯 Objective
Implement a helper function that generates an HTTP `Link` header value for paginated REST API responses.

### 💡 Beginner Friendly Context
Pagination splits a long list of items into pages:
- If a client requests items, you return a header telling them how to fetch the `next`, `prev`, `first`, and `last` page.
- The standard format is: `<url>; rel="relation"`.

### 📋 Detailed Example
- **Input:** `"http://api.com/users", page: 2, limit: 10, total: 25`
- **Output:** `"<http://api.com/users?page=1&limit=10>; rel=\"first\", <http://api.com/users?page=1&limit=10>; rel=\"prev\", <http://api.com/users?page=3&limit=10>; rel=\"next\", <http://api.com/users?page=3&limit=10>; rel=\"last\""`

### 🚀 Step-by-Step Implementation Guide
1. **Calculate Pages**: Total pages = `Math.ceil(total / limit)`.
2. **Build URLs**: Append page and limit parameters to the base URL.
3. **Assemble Header**: Map relationship relations and combine into comma-separated links.""",
        "starter_code": {
            "javascript": """function buildPaginationLinkHeader(baseUrl, page, limit, total) {
  const totalPages = Math.ceil(total / limit);
  const links = [];

  const getUrl = (p) => {
    const url = new URL(baseUrl);
    url.searchParams.set("page", p);
    url.searchParams.set("limit", limit);
    return url.toString();
  };

  // STEP 1: First page link
  links.push(`<${getUrl(1)}>; rel="first"`);

  // STEP 2: Previous page link (if page > 1)
  if (page > 1) {
    links.push(`<${getUrl(page - 1)}>; rel="prev"`);
  }

  // STEP 3: Next page link (if page < totalPages)
  if (page < totalPages) {
    links.push(`<${getUrl(page + 1)}>; rel="next"`);
  }

  // STEP 4: Last page link
  links.push(`<${getUrl(totalPages)}>; rel="last"`);

  return links.join(", ");
}
"""
        }
    }
}

DIFFICULTY_MAPPING = {
    "Expert": "Medium",
    "Hard": "Medium",
    "Medium": "Easy",
    "Easy": "Easy"
}

def enhance_description_generic(p):
    orig_desc = p.get("description") or p.get("short_description") or "Solve this coding challenge."
    title = p.get("title")
    domain = p.get("domain")
    
    desc = f"""### 🎯 Objective
{orig_desc}

### 💡 Beginner Friendly Context
This is a beginner-focused **{domain}** engineering task. The goal is to build a reliable, performant, and clean module executing the stated operations. 

### 🚀 Step-by-Step Implementation Guide
1. **Initialize/Setup**: Check input arguments and establish key boundaries or variables.
2. **Core Operations**: Implement the primary algorithms sequentially.
3. **Verification/Return**: Output the calculated result adhering strictly to expected types.
"""
    return desc

def enhance_starter_code_generic(starter_code, slug, title):
    if not starter_code or not isinstance(starter_code, dict):
        return starter_code
    
    updated = {}
    for lang, code in starter_code.items():
        if not code:
            updated[lang] = code
            continue
            
        if lang == "javascript":
            c = code
            if "class" in c:
                if "constructor(" in c:
                    c = c.replace("constructor(", "constructor(\n    // STEP 1: Initialize instance state fields here\n    ")
                # Inject inside empty brackets {}
                c = re.sub(r'(\b\w+)\(([^)]*)\)\s*\{\s*\}', r'\1(\2) {\n    // STEP 2: Implement operations logic\n    // Verify boundary edge cases\n  }', c)
            else:
                if "function " in c:
                    c = c.replace("{\n", "{\n  // STEP 1: Check inputs and boundary conditions\n  // STEP 2: Process core algorithm logic\n  // STEP 3: Return final result\n")
            updated[lang] = c
        elif lang == "python":
            c = code
            if "def " in c:
                # Replace standard pass statements
                c = c.replace("pass", "# STEP 1: Validate inputs\n        # STEP 2: Implement logic steps\n        # STEP 3: Return output\n        pass")
            updated[lang] = c
        elif lang == "typescript":
            c = code
            if "class" in c:
                if "constructor(" in c:
                    c = c.replace("constructor(", "constructor(\n    // STEP 1: Initialize states\n    ")
            updated[lang] = c
        else:
            updated[lang] = code
            
    return updated

async def main():
    db = get_db()
    cursor = db.problems.find({})
    count = 0
    async for p in cursor:
        slug = p.get("slug")
        orig_diff = p.get("difficulty", "Easy")
        new_diff = DIFFICULTY_MAPPING.get(orig_diff, "Easy")
        
        # Determine updated fields
        if slug in CUSTOM_PROBLEM_HELPERS:
            helper = CUSTOM_PROBLEM_HELPERS[slug]
            desc = helper["description"]
            # Merge custom starter code on top of existing keys
            starter_code = p.get("starter_code", {})
            for k, v in helper["starter_code"].items():
                starter_code[k] = v
        else:
            desc = enhance_description_generic(p)
            starter_code = enhance_starter_code_generic(p.get("starter_code"), slug, p.get("title"))
            
        # Update database document
        await db.problems.update_one(
            {"_id": p["_id"]},
            {
                "$set": {
                    "difficulty": new_diff,
                    "description": desc,
                    "starter_code": starter_code,
                    "recommended_for_beginner": True
                }
            }
        )
        count += 1
        print(f"Updated problem #{count}: {slug} (Difficulty: {orig_diff} -> {new_diff})")
        
    print(f"Successfully processed and transformed {count} problems to be beginner-friendly.")

if __name__ == "__main__":
    asyncio.run(main())
