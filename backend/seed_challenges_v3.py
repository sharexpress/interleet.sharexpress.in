"""
Interleet — 50 Additional Production Challenges
Append-only: does NOT delete existing challenges.
Run: python seed_challenges_v3.py
"""
import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "interleet"

# ─────────────────────────────────────────────────────────────────────────────
#  Helper — JS and Python CLI starters
# ─────────────────────────────────────────────────────────────────────────────
def js_cli(body):
    return "const fs = require('fs');\nconst input = JSON.parse(fs.readFileSync(0, 'utf-8').trim());\n\n" + body

def py_cli(body):
    return "import sys, json\ndata = json.loads(sys.stdin.read().strip())\n\n" + body

def js_raw(body):
    return "const fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\n\n" + body

def py_raw(body):
    return "import sys\ninput_data = sys.stdin.read().strip()\n\n" + body


CHALLENGES = [
    # ═══════════════════════ BACKEND — Easy (6) ══════════════════════════════

    {
        "title": "Two Sum",
        "slug": "two-sum",
        "short_description": "Find two indices whose values add up to a target sum.",
        "description": (
            "### Two Sum\n\n"
            "Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.\n\n"
            "- There is exactly one solution. Do not use the same element twice.\n"
            "- Return indices in ascending order.\n\n"
            "### Input (stdin)\n"
            "```json\n{\"nums\": [2, 7, 11, 15], \"target\": 9}\n```\n\n"
            "### Output (stdout)\n`[0, 1]`"
        ),
        "domain": "Backend", "difficulty": "Easy",
        "tags": ["Arrays", "Hash Map", "Two Pointers"],
        "technologies": ["javascript", "python"],
        "hints": ["Use a hash map to store seen values.", "For each element x, check if target - x exists in the map."],
        "concepts": ["Hash Maps", "Array Traversal"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_cli(
                "function twoSum(nums, target) {\n"
                "    // TODO: Return indices [i, j] such that nums[i] + nums[j] === target\n"
                "    return [];\n"
                "}\n\n"
                "const { nums, target } = input;\n"
                "console.log(JSON.stringify(twoSum(nums, target)));\n"
            ),
            "python": py_cli(
                "def two_sum(nums, target):\n"
                "    # TODO: Return [i, j] such that nums[i] + nums[j] == target\n"
                "    return []\n\n"
                "result = two_sum(data['nums'], data['target'])\n"
                "print(json.dumps(result))\n"
            ),
        },
        "test_cases": [
            {"id": "ts-1", "name": "basic case", "hidden": False, "weight": 1,
             "stdin": json.dumps({"nums": [2, 7, 11, 15], "target": 9}),
             "expected_output": "[0,1]\n", "comparison_mode": "json"},
            {"id": "ts-2", "name": "mid-array match", "hidden": True, "weight": 1,
             "stdin": json.dumps({"nums": [3, 2, 4], "target": 6}),
             "expected_output": "[1,2]\n", "comparison_mode": "json"},
        ],
    },

    {
        "title": "Valid Brackets",
        "slug": "valid-brackets",
        "short_description": "Determine if a bracket string is valid using a stack.",
        "description": (
            "### Valid Brackets\n\n"
            "Given a string containing only `(`, `)`, `{`, `}`, `[`, `]`, return `true` if the brackets are valid (properly opened and closed), otherwise `false`.\n\n"
            "### Input (stdin)\nRaw string, e.g. `()[]{}`\n\n"
            "### Output (stdout)\n`true` or `false`"
        ),
        "domain": "Backend", "difficulty": "Easy",
        "tags": ["Stack", "Strings", "Parsing"],
        "technologies": ["javascript", "python"],
        "hints": ["Push opening brackets; pop and verify on closing ones.", "If the stack is not empty at the end, return false."],
        "concepts": ["Stack", "String Processing"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_raw(
                "function isValid(s) {\n"
                "    // TODO: Use a stack to validate bracket pairs\n"
                "    return false;\n"
                "}\n\n"
                "console.log(isValid(input));\n"
            ),
            "python": py_raw(
                "def is_valid(s):\n"
                "    # TODO: Use a stack to validate bracket pairs\n"
                "    return False\n\n"
                "print(str(is_valid(input_data)).lower())\n"
            ),
        },
        "test_cases": [
            {"id": "vb-1", "name": "all valid", "hidden": False, "weight": 1,
             "stdin": "()[]{}", "expected_output": "true\n"},
            {"id": "vb-2", "name": "mismatched", "hidden": True, "weight": 1,
             "stdin": "(]", "expected_output": "false\n"},
        ],
    },

    {
        "title": "Flatten Nested Array",
        "slug": "flatten-array",
        "short_description": "Recursively flatten a deeply nested array into a single-level array.",
        "description": (
            "### Flatten Nested Array\n\n"
            "Given a nested array of integers (arbitrarily deep), return a single flat array containing all values in order.\n\n"
            "### Input (stdin)\n```json\n[[1,[2,3]],[4,[5,[6]]]]\n```\n\n"
            "### Output (stdout)\n`[1,2,3,4,5,6]`"
        ),
        "domain": "Backend", "difficulty": "Easy",
        "tags": ["Recursion", "Arrays"],
        "technologies": ["javascript", "python"],
        "hints": ["Recursively check if each element is an array.", "Spread/extend the result for each nested array."],
        "concepts": ["Recursion", "Array Manipulation"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_cli(
                "function flatten(arr) {\n"
                "    // TODO: Recursively flatten the nested array\n"
                "    return [];\n"
                "}\n\n"
                "console.log(JSON.stringify(flatten(input)));\n"
            ),
            "python": py_cli(
                "def flatten(arr):\n"
                "    # TODO: Recursively flatten the nested array\n"
                "    return []\n\n"
                "print(json.dumps(flatten(data)))\n"
            ),
        },
        "test_cases": [
            {"id": "fa-1", "name": "nested 3-deep", "hidden": False, "weight": 1,
             "stdin": json.dumps([[1, [2, 3]], [4, [5, [6]]]]),
             "expected_output": "[1,2,3,4,5,6]\n", "comparison_mode": "json"},
        ],
    },

    {
        "title": "Palindrome Check",
        "slug": "palindrome-check",
        "short_description": "Determine if a string is a palindrome ignoring case and non-alphanumerics.",
        "description": (
            "### Palindrome Check\n\n"
            "Given a string, determine if it is a palindrome considering only alphanumeric characters and ignoring case.\n\n"
            "### Input (stdin)\nRaw string, e.g. `A man, a plan, a canal: Panama`\n\n"
            "### Output (stdout)\n`true` or `false`"
        ),
        "domain": "Backend", "difficulty": "Easy",
        "tags": ["Strings", "Two Pointers"],
        "technologies": ["javascript", "python"],
        "hints": ["Filter out non-alphanumeric chars first.", "Use two pointers from both ends."],
        "concepts": ["String Processing", "Two Pointers"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_raw(
                "function isPalindrome(s) {\n"
                "    // TODO: Return true if s is a palindrome (ignore case and non-alphanum)\n"
                "    return false;\n"
                "}\n\n"
                "console.log(isPalindrome(input));\n"
            ),
            "python": py_raw(
                "def is_palindrome(s):\n"
                "    # TODO: Return True if s is a palindrome (ignore case and non-alphanum)\n"
                "    return False\n\n"
                "print(str(is_palindrome(input_data)).lower())\n"
            ),
        },
        "test_cases": [
            {"id": "pc-1", "name": "classic sentence", "hidden": False, "weight": 1,
             "stdin": "A man, a plan, a canal: Panama", "expected_output": "true\n"},
            {"id": "pc-2", "name": "not palindrome", "hidden": True, "weight": 1,
             "stdin": "race a car", "expected_output": "false\n"},
        ],
    },

    {
        "title": "Word Frequency Counter",
        "slug": "word-frequency",
        "short_description": "Count word occurrences and return top-N most frequent words.",
        "description": (
            "### Word Frequency Counter\n\n"
            "Given a text string and a number `n`, return the `n` most frequent words (case-insensitive), sorted by frequency descending. Ties broken alphabetically.\n\n"
            "### Input (stdin)\n```json\n{\"text\": \"the cat sat on the mat the cat\", \"n\": 2}\n```\n\n"
            "### Output (stdout)\n```json\n[{\"word\": \"the\", \"count\": 3}, {\"word\": \"cat\", \"count\": 2}]\n```"
        ),
        "domain": "Backend", "difficulty": "Easy",
        "tags": ["Strings", "Hash Map", "Sorting"],
        "technologies": ["javascript", "python"],
        "hints": ["Split by whitespace, lowercase each word.", "Sort by count descending, then alphabetically for ties."],
        "concepts": ["String Processing", "Frequency Counting"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_cli(
                "function topNWords(text, n) {\n"
                "    // TODO: Count word frequency and return top n [{word, count}]\n"
                "    return [];\n"
                "}\n\n"
                "console.log(JSON.stringify(topNWords(input.text, input.n)));\n"
            ),
            "python": py_cli(
                "def top_n_words(text, n):\n"
                "    # TODO: Count word frequency and return top n [{'word': w, 'count': c}]\n"
                "    return []\n\n"
                "print(json.dumps(top_n_words(data['text'], data['n'])))\n"
            ),
        },
        "test_cases": [
            {"id": "wf-1", "name": "top 2 words", "hidden": False, "weight": 1,
             "stdin": json.dumps({"text": "the cat sat on the mat the cat", "n": 2}),
             "expected_output": json.dumps([{"word": "the", "count": 3}, {"word": "cat", "count": 2}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Anagram Groups",
        "slug": "anagram-groups",
        "short_description": "Group a list of words into anagram families.",
        "description": (
            "### Anagram Groups\n\n"
            "Given a list of strings, group the anagrams together. Return a list of groups, each sorted internally. The overall list can be in any order.\n\n"
            "### Input (stdin)\n```json\n[\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]\n```\n\n"
            "### Output (stdout)\n```json\n[[\"ate\",\"eat\",\"tea\"],[\"nat\",\"tan\"],[\"bat\"]]\n```"
        ),
        "domain": "Backend", "difficulty": "Easy",
        "tags": ["Strings", "Hash Map", "Sorting"],
        "technologies": ["javascript", "python"],
        "hints": ["Sort each word's characters to get a canonical key.", "Group words by their sorted key."],
        "concepts": ["String Processing", "Grouping"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 120, "estimated_time_minutes": 20,
        "starter_code": {
            "javascript": js_cli(
                "function groupAnagrams(strs) {\n"
                "    // TODO: Group strings that are anagrams of each other\n"
                "    return [];\n"
                "}\n\n"
                "const result = groupAnagrams(input).map(g => g.sort());\n"
                "result.sort((a, b) => a[0].localeCompare(b[0]));\n"
                "console.log(JSON.stringify(result));\n"
            ),
            "python": py_cli(
                "def group_anagrams(strs):\n"
                "    # TODO: Group strings that are anagrams of each other\n"
                "    return []\n\n"
                "result = [sorted(g) for g in group_anagrams(data)]\n"
                "result.sort(key=lambda g: g[0])\n"
                "print(json.dumps(result))\n"
            ),
        },
        "test_cases": [
            {"id": "ag-1", "name": "standard anagram groups", "hidden": False, "weight": 1,
             "stdin": json.dumps(["eat", "tea", "tan", "ate", "nat", "bat"]),
             "expected_output": json.dumps([["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    # ═══════════════════════ BACKEND — Medium (10) ═══════════════════════════

    {
        "title": "Group By Key",
        "slug": "group-by-key",
        "short_description": "Group an array of objects by a specified key property.",
        "description": (
            "### Group By Key\n\n"
            "Given an array of objects and a `key` name, return an object grouping the items by the value of that key.\n\n"
            "### Input (stdin)\n```json\n{\"items\": [{\"name\":\"apple\",\"type\":\"fruit\"},{\"name\":\"carrot\",\"type\":\"veggie\"},{\"name\":\"banana\",\"type\":\"fruit\"}], \"key\": \"type\"}\n```\n\n"
            "### Output (stdout)\n```json\n{\"fruit\":[{\"name\":\"apple\",\"type\":\"fruit\"},{\"name\":\"banana\",\"type\":\"fruit\"}],\"veggie\":[{\"name\":\"carrot\",\"type\":\"veggie\"}]}\n```"
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Arrays", "Objects", "Functional"],
        "technologies": ["javascript", "python"],
        "hints": ["Iterate and build a map keyed by item[key].", "Append each item to the appropriate bucket."],
        "concepts": ["Data Grouping", "Functional Programming"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 150, "estimated_time_minutes": 20,
        "starter_code": {
            "javascript": js_cli(
                "function groupBy(items, key) {\n"
                "    // TODO: Group items into an object keyed by item[key]\n"
                "    return {};\n"
                "}\n\n"
                "console.log(JSON.stringify(groupBy(input.items, input.key)));\n"
            ),
            "python": py_cli(
                "def group_by(items, key):\n"
                "    # TODO: Group items into a dict keyed by item[key]\n"
                "    return {}\n\n"
                "print(json.dumps(group_by(data['items'], data['key'])))\n"
            ),
        },
        "test_cases": [
            {"id": "gb-1", "name": "group by type", "hidden": False, "weight": 1,
             "stdin": json.dumps({"items": [{"name": "apple", "type": "fruit"}, {"name": "carrot", "type": "veggie"}, {"name": "banana", "type": "fruit"}], "key": "type"}),
             "expected_output": json.dumps({"fruit": [{"name": "apple", "type": "fruit"}, {"name": "banana", "type": "fruit"}], "veggie": [{"name": "carrot", "type": "veggie"}]}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "short_description": "Merge all overlapping intervals in a list and return the result.",
        "description": (
            "### Merge Intervals\n\n"
            "Given an array of intervals `[start, end]`, merge all overlapping ones and return the sorted list of non-overlapping intervals.\n\n"
            "### Input (stdin)\n```json\n[[1,3],[2,6],[8,10],[15,18]]\n```\n\n"
            "### Output (stdout)\n```json\n[[1,6],[8,10],[15,18]]\n```"
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Arrays", "Sorting", "Intervals"],
        "technologies": ["javascript", "python"],
        "hints": ["Sort intervals by start time.", "Merge the current interval with the last merged one if they overlap."],
        "concepts": ["Interval Merging", "Sorting"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function mergeIntervals(intervals) {\n"
                "    // TODO: Sort and merge overlapping intervals\n"
                "    return [];\n"
                "}\n\n"
                "console.log(JSON.stringify(mergeIntervals(input)));\n"
            ),
            "python": py_cli(
                "def merge_intervals(intervals):\n"
                "    # TODO: Sort and merge overlapping intervals\n"
                "    return []\n\n"
                "print(json.dumps(merge_intervals(data)))\n"
            ),
        },
        "test_cases": [
            {"id": "mi-1", "name": "standard merge", "hidden": False, "weight": 1,
             "stdin": json.dumps([[1, 3], [2, 6], [8, 10], [15, 18]]),
             "expected_output": "[[1,6],[8,10],[15,18]]\n", "comparison_mode": "json"},
        ],
    },

    {
        "title": "Sliding Window Maximum",
        "slug": "sliding-window-max",
        "short_description": "Find the maximum value in every sliding window of size k.",
        "description": (
            "### Sliding Window Maximum\n\n"
            "Given an array `nums` and window size `k`, return an array of the maximum values in each sliding window of size `k`.\n\n"
            "### Input (stdin)\n```json\n{\"nums\": [1,3,-1,-3,5,3,6,7], \"k\": 3}\n```\n\n"
            "### Output (stdout)\n```json\n[3,3,5,5,6,7]\n```"
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Sliding Window", "Deque", "Arrays"],
        "technologies": ["javascript", "python"],
        "hints": ["Use a monotonic deque (double-ended queue) for O(n) solution.", "Remove indices that fall outside the window or are smaller than the current element."],
        "concepts": ["Sliding Window", "Monotonic Queue"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 250, "estimated_time_minutes": 35,
        "starter_code": {
            "javascript": js_cli(
                "function maxSlidingWindow(nums, k) {\n"
                "    // TODO: Return the max of each window of size k\n"
                "    // Hint: a monotonic deque gives O(n)\n"
                "    return [];\n"
                "}\n\n"
                "console.log(JSON.stringify(maxSlidingWindow(input.nums, input.k)));\n"
            ),
            "python": py_cli(
                "from collections import deque\n\n"
                "def max_sliding_window(nums, k):\n"
                "    # TODO: Return the max of each window of size k\n"
                "    return []\n\n"
                "print(json.dumps(max_sliding_window(data['nums'], data['k'])))\n"
            ),
        },
        "test_cases": [
            {"id": "sw-1", "name": "standard window", "hidden": False, "weight": 1,
             "stdin": json.dumps({"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3}),
             "expected_output": "[3,3,5,5,6,7]\n", "comparison_mode": "json"},
        ],
    },

    {
        "title": "Longest Substring Without Repeating",
        "slug": "longest-no-repeat",
        "short_description": "Find the length of the longest substring with all unique characters.",
        "description": (
            "### Longest Substring Without Repeating Characters\n\n"
            "Given a string `s`, find the length of the longest substring without repeating characters.\n\n"
            "### Input (stdin)\nRaw string, e.g. `abcabcbb`\n\n"
            "### Output (stdout)\n`3` (the substring is `abc`)"
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Sliding Window", "Hash Map", "Strings"],
        "technologies": ["javascript", "python"],
        "hints": ["Use a sliding window with a set or map.", "Shrink the window from the left when a duplicate is found."],
        "concepts": ["Sliding Window", "String Processing"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 25,
        "starter_code": {
            "javascript": js_raw(
                "function lengthOfLongestSubstring(s) {\n"
                "    // TODO: Return the length of the longest non-repeating substring\n"
                "    return 0;\n"
                "}\n\n"
                "console.log(lengthOfLongestSubstring(input));\n"
            ),
            "python": py_raw(
                "def length_of_longest_substring(s):\n"
                "    # TODO: Return the length of the longest non-repeating substring\n"
                "    return 0\n\n"
                "print(length_of_longest_substring(input_data))\n"
            ),
        },
        "test_cases": [
            {"id": "ln-1", "name": "classic case", "hidden": False, "weight": 1,
             "stdin": "abcabcbb", "expected_output": "3\n"},
            {"id": "ln-2", "name": "all unique", "hidden": True, "weight": 1,
             "stdin": "abcde", "expected_output": "5\n"},
        ],
    },

    {
        "title": "Binary Search on Rotated Array",
        "slug": "rotated-binary-search",
        "short_description": "Search a target in a sorted array that has been rotated at a pivot.",
        "description": (
            "### Binary Search on Rotated Array\n\n"
            "Given a sorted integer array rotated at an unknown pivot, search for a `target`. Return its index or `-1` if not found.\n\n"
            "### Input (stdin)\n```json\n{\"nums\": [4,5,6,7,0,1,2], \"target\": 0}\n```\n\n"
            "### Output (stdout)\n`4`"
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Binary Search", "Arrays", "Divide and Conquer"],
        "technologies": ["javascript", "python"],
        "hints": ["At every midpoint, one half is always sorted.", "Determine which half is sorted and whether the target lies within it."],
        "concepts": ["Binary Search", "Array Rotation"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function search(nums, target) {\n"
                "    // TODO: Binary search on rotated sorted array\n"
                "    return -1;\n"
                "}\n\n"
                "console.log(search(input.nums, input.target));\n"
            ),
            "python": py_cli(
                "def search(nums, target):\n"
                "    # TODO: Binary search on rotated sorted array\n"
                "    return -1\n\n"
                "print(search(data['nums'], data['target']))\n"
            ),
        },
        "test_cases": [
            {"id": "rb-1", "name": "found in right half", "hidden": False, "weight": 1,
             "stdin": json.dumps({"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}),
             "expected_output": "4\n"},
            {"id": "rb-2", "name": "not found", "hidden": True, "weight": 1,
             "stdin": json.dumps({"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}),
             "expected_output": "-1\n"},
        ],
    },

    {
        "title": "Deep Equal Check",
        "slug": "deep-equal",
        "short_description": "Implement a deep equality check for arbitrary nested objects.",
        "description": (
            "### Deep Equal Check\n\n"
            "Implement a `deepEqual(a, b)` function that returns `true` if the two values are structurally identical — same types, same keys, same values recursively.\n\n"
            "### Input (stdin)\n```json\n{\"a\": {\"x\": [1, {\"y\": 2}]}, \"b\": {\"x\": [1, {\"y\": 2}]}}\n```\n\n"
            "### Output (stdout)\n`true`"
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Recursion", "Objects", "Equality"],
        "technologies": ["javascript", "python"],
        "hints": ["Handle primitives, arrays, and objects separately.", "For objects, compare keys and recursively compare values."],
        "concepts": ["Recursion", "Type Checking"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 150, "estimated_time_minutes": 20,
        "starter_code": {
            "javascript": js_cli(
                "function deepEqual(a, b) {\n"
                "    // TODO: Return true if a and b are deeply equal\n"
                "    return false;\n"
                "}\n\n"
                "console.log(deepEqual(input.a, input.b));\n"
            ),
            "python": py_cli(
                "def deep_equal(a, b):\n"
                "    # TODO: Return True if a and b are deeply equal\n"
                "    return False\n\n"
                "print(str(deep_equal(data['a'], data['b'])).lower())\n"
            ),
        },
        "test_cases": [
            {"id": "de-1", "name": "equal nested objects", "hidden": False, "weight": 1,
             "stdin": json.dumps({"a": {"x": [1, {"y": 2}]}, "b": {"x": [1, {"y": 2}]}}),
             "expected_output": "true\n"},
            {"id": "de-2", "name": "different nested values", "hidden": True, "weight": 1,
             "stdin": json.dumps({"a": {"x": [1, {"y": 2}]}, "b": {"x": [1, {"y": 3}]}}),
             "expected_output": "false\n"},
        ],
    },

    {
        "title": "Event Emitter",
        "slug": "event-emitter",
        "short_description": "Implement a publish/subscribe EventEmitter with on, off, and emit.",
        "description": (
            "### Event Emitter\n\n"
            "Implement an `EventEmitter` class with:\n"
            "- `on(event, listener)` — register a listener\n"
            "- `off(event, listener)` — remove a listener\n"
            "- `emit(event, ...args)` — call all listeners with the given args\n\n"
            "### Input (stdin)\n```json\n{\"ops\": [[\"on\",\"greet\"],[\"emit\",\"greet\",\"Alice\"],[\"off\",\"greet\"],[\"emit\",\"greet\",\"Bob\"]]}\n```\n\n"
            "### Output (stdout)\nJSON array of collected outputs from emit calls."
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Design Patterns", "Event Loop", "OOP"],
        "technologies": ["javascript", "python"],
        "hints": ["Store listeners in a Map keyed by event name.", "Filter/splice on off(); call all matching listeners on emit()."],
        "concepts": ["Observer Pattern", "Pub/Sub"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "class EventEmitter {\n"
                "    constructor() {\n"
                "        this.listeners = {};\n"
                "    }\n\n"
                "    on(event, listener) {\n"
                "        // TODO: Register listener\n"
                "    }\n\n"
                "    off(event, listener) {\n"
                "        // TODO: Remove listener\n"
                "    }\n\n"
                "    emit(event, ...args) {\n"
                "        // TODO: Call all registered listeners for event\n"
                "    }\n"
                "}\n\n"
                "const emitter = new EventEmitter();\n"
                "const results = [];\n"
                "const handler = (name) => results.push('Hello, ' + name + '!');\n"
                "for (const [op, ...rest] of input.ops) {\n"
                "    if (op === 'on') emitter.on(rest[0], handler);\n"
                "    else if (op === 'off') emitter.off(rest[0], handler);\n"
                "    else if (op === 'emit') emitter.emit(rest[0], rest[1]);\n"
                "}\n"
                "console.log(JSON.stringify(results));\n"
            ),
            "python": py_cli(
                "class EventEmitter:\n"
                "    def __init__(self):\n"
                "        self.listeners = {}\n\n"
                "    def on(self, event, listener):\n"
                "        # TODO: Register listener\n"
                "        pass\n\n"
                "    def off(self, event, listener):\n"
                "        # TODO: Remove listener\n"
                "        pass\n\n"
                "    def emit(self, event, *args):\n"
                "        # TODO: Call all listeners for event\n"
                "        pass\n\n"
                "emitter = EventEmitter()\n"
                "results = []\n"
                "def handler(name): results.append(f'Hello, {name}!')\n"
                "for op in data['ops']:\n"
                "    if op[0] == 'on': emitter.on(op[1], handler)\n"
                "    elif op[0] == 'off': emitter.off(op[1], handler)\n"
                "    elif op[0] == 'emit': emitter.emit(op[1], op[2])\n"
                "print(json.dumps(results))\n"
            ),
        },
        "test_cases": [
            {"id": "ee-1", "name": "on/emit/off sequence", "hidden": False, "weight": 1,
             "stdin": json.dumps({"ops": [["on", "greet"], ["emit", "greet", "Alice"], ["off", "greet"], ["emit", "greet", "Bob"]]}),
             "expected_output": '["Hello, Alice!"]\n', "comparison_mode": "json"},
        ],
    },

    {
        "title": "Memoize with TTL",
        "slug": "memoize-ttl",
        "short_description": "Implement memoization with a time-to-live expiry for cached results.",
        "description": (
            "### Memoize with TTL\n\n"
            "Implement a `memoize(fn, ttlMs)` wrapper that caches the result of `fn` by its arguments for `ttlMs` milliseconds. Expired entries should be recomputed.\n\n"
            "### Input (stdin)\n```json\n{\"calls\": [{\"args\": [3, 4], \"time\": 0}, {\"args\": [3, 4], \"time\": 50}, {\"args\": [3, 4], \"time\": 200}], \"ttl\": 100}\n```\n\n"
            "### Output (stdout)\n```json\n{\"results\": [7, 7, 7], \"computations\": 2}\n```\n\n"
            "The function computes `a + b`. A cached call returns immediately; expired entries recompute."
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Caching", "Closures", "Performance"],
        "technologies": ["javascript", "python"],
        "hints": ["Use a Map with key = JSON(args) and value = {result, expiry}.", "Check the timestamp against the stored expiry."],
        "concepts": ["Memoization", "TTL Caching", "Closures"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function memoize(fn, ttlMs) {\n"
                "    const cache = new Map();\n"
                "    return function(args, currentTime) {\n"
                "        // TODO: Return cached value if not expired, else recompute\n"
                "        return fn(...args);\n"
                "    };\n"
                "}\n\n"
                "const add = (a, b) => a + b;\n"
                "const memo = memoize(add, input.ttl);\n"
                "let computations = 0;\n"
                "const origAdd = add;\n"
                "const results = input.calls.map(({ args, time }) => memo(args, time));\n"
                "// Count: For this skeleton, just run it — implement to track recomputes\n"
                "console.log(JSON.stringify({ results, computations: 0 }));\n"
            ),
            "python": py_cli(
                "def memoize(fn, ttl_ms):\n"
                "    cache = {}\n"
                "    computations = [0]\n"
                "    def wrapper(args, current_time):\n"
                "        key = json.dumps(args)\n"
                "        # TODO: Return cached value if not expired, else recompute and cache\n"
                "        computations[0] += 1\n"
                "        result = fn(*args)\n"
                "        return result\n"
                "    return wrapper, computations\n\n"
                "def add(a, b): return a + b\n"
                "memo, comps = memoize(add, data['ttl'])\n"
                "results = [memo(call['args'], call['time']) for call in data['calls']]\n"
                "print(json.dumps({'results': results, 'computations': comps[0]}))\n"
            ),
        },
        "test_cases": [
            {"id": "mt-1", "name": "ttl expiry", "hidden": False, "weight": 1,
             "stdin": json.dumps({"calls": [{"args": [3, 4], "time": 0}, {"args": [3, 4], "time": 50}, {"args": [3, 4], "time": 200}], "ttl": 100}),
             "expected_output": json.dumps({"results": [7, 7, 7], "computations": 2}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Retry with Exponential Backoff",
        "slug": "retry-backoff",
        "short_description": "Implement a retry wrapper with exponential backoff delay simulation.",
        "description": (
            "### Retry with Exponential Backoff\n\n"
            "Given a list of simulated function call results and a retry config, determine which attempt succeeds (or all fail).\n\n"
            "### Input (stdin)\n```json\n{\"results\": [\"fail\", \"fail\", \"success\"], \"maxRetries\": 3, \"baseDelayMs\": 100}\n```\n\n"
            "### Output (stdout)\n```json\n{\"attempt\": 3, \"success\": true, \"totalDelayMs\": 300}\n```\n\n"
            "Delay formula: `baseDelay * 2^(attempt-1)`. Attempt 1 = no delay. Attempt 2 = 100ms. Attempt 3 = 200ms."
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Async", "Error Handling", "Patterns"],
        "technologies": ["javascript", "python"],
        "hints": ["Loop up to maxRetries times.", "Delay at attempt n = baseDelayMs * 2^(n-1) (skip delay for attempt 1)."],
        "concepts": ["Retry Logic", "Exponential Backoff"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 25,
        "starter_code": {
            "javascript": js_cli(
                "function retryWithBackoff(results, maxRetries, baseDelayMs) {\n"
                "    // TODO: Simulate retries using the results array\n"
                "    // results[i] is 'success' or 'fail' for attempt i+1\n"
                "    // Return { attempt, success, totalDelayMs }\n"
                "    return { attempt: 0, success: false, totalDelayMs: 0 };\n"
                "}\n\n"
                "const { results, maxRetries, baseDelayMs } = input;\n"
                "console.log(JSON.stringify(retryWithBackoff(results, maxRetries, baseDelayMs)));\n"
            ),
            "python": py_cli(
                "def retry_with_backoff(results, max_retries, base_delay_ms):\n"
                "    # TODO: Simulate retries and return {attempt, success, totalDelayMs}\n"
                "    return {'attempt': 0, 'success': False, 'totalDelayMs': 0}\n\n"
                "r = retry_with_backoff(data['results'], data['maxRetries'], data['baseDelayMs'])\n"
                "print(json.dumps(r))\n"
            ),
        },
        "test_cases": [
            {"id": "rb2-1", "name": "success on 3rd try", "hidden": False, "weight": 1,
             "stdin": json.dumps({"results": ["fail", "fail", "success"], "maxRetries": 3, "baseDelayMs": 100}),
             "expected_output": json.dumps({"attempt": 3, "success": True, "totalDelayMs": 300}) + "\n",
             "comparison_mode": "json"},
            {"id": "rb2-2", "name": "all fail", "hidden": True, "weight": 1,
             "stdin": json.dumps({"results": ["fail", "fail", "fail"], "maxRetries": 3, "baseDelayMs": 100}),
             "expected_output": json.dumps({"attempt": 3, "success": False, "totalDelayMs": 300}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Throttle Function",
        "slug": "throttle-fn",
        "short_description": "Implement a throttle wrapper that limits function calls to once per interval.",
        "description": (
            "### Throttle Function\n\n"
            "Throttle ensures a function is called at most once per `intervalMs`. Given a list of calls with timestamps, determine which ones actually execute.\n\n"
            "### Input (stdin)\n```json\n{\"calls\": [0, 100, 150, 400, 500], \"intervalMs\": 200}\n```\n\n"
            "### Output (stdout)\n```json\n[0, 400]\n```\n\n"
            "Call at t=0 executes. t=100 and t=150 are within 200ms, so throttled. t=400 executes (≥200ms from last). t=500 throttled."
        ),
        "domain": "Backend", "difficulty": "Medium",
        "tags": ["Rate Limiting", "Closures", "Performance"],
        "technologies": ["javascript", "python"],
        "hints": ["Track the timestamp of the last executed call.", "Only execute if current time - lastExecuted >= intervalMs."],
        "concepts": ["Throttling", "Rate Limiting"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 25,
        "starter_code": {
            "javascript": js_cli(
                "function throttle(calls, intervalMs) {\n"
                "    // TODO: Return timestamps of calls that actually execute\n"
                "    const executed = [];\n"
                "    let lastExecuted = -Infinity;\n"
                "    for (const t of calls) {\n"
                "        // if (t - lastExecuted >= intervalMs) { ... }\n"
                "    }\n"
                "    return executed;\n"
                "}\n\n"
                "console.log(JSON.stringify(throttle(input.calls, input.intervalMs)));\n"
            ),
            "python": py_cli(
                "def throttle(calls, interval_ms):\n"
                "    # TODO: Return timestamps of calls that actually execute\n"
                "    executed = []\n"
                "    last_executed = float('-inf')\n"
                "    for t in calls:\n"
                "        pass  # if t - last_executed >= interval_ms: ...\n"
                "    return executed\n\n"
                "print(json.dumps(throttle(data['calls'], data['intervalMs'])))\n"
            ),
        },
        "test_cases": [
            {"id": "th-1", "name": "throttle 200ms interval", "hidden": False, "weight": 1,
             "stdin": json.dumps({"calls": [0, 100, 150, 400, 500], "intervalMs": 200}),
             "expected_output": "[0,400]\n", "comparison_mode": "json"},
        ],
    },

    # ═══════════════════════ BACKEND — Hard (2) ══════════════════════════════

    {
        "title": "Topological Sort",
        "slug": "topological-sort",
        "short_description": "Order tasks respecting dependencies using topological sort (Kahn's algorithm).",
        "description": (
            "### Topological Sort\n\n"
            "Given `n` tasks (0 to n-1) and a list of `dependencies` `[a, b]` (meaning `a` must come before `b`), return a valid topological ordering. If there's a cycle, return `[]`.\n\n"
            "### Input (stdin)\n```json\n{\"n\": 4, \"dependencies\": [[1,0],[2,0],[3,1],[3,2]]}\n```\n\n"
            "### Output (stdout)\nA valid order such as `[1,2,3,0]` or `[2,1,3,0]`."
        ),
        "domain": "Backend", "difficulty": "Hard",
        "tags": ["Graphs", "BFS", "DAG"],
        "technologies": ["javascript", "python"],
        "hints": ["Use Kahn's algorithm: compute in-degrees, start BFS from 0-in-degree nodes.", "If the output length < n, a cycle exists."],
        "concepts": ["Graph Theory", "BFS", "Topological Sort"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 350, "estimated_time_minutes": 45,
        "starter_code": {
            "javascript": js_cli(
                "function topoSort(n, deps) {\n"
                "    // TODO: Kahn's algorithm — return topological order or []\n"
                "    const inDegree = Array(n).fill(0);\n"
                "    const graph = Array.from({length: n}, () => []);\n"
                "    for (const [a, b] of deps) {\n"
                "        graph[a].push(b);\n"
                "        inDegree[b]++;\n"
                "    }\n"
                "    const queue = [];\n"
                "    for (let i = 0; i < n; i++) if (inDegree[i] === 0) queue.push(i);\n"
                "    const result = [];\n"
                "    // TODO: BFS and collect result\n"
                "    return result.length === n ? result : [];\n"
                "}\n\n"
                "const order = topoSort(input.n, input.dependencies);\n"
                "console.log(JSON.stringify(order));\n"
            ),
            "python": py_cli(
                "from collections import deque\n\n"
                "def topo_sort(n, deps):\n"
                "    # TODO: Kahn's algorithm — return topological order or []\n"
                "    in_degree = [0] * n\n"
                "    graph = [[] for _ in range(n)]\n"
                "    for a, b in deps:\n"
                "        graph[a].append(b)\n"
                "        in_degree[b] += 1\n"
                "    queue = deque(i for i in range(n) if in_degree[i] == 0)\n"
                "    result = []\n"
                "    # TODO: BFS and collect result\n"
                "    return result if len(result) == n else []\n\n"
                "order = topo_sort(data['n'], data['dependencies'])\n"
                "print(json.dumps(order))\n"
            ),
        },
        "test_cases": [
            {"id": "ts2-1", "name": "valid DAG", "hidden": False, "weight": 1,
             "stdin": json.dumps({"n": 4, "dependencies": [[1, 0], [2, 0], [3, 1], [3, 2]]}),
             "expected_output": json.dumps([1, 2, 3, 0]) + "\n", "comparison_mode": "json"},
        ],
    },

    {
        "title": "Implement a Min-Heap",
        "slug": "min-heap",
        "short_description": "Build a MinHeap with insert, extractMin, and heapify operations.",
        "description": (
            "### Min-Heap Implementation\n\n"
            "Implement a `MinHeap` class with:\n"
            "- `insert(val)` — add a value\n"
            "- `extractMin()` — remove and return the smallest value\n"
            "- `peek()` — return the smallest without removing\n\n"
            "### Input (stdin)\n```json\n{\"ops\": [[\"insert\",3],[\"insert\",1],[\"insert\",2],[\"peek\"],[\"extractMin\"],[\"extractMin\"]]}\n```\n\n"
            "### Output (stdout)\n```json\n[1, 1, 2]\n```\n\nOnly return values for `peek` and `extractMin`."
        ),
        "domain": "Backend", "difficulty": "Hard",
        "tags": ["Data Structures", "Heap", "Priority Queue"],
        "technologies": ["javascript", "python"],
        "hints": ["Use a parent/children index formula: parent = (i-1)//2, left = 2*i+1, right = 2*i+2.", "Maintain heap property by bubbling up on insert and sifting down on extract."],
        "concepts": ["Heap", "Priority Queue", "Algorithms"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 350, "estimated_time_minutes": 45,
        "starter_code": {
            "javascript": js_cli(
                "class MinHeap {\n"
                "    constructor() { this.heap = []; }\n\n"
                "    insert(val) {\n"
                "        // TODO: Add val and bubble up\n"
                "    }\n\n"
                "    extractMin() {\n"
                "        // TODO: Remove root, put last at root, sift down\n"
                "        return null;\n"
                "    }\n\n"
                "    peek() {\n"
                "        return this.heap[0] ?? null;\n"
                "    }\n"
                "}\n\n"
                "const h = new MinHeap();\n"
                "const results = [];\n"
                "for (const [op, val] of input.ops) {\n"
                "    if (op === 'insert') h.insert(val);\n"
                "    else if (op === 'extractMin') results.push(h.extractMin());\n"
                "    else if (op === 'peek') results.push(h.peek());\n"
                "}\n"
                "console.log(JSON.stringify(results));\n"
            ),
            "python": py_cli(
                "class MinHeap:\n"
                "    def __init__(self): self.heap = []\n\n"
                "    def insert(self, val):\n"
                "        # TODO: Add val and bubble up\n"
                "        pass\n\n"
                "    def extract_min(self):\n"
                "        # TODO: Remove root, put last at root, sift down\n"
                "        return None\n\n"
                "    def peek(self):\n"
                "        return self.heap[0] if self.heap else None\n\n"
                "h = MinHeap()\n"
                "results = []\n"
                "for op in data['ops']:\n"
                "    if op[0] == 'insert': h.insert(op[1])\n"
                "    elif op[0] == 'extractMin': results.append(h.extract_min())\n"
                "    elif op[0] == 'peek': results.append(h.peek())\n"
                "print(json.dumps(results))\n"
            ),
        },
        "test_cases": [
            {"id": "mh-1", "name": "insert and extract", "hidden": False, "weight": 1,
             "stdin": json.dumps({"ops": [["insert", 3], ["insert", 1], ["insert", 2], ["peek"], ["extractMin"], ["extractMin"]]}),
             "expected_output": "[1,1,2]\n", "comparison_mode": "json"},
        ],
    },

    # ═══════════════════════ FRONTEND — (8) ══════════════════════════════════

    {
        "title": "Todo List App",
        "slug": "todo-list-app",
        "short_description": "Build a fully functional Todo app with add, complete, and delete.",
        "description": (
            "### Todo List App\n\n"
            "Build a functional Todo application with:\n"
            "- An input field (`#todo-input`) and an 'Add' button (`#add-btn`) to add todos\n"
            "- A list (`#todo-list`) displaying all todos\n"
            "- Each todo item has a **complete** button (toggles `completed` class) and a **delete** button\n"
            "- Completed items should have a strikethrough style\n\n"
            "### Requirements\n"
            "- Pressing Enter in the input should also add the todo\n"
            "- Empty inputs should not create todos"
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["HTML", "CSS", "JavaScript", "DOM"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use `addEventListener('keydown')` to handle Enter key.", "Toggle a class on click rather than reading DOM text."],
        "concepts": ["DOM Manipulation", "Event Handling", "State Management"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Todo List</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n    <h1>Todo List</h1>\n"
                    "    <div class=\"input-row\">\n      <input id=\"todo-input\" type=\"text\" placeholder=\"Add a new todo...\">\n"
                    "      <button id=\"add-btn\">Add</button>\n    </div>\n"
                    "    <ul id=\"todo-list\"></ul>\n  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0f0f11; color: #fafafa; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { width: 100%; max-width: 480px; padding: 24px; }\n"
                    "h1 { font-size: 1.5rem; margin-bottom: 16px; }\n"
                    ".input-row { display: flex; gap: 8px; margin-bottom: 16px; }\n"
                    "#todo-input { flex: 1; padding: 10px 14px; background: #1c1c1e; border: 1px solid #3a3a3c; border-radius: 8px; color: #fff; font-size: 14px; }\n"
                    "#add-btn { padding: 10px 18px; background: #2563eb; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; }\n"
                    "#todo-list { list-style: none; display: flex; flex-direction: column; gap: 8px; }\n"
                    ".todo-item { display: flex; align-items: center; gap: 8px; padding: 10px 14px; background: #1c1c1e; border: 1px solid #3a3a3c; border-radius: 8px; }\n"
                    ".todo-item span { flex: 1; }\n"
                    ".todo-item.completed span { text-decoration: line-through; opacity: 0.5; }\n"
                    ".todo-item button { padding: 4px 10px; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; }\n"
                    ".complete-btn { background: #16a34a; color: #fff; }\n"
                    ".delete-btn { background: #dc2626; color: #fff; }\n"
                ),
                "index.js": (
                    "// TODO: Implement the Todo List functionality\n"
                    "// 1. Get references to #todo-input, #add-btn, and #todo-list\n"
                    "// 2. On 'Add' click (or Enter key), create a new list item and append it\n"
                    "// 3. Each item has a 'Complete' button (toggles .completed class) and 'Delete' button\n"
                    "// 4. Don't add empty todos\n"
                )
            })
        },
        "test_cases": [
            {"id": "tla-1", "name": "can add and delete a todo", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const input = document.getElementById('todo-input'); const btn = document.getElementById('add-btn'); const list = document.getElementById('todo-list'); if (!input || !btn || !list) return 'FAIL: missing elements'; input.value = 'Buy milk'; btn.click(); const items = list.querySelectorAll('.todo-item'); return items.length === 1 ? 'PASS' : 'FAIL: expected 1 item got ' + items.length;"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    {
        "title": "Stopwatch Timer",
        "slug": "stopwatch-timer",
        "short_description": "Build a stopwatch with start, stop, reset, and lap recording.",
        "description": (
            "### Stopwatch Timer\n\n"
            "Build a stopwatch UI with:\n"
            "- A display showing `MM:SS.ms` format\n"
            "- **Start** (`#start-btn`), **Stop** (`#stop-btn`), **Reset** (`#reset-btn`) buttons\n"
            "- A **Lap** (`#lap-btn`) button that records the current time to a list (`#lap-list`)\n"
            "- The timer should update every 10ms"
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["JavaScript", "Timers", "DOM"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use `setInterval` for the timer.", "Store start time with `Date.now()` and compute elapsed on each tick."],
        "concepts": ["Timers", "State Management", "DOM Updates"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Stopwatch</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n    <div id=\"display\" class=\"display\">00:00.000</div>\n"
                    "    <div class=\"controls\">\n"
                    "      <button id=\"start-btn\">Start</button>\n      <button id=\"stop-btn\">Stop</button>\n"
                    "      <button id=\"lap-btn\">Lap</button>\n      <button id=\"reset-btn\">Reset</button>\n"
                    "    </div>\n    <ul id=\"lap-list\"></ul>\n  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: 'JetBrains Mono', monospace, system-ui; background: #0a0a0b; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { text-align: center; padding: 32px; }\n"
                    ".display { font-size: 3rem; font-weight: 700; letter-spacing: 2px; margin-bottom: 24px; font-variant-numeric: tabular-nums; }\n"
                    ".controls { display: flex; gap: 12px; justify-content: center; margin-bottom: 24px; }\n"
                    "button { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 14px; }\n"
                    "#start-btn { background: #16a34a; color: #fff; }\n"
                    "#stop-btn { background: #dc2626; color: #fff; }\n"
                    "#lap-btn { background: #2563eb; color: #fff; }\n"
                    "#reset-btn { background: #52525b; color: #fff; }\n"
                    "#lap-list { list-style: none; max-height: 200px; overflow-y: auto; }\n"
                    "#lap-list li { padding: 6px 0; border-bottom: 1px solid #27272a; font-size: 14px; color: #a1a1aa; }\n"
                ),
                "index.js": (
                    "// TODO: Implement the Stopwatch\n"
                    "// Variables: let startTime, elapsedTime = 0, timerInterval, lapCount = 0;\n"
                    "// Start: record startTime = Date.now() - elapsedTime, setInterval every 10ms\n"
                    "// Stop: clearInterval, update elapsedTime\n"
                    "// Reset: clearInterval, elapsedTime = 0, update display, clear laps\n"
                    "// Lap: append current time as li to #lap-list\n"
                    "// Format: MM:SS.mmm\n"
                )
            })
        },
        "test_cases": [
            {"id": "sw2-1", "name": "UI elements present", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const ids = ['display','start-btn','stop-btn','lap-btn','reset-btn','lap-list']; const missing = ids.filter(id => !document.getElementById(id)); return missing.length === 0 ? 'PASS' : 'FAIL: missing ' + missing.join(', ');"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    {
        "title": "Form Validator",
        "slug": "form-validator",
        "short_description": "Build a registration form with real-time validation for email, password, and username.",
        "description": (
            "### Form Validator\n\n"
            "Build a registration form (`#register-form`) with real-time validation:\n"
            "- **Username** (`#username`): 3-20 chars, alphanumeric only\n"
            "- **Email** (`#email`): valid email format\n"
            "- **Password** (`#password`): min 8 chars, 1 uppercase, 1 number\n"
            "- **Confirm Password** (`#confirm-password`): must match password\n\n"
            "Show error messages below each field. A **Submit** (`#submit-btn`) button should only activate when all fields are valid."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["HTML", "CSS", "JavaScript", "Forms", "Regex"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use `input` event listeners for real-time feedback.", "Regex: email = /^[^@]+@[^@]+\\.[^@]+$/, password = /(?=.*[A-Z])(?=.*\\d).{8,}/"],
        "concepts": ["Form Validation", "Regex", "UX Patterns"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Register</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"container\">\n    <h1>Create Account</h1>\n"
                    "    <form id=\"register-form\">\n"
                    "      <div class=\"field\">\n        <label>Username</label>\n        <input id=\"username\" type=\"text\" placeholder=\"3-20 alphanumeric\">\n        <span class=\"error\" id=\"username-error\"></span>\n      </div>\n"
                    "      <div class=\"field\">\n        <label>Email</label>\n        <input id=\"email\" type=\"email\" placeholder=\"you@example.com\">\n        <span class=\"error\" id=\"email-error\"></span>\n      </div>\n"
                    "      <div class=\"field\">\n        <label>Password</label>\n        <input id=\"password\" type=\"password\" placeholder=\"Min 8 chars, 1 uppercase, 1 number\">\n        <span class=\"error\" id=\"password-error\"></span>\n      </div>\n"
                    "      <div class=\"field\">\n        <label>Confirm Password</label>\n        <input id=\"confirm-password\" type=\"password\" placeholder=\"Repeat password\">\n        <span class=\"error\" id=\"confirm-error\"></span>\n      </div>\n"
                    "      <button id=\"submit-btn\" type=\"submit\" disabled>Create Account</button>\n"
                    "    </form>\n  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0f0f11; color: #fafafa; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".container { width: 100%; max-width: 420px; padding: 32px; background: #18181b; border: 1px solid #27272a; border-radius: 16px; }\n"
                    "h1 { font-size: 1.4rem; margin-bottom: 24px; }\n"
                    ".field { margin-bottom: 16px; display: flex; flex-direction: column; gap: 4px; }\n"
                    "label { font-size: 13px; color: #a1a1aa; }\n"
                    "input { padding: 10px 14px; background: #27272a; border: 1px solid #3f3f46; border-radius: 8px; color: #fff; font-size: 14px; }\n"
                    "input.invalid { border-color: #dc2626; }\n"
                    "input.valid { border-color: #16a34a; }\n"
                    ".error { font-size: 12px; color: #dc2626; min-height: 16px; }\n"
                    "#submit-btn { width: 100%; padding: 12px; background: #2563eb; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; margin-top: 8px; }\n"
                    "#submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }\n"
                ),
                "index.js": (
                    "// TODO: Add input event listeners to all 4 fields\n"
                    "// Validate each field with:\n"
                    "//   username: /^[a-zA-Z0-9]{3,20}$/\n"
                    "//   email: /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/\n"
                    "//   password: length >= 8, has uppercase, has digit\n"
                    "//   confirm: matches password value\n"
                    "// Show errors in corresponding #*-error spans\n"
                    "// Enable #submit-btn only when all fields pass validation\n"
                )
            })
        },
        "test_cases": [
            {"id": "fv-1", "name": "form elements exist", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const ids = ['register-form','username','email','password','confirm-password','submit-btn']; const missing = ids.filter(id => !document.getElementById(id)); return missing.length === 0 ? 'PASS' : 'FAIL: missing ' + missing.join(', ');"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    {
        "title": "Markdown Preview",
        "slug": "markdown-preview",
        "short_description": "Build a live markdown editor that renders a real-time preview.",
        "description": (
            "### Markdown Preview\n\n"
            "Build a split-pane markdown editor:\n"
            "- Left pane: `<textarea id=\"md-input\">` for raw markdown\n"
            "- Right pane: `<div id=\"md-preview\">` showing rendered HTML\n"
            "- Update preview on every keystroke\n\n"
            "### Markdown to parse (minimum)\n"
            "- `# H1`, `## H2`, `### H3` — heading tags\n"
            "- `**bold**` — `<strong>`\n"
            "- `*italic*` — `<em>`\n"
            "- `` `code` `` — `<code>`\n"
            "- Paragraphs separated by blank lines"
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["JavaScript", "Regex", "DOM", "Parsing"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Process line-by-line: if line starts with #, convert to heading.", "Use regex replace for bold/italic/code within lines."],
        "concepts": ["String Parsing", "Regex", "Live Updates"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 200, "estimated_time_minutes": 35,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Markdown Preview</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"editor\">\n"
                    "    <div class=\"pane\">\n      <div class=\"pane-header\">Markdown</div>\n"
                    "      <textarea id=\"md-input\" placeholder=\"Type markdown here...\">## Hello World\n\n**Bold text** and *italic text*.\n\nInline `code` here.\n</textarea>\n    </div>\n"
                    "    <div class=\"pane\">\n      <div class=\"pane-header\">Preview</div>\n"
                    "      <div id=\"md-preview\"></div>\n    </div>\n  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0f0f11; color: #fafafa; height: 100vh; }\n"
                    ".editor { display: flex; height: 100vh; }\n"
                    ".pane { flex: 1; display: flex; flex-direction: column; border-right: 1px solid #27272a; }\n"
                    ".pane:last-child { border-right: none; }\n"
                    ".pane-header { padding: 12px 16px; font-size: 12px; font-weight: 600; color: #71717a; background: #18181b; border-bottom: 1px solid #27272a; text-transform: uppercase; letter-spacing: 1px; }\n"
                    "textarea { flex: 1; padding: 16px; background: #0f0f11; color: #e4e4e7; font-family: 'JetBrains Mono', monospace; font-size: 14px; border: none; resize: none; outline: none; }\n"
                    "#md-preview { flex: 1; padding: 16px; overflow-y: auto; line-height: 1.7; }\n"
                    "#md-preview h1 { font-size: 2rem; margin: 16px 0 8px; }\n"
                    "#md-preview h2 { font-size: 1.5rem; margin: 12px 0 6px; }\n"
                    "#md-preview h3 { font-size: 1.2rem; margin: 10px 0 4px; }\n"
                    "#md-preview p { margin-bottom: 12px; }\n"
                    "#md-preview code { background: #27272a; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 13px; }\n"
                    "#md-preview strong { font-weight: 700; }\n"
                ),
                "index.js": (
                    "function parseMarkdown(md) {\n"
                    "    // TODO: Convert markdown string to HTML string\n"
                    "    // Handle: # headings, **bold**, *italic*, `code`, paragraphs\n"
                    "    return md;\n"
                    "}\n\n"
                    "const input = document.getElementById('md-input');\n"
                    "const preview = document.getElementById('md-preview');\n\n"
                    "function update() {\n"
                    "    preview.innerHTML = parseMarkdown(input.value);\n"
                    "}\n\n"
                    "input.addEventListener('input', update);\n"
                    "update(); // initial render\n"
                )
            })
        },
        "test_cases": [
            {"id": "mp-1", "name": "editor panes present", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const inp = document.getElementById('md-input'); const prev = document.getElementById('md-preview'); return (inp && prev) ? 'PASS' : 'FAIL: missing elements';"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    {
        "title": "Color Palette Generator",
        "slug": "color-palette",
        "short_description": "Build a UI that generates random 5-color palettes with hex codes and copy support.",
        "description": (
            "### Color Palette Generator\n\n"
            "Build a color palette generator with:\n"
            "- A `#generate-btn` button to generate a new random 5-color palette\n"
            "- A `#palette` container displaying 5 color swatches\n"
            "- Each swatch shows the hex code and allows clicking to copy it\n"
            "- The palette should regenerate on each button click\n\n"
            "Each swatch should have class `color-swatch` and a `data-hex` attribute."
        ),
        "domain": "Frontend", "difficulty": "Easy",
        "tags": ["JavaScript", "CSS", "Colors", "DOM"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Generate hex: `'#' + Math.floor(Math.random()*0xFFFFFF).toString(16).padStart(6,'0')`", "Use `navigator.clipboard.writeText()` for copy."],
        "concepts": ["Color Theory", "DOM Manipulation", "Clipboard API"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 100, "estimated_time_minutes": 20,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Color Palette</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"app\">\n    <h1>Color Palette Generator</h1>\n"
                    "    <button id=\"generate-btn\">Generate Palette</button>\n"
                    "    <div id=\"palette\"></div>\n  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #09090b; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".app { text-align: center; }\n"
                    "h1 { font-size: 1.5rem; margin-bottom: 24px; }\n"
                    "#generate-btn { padding: 12px 28px; background: #7c3aed; color: #fff; border: none; border-radius: 10px; cursor: pointer; font-size: 15px; font-weight: 600; margin-bottom: 32px; }\n"
                    "#palette { display: flex; gap: 12px; justify-content: center; }\n"
                    ".color-swatch { width: 120px; height: 160px; border-radius: 12px; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; cursor: pointer; transition: transform 0.2s; }\n"
                    ".color-swatch:hover { transform: scale(1.05); }\n"
                    ".color-swatch .hex { font-size: 12px; font-weight: 700; background: rgba(0,0,0,0.4); padding: 4px 8px; border-radius: 6px; font-family: monospace; }\n"
                ),
                "index.js": (
                    "function randomHex() {\n"
                    "    // TODO: Return a random hex color string like '#a3f2b1'\n"
                    "    return '#000000';\n"
                    "}\n\n"
                    "function generatePalette() {\n"
                    "    const palette = document.getElementById('palette');\n"
                    "    palette.innerHTML = '';\n"
                    "    // TODO: Create 5 swatches with class 'color-swatch' and data-hex attribute\n"
                    "    // Each swatch background = its hex color, shows the hex code\n"
                    "    // Clicking a swatch copies its hex to clipboard\n"
                    "}\n\n"
                    "document.getElementById('generate-btn').addEventListener('click', generatePalette);\n"
                    "generatePalette();\n"
                )
            })
        },
        "test_cases": [
            {"id": "cp-1", "name": "generates 5 swatches", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const palette = document.getElementById('palette'); const swatches = palette ? palette.querySelectorAll('.color-swatch') : []; return swatches.length === 5 ? 'PASS' : 'FAIL: expected 5 swatches, got ' + swatches.length;"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    {
        "title": "Quiz App",
        "slug": "quiz-app",
        "short_description": "Build a multi-step quiz with progress tracking and a final score screen.",
        "description": (
            "### Quiz App\n\n"
            "Build a multiple-choice quiz with:\n"
            "- A question container (`#question`) showing the current question\n"
            "- 4 answer buttons (`#opt-0` through `#opt-3`) for the choices\n"
            "- A progress bar or text (`#progress`) showing `Question X / N`\n"
            "- On correct answer: highlight green; wrong: highlight red\n"
            "- After all questions, show a score screen (`#score-screen`) with `#final-score`\n\n"
            "Use at least 3 hardcoded questions."
        ),
        "domain": "Frontend", "difficulty": "Medium",
        "tags": ["JavaScript", "DOM", "UI Flow"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Store questions as an array of `{question, options, answer}` objects.", "Track `currentIndex` and `score` in state."],
        "concepts": ["State Management", "UI Flow", "Event Handling"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 200, "estimated_time_minutes": 35,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Quiz</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"app\">\n"
                    "    <div id=\"quiz-screen\">\n"
                    "      <div id=\"progress\">Question 1 / 3</div>\n"
                    "      <h2 id=\"question\">Loading question...</h2>\n"
                    "      <div id=\"options\">\n"
                    "        <button id=\"opt-0\"></button>\n        <button id=\"opt-1\"></button>\n"
                    "        <button id=\"opt-2\"></button>\n        <button id=\"opt-3\"></button>\n"
                    "      </div>\n    </div>\n"
                    "    <div id=\"score-screen\" style=\"display:none\">\n"
                    "      <h2>Quiz Complete!</h2>\n      <p>Your score: <span id=\"final-score\">0</span></p>\n"
                    "    </div>\n  </div>\n"
                    "  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0f0f11; color: #fff; min-height: 100vh; display: flex; align-items: center; justify-content: center; }\n"
                    ".app { width: 100%; max-width: 560px; padding: 32px; background: #18181b; border: 1px solid #27272a; border-radius: 16px; }\n"
                    "#progress { font-size: 13px; color: #71717a; margin-bottom: 16px; }\n"
                    "#question { font-size: 1.2rem; margin-bottom: 24px; line-height: 1.5; }\n"
                    "#options { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }\n"
                    "#options button { padding: 12px; background: #27272a; border: 1px solid #3f3f46; border-radius: 8px; color: #fff; cursor: pointer; font-size: 14px; transition: background 0.15s; }\n"
                    "#options button:hover { background: #3f3f46; }\n"
                    "#options button.correct { background: #16a34a; border-color: #16a34a; }\n"
                    "#options button.wrong { background: #dc2626; border-color: #dc2626; }\n"
                    "#score-screen { text-align: center; }\n"
                    "#score-screen h2 { font-size: 1.5rem; margin-bottom: 16px; }\n"
                    "#final-score { color: #22c55e; font-weight: 700; font-size: 1.2rem; }\n"
                ),
                "index.js": (
                    "const questions = [\n"
                    "    { question: 'What does HTTP stand for?', options: ['HyperText Transfer Protocol', 'High Transfer Text Protocol', 'HyperText Transport Process', 'Host Transfer Protocol'], answer: 0 },\n"
                    "    { question: 'Which data structure uses LIFO?', options: ['Queue', 'Stack', 'Tree', 'Graph'], answer: 1 },\n"
                    "    { question: 'What is Big O notation for?', options: ['Code style', 'Algorithm complexity', 'Memory allocation', 'Network speed'], answer: 1 },\n"
                    "];\n\n"
                    "let currentIndex = 0;\n"
                    "let score = 0;\n\n"
                    "// TODO: Implement loadQuestion(index) to display question and options\n"
                    "// TODO: Implement option click handler to check answer, update score, move to next\n"
                    "// TODO: When all questions answered, hide #quiz-screen and show #score-screen with #final-score\n\n"
                    "loadQuestion(0); // Start the quiz\n"
                )
            })
        },
        "test_cases": [
            {"id": "qa-1", "name": "quiz UI elements exist", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const ids = ['question','opt-0','opt-1','opt-2','opt-3','score-screen','final-score']; const missing = ids.filter(id => !document.getElementById(id)); return missing.length === 0 ? 'PASS' : 'FAIL: missing ' + missing.join(', ');"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    {
        "title": "Drag & Drop Kanban Board",
        "slug": "kanban-board",
        "short_description": "Build a 3-column Kanban board with drag-and-drop card movement.",
        "description": (
            "### Drag & Drop Kanban Board\n\n"
            "Build a Kanban board with 3 columns: **Todo**, **In Progress**, **Done** (IDs: `#col-todo`, `#col-progress`, `#col-done`).\n\n"
            "Features:\n"
            "- Each column has a card list and an 'Add card' input+button\n"
            "- Cards are draggable between columns using the HTML5 Drag & Drop API\n"
            "- Cards have class `kanban-card` and a unique `data-id` attribute\n"
            "- Column headers show the count of cards in that column"
        ),
        "domain": "Frontend", "difficulty": "Hard",
        "tags": ["JavaScript", "Drag & Drop", "CSS Grid", "UX"],
        "technologies": ["html", "css", "javascript"],
        "hints": ["Use `draggable='true'` on cards and listen to `dragstart`, `dragover`, `drop`.", "On `drop`, use `e.preventDefault()` then `appendChild` the dragged card."],
        "concepts": ["Drag & Drop API", "DOM Manipulation", "State Management"],
        "runtime": "frontend", "execution_mode": "browser",
        "xp_reward": 350, "estimated_time_minutes": 50,
        "starter_code": {
            "html": json.dumps({
                "index.html": (
                    "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <title>Kanban</title>\n"
                    "  <link rel=\"stylesheet\" href=\"index.css\">\n</head>\n<body>\n"
                    "  <div class=\"board\">\n"
                    "    <div class=\"column\" id=\"col-todo\">\n      <div class=\"col-header\">Todo <span class=\"count\">0</span></div>\n      <div class=\"cards\"></div>\n      <div class=\"add-card\"><input placeholder=\"New card...\"><button>Add</button></div>\n    </div>\n"
                    "    <div class=\"column\" id=\"col-progress\">\n      <div class=\"col-header\">In Progress <span class=\"count\">0</span></div>\n      <div class=\"cards\"></div>\n      <div class=\"add-card\"><input placeholder=\"New card...\"><button>Add</button></div>\n    </div>\n"
                    "    <div class=\"column\" id=\"col-done\">\n      <div class=\"col-header\">Done <span class=\"count\">0</span></div>\n      <div class=\"cards\"></div>\n      <div class=\"add-card\"><input placeholder=\"New card...\"><button>Add</button></div>\n    </div>\n"
                    "  </div>\n  <script src=\"index.js\"></script>\n</body>\n</html>"
                ),
                "index.css": (
                    "* { box-sizing: border-box; margin: 0; padding: 0; }\n"
                    "body { font-family: system-ui, sans-serif; background: #0a0a0b; color: #fff; min-height: 100vh; padding: 24px; }\n"
                    ".board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; height: calc(100vh - 48px); }\n"
                    ".column { background: #18181b; border: 1px solid #27272a; border-radius: 12px; display: flex; flex-direction: column; padding: 16px; gap: 12px; }\n"
                    ".col-header { font-weight: 700; font-size: 14px; display: flex; justify-content: space-between; align-items: center; }\n"
                    ".count { background: #27272a; border-radius: 999px; padding: 2px 8px; font-size: 12px; }\n"
                    ".cards { flex: 1; display: flex; flex-direction: column; gap: 8px; min-height: 40px; }\n"
                    ".kanban-card { background: #27272a; border: 1px solid #3f3f46; border-radius: 8px; padding: 10px 12px; font-size: 14px; cursor: grab; user-select: none; }\n"
                    ".kanban-card.dragging { opacity: 0.5; }\n"
                    ".column.drag-over .cards { border: 2px dashed #2563eb; border-radius: 8px; }\n"
                    ".add-card { display: flex; gap: 8px; }\n"
                    ".add-card input { flex: 1; padding: 6px 10px; background: #27272a; border: 1px solid #3f3f46; border-radius: 6px; color: #fff; font-size: 13px; }\n"
                    ".add-card button { padding: 6px 12px; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; }\n"
                ),
                "index.js": (
                    "let draggedCard = null;\n"
                    "let cardCounter = 0;\n\n"
                    "function createCard(text, columnId) {\n"
                    "    // TODO: Create a div.kanban-card with data-id, draggable='true'\n"
                    "    // Set up dragstart, dragend event listeners\n"
                    "    // Append to column's .cards container\n"
                    "    // Update column count\n"
                    "}\n\n"
                    "function setupColumn(column) {\n"
                    "    const cards = column.querySelector('.cards');\n"
                    "    const btn = column.querySelector('.add-card button');\n"
                    "    const inp = column.querySelector('.add-card input');\n"
                    "    // TODO: dragover -> e.preventDefault(); drop -> append draggedCard\n"
                    "    btn.addEventListener('click', () => {\n"
                    "        if (inp.value.trim()) { createCard(inp.value.trim(), column.id); inp.value = ''; }\n"
                    "    });\n"
                    "}\n\n"
                    "document.querySelectorAll('.column').forEach(setupColumn);\n\n"
                    "// Add some starter cards\n"
                    "createCard('Design system setup', 'col-todo');\n"
                    "createCard('API integration', 'col-progress');\n"
                    "createCard('Authentication flow', 'col-done');\n"
                )
            })
        },
        "test_cases": [
            {"id": "kb-1", "name": "three columns present", "hidden": False, "weight": 1,
             "stdin": json.dumps({"evaluation": "const cols = ['col-todo','col-progress','col-done']; const missing = cols.filter(id => !document.getElementById(id)); const cards = document.querySelectorAll('.kanban-card'); return missing.length === 0 && cards.length >= 3 ? 'PASS' : 'FAIL';"}),
             "expected_output": "PASS\n", "comparison_mode": "exact"},
        ],
    },

    # ═══════════════════════ APIs — (10) ═════════════════════════════════════

    {
        "title": "Notes CRUD API",
        "slug": "notes-api",
        "short_description": "Build a RESTful Notes API with create, list, update, and delete endpoints.",
        "description": (
            "### Notes API\n\n"
            "Build a REST API for a note-taking service:\n"
            "- `POST /notes` — create a note `{title, content}`, return `{id, title, content, createdAt}`\n"
            "- `GET /notes` — list all notes\n"
            "- `GET /notes/:id` — get a single note\n"
            "- `PUT /notes/:id` — update title/content\n"
            "- `DELETE /notes/:id` — delete, return `{deleted: true}`\n"
            "- `GET /health` — return `{status: 'ok'}`"
        ),
        "domain": "APIs", "difficulty": "Medium",
        "tags": ["REST", "CRUD", "Express.js", "MongoDB"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["RESTful Design", "CRUD Operations", "HTTP Methods"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 300, "estimated_time_minutes": 45,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\n"
                    "const { MongoClient, ObjectId } = require('mongodb');\n"
                    "const app = express();\n"
                    "app.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\n"
                    "let notes;\n"
                    "client.connect().then(() => { notes = client.db('notes_db').collection('notes'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /notes - create note\n"
                    "// TODO: GET /notes  - list all notes\n"
                    "// TODO: GET /notes/:id - get note by id\n"
                    "// TODO: PUT /notes/:id - update note\n"
                    "// TODO: DELETE /notes/:id - delete note\n\n"
                    "const PORT = process.env.PORT || 3000;\n"
                    "app.listen(PORT, () => console.log('Server running on port ' + PORT));\n"
                )
            }),
            "py_mongodb": json.dumps({
                "solution.py": (
                    "from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\nfrom pymongo import MongoClient\nfrom bson import ObjectId\nfrom datetime import datetime\nimport os\n\n"
                    "app = FastAPI()\nclient = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))\nnotes = client['notes_db']['notes']\n\n"
                    "@app.get('/health')\ndef health(): return {'status': 'ok'}\n\n"
                    "class NoteCreate(BaseModel):\n    title: str\n    content: str | None = None\n\n"
                    "# TODO: POST /notes, GET /notes, GET /notes/{note_id}, PUT /notes/{note_id}, DELETE /notes/{note_id}\n\n"
                    "if __name__ == '__main__':\n    import uvicorn\n    port = int(os.environ.get('PORT', 3000))\n    uvicorn.run(app, host='127.0.0.1', port=port)\n"
                )
            })
        },
        "test_cases": [
            {"id": "na-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "URL Shortener API",
        "slug": "url-shortener-api",
        "short_description": "Build a URL shortener API that encodes long URLs to short slugs and resolves them.",
        "description": (
            "### URL Shortener API\n\n"
            "Build a URL shortener service:\n"
            "- `POST /shorten` — accept `{url}`, return `{slug, shortUrl, originalUrl}`\n"
            "- `GET /resolve/:slug` — return `{originalUrl}` or `404`\n"
            "- `GET /stats/:slug` — return `{slug, visits, originalUrl}`\n"
            "- `GET /health` — return `{status: 'ok'}`\n\n"
            "Slugs should be 6 random alphanumeric characters."
        ),
        "domain": "APIs", "difficulty": "Medium",
        "tags": ["REST", "MongoDB", "URL Encoding", "Hash"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["URL Shortening", "Slug Generation", "Analytics"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 300, "estimated_time_minutes": 40,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet urls;\nclient.connect().then(() => { urls = client.db('shortener_db').collection('urls'); });\n\n"
                    "function generateSlug() {\n    return Math.random().toString(36).substring(2, 8);\n}\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /shorten - generate slug and store mapping\n"
                    "// TODO: GET /resolve/:slug - look up slug, increment visits, return originalUrl\n"
                    "// TODO: GET /stats/:slug - return {slug, visits, originalUrl}\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server running on port ' + PORT));\n"
                )
            }),
            "py_mongodb": json.dumps({
                "solution.py": (
                    "from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\nfrom pymongo import MongoClient\nimport os, random, string\n\n"
                    "app = FastAPI()\nclient = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))\nurls = client['shortener_db']['urls']\n\n"
                    "def generate_slug(): return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))\n\n"
                    "@app.get('/health')\ndef health(): return {'status': 'ok'}\n\n"
                    "class ShortenRequest(BaseModel):\n    url: str\n\n"
                    "# TODO: POST /shorten, GET /resolve/{slug}, GET /stats/{slug}\n\n"
                    "if __name__ == '__main__':\n    import uvicorn\n    port = int(os.environ.get('PORT', 3000))\n    uvicorn.run(app, host='127.0.0.1', port=port)\n"
                )
            })
        },
        "test_cases": [
            {"id": "us-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Blog Posts API",
        "slug": "blog-posts-api",
        "short_description": "Create a blog API with posts and comments supporting full CRUD operations.",
        "description": (
            "### Blog Posts API\n\n"
            "Build a blog REST API:\n"
            "- `POST /posts` — create `{title, content, author}`, return created post\n"
            "- `GET /posts` — list all posts (title, author, createdAt, commentCount)\n"
            "- `GET /posts/:id` — get post with its comments\n"
            "- `POST /posts/:id/comments` — add `{text, author}` comment\n"
            "- `DELETE /posts/:id` — delete post and its comments\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "APIs", "difficulty": "Hard",
        "tags": ["REST", "MongoDB", "Nested Resources", "Blog"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Nested Resources", "Aggregation", "RESTful Design"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient, ObjectId } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet posts, comments;\nclient.connect().then(() => {\n    const db = client.db('blog_db');\n    posts = db.collection('posts');\n    comments = db.collection('comments');\n});\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /posts\n// TODO: GET /posts\n// TODO: GET /posts/:id (include comments)\n// TODO: POST /posts/:id/comments\n// TODO: DELETE /posts/:id\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "bp-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Inventory Manager API",
        "slug": "inventory-api",
        "short_description": "Build a product inventory API with stock management and low-stock alerts.",
        "description": (
            "### Inventory Manager API\n\n"
            "Build an inventory management REST API:\n"
            "- `POST /products` — create `{name, sku, stock, price}`, return created product\n"
            "- `GET /products` — list all products\n"
            "- `GET /products/low-stock?threshold=5` — products with stock ≤ threshold\n"
            "- `PATCH /products/:id/stock` — update stock `{delta}` (positive = restock, negative = sold)\n"
            "- `DELETE /products/:id` — remove product\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "APIs", "difficulty": "Medium",
        "tags": ["REST", "MongoDB", "Inventory", "Business Logic"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Inventory Management", "Partial Updates", "Query Params"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 300, "estimated_time_minutes": 45,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient, ObjectId } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet products;\nclient.connect().then(() => { products = client.db('inventory_db').collection('products'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /products\n// TODO: GET /products\n// TODO: GET /products/low-stock\n// TODO: PATCH /products/:id/stock\n// TODO: DELETE /products/:id\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "ia-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "JWT Auth API",
        "slug": "auth-jwt-api",
        "short_description": "Build a register/login authentication API issuing JWT tokens.",
        "description": (
            "### JWT Authentication API\n\n"
            "Build a JWT-based auth system:\n"
            "- `POST /auth/register` — create user `{username, password}`, return `{token, userId}`\n"
            "- `POST /auth/login` — verify credentials, return `{token, userId}` or `401`\n"
            "- `GET /auth/me` — protected route; return user info from `Authorization: Bearer <token>`\n"
            "- `GET /health` — `{status: 'ok'}`\n\n"
            "Use `jsonwebtoken` (Node) or `python-jose` (Python) for JWT signing."
        ),
        "domain": "APIs", "difficulty": "Hard",
        "tags": ["REST", "JWT", "Auth", "Security", "MongoDB"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["JWT", "Authentication", "Password Hashing", "Middleware"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient } = require('mongodb');\nconst jwt = require('jsonwebtoken');\nconst crypto = require('crypto');\nconst app = express();\napp.use(express.json());\n\n"
                    "const SECRET = process.env.JWT_SECRET || 'interleet-secret';\nconst client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet users;\nclient.connect().then(() => { users = client.db('auth_db').collection('users'); });\n\n"
                    "const hash = (pwd) => crypto.createHash('sha256').update(pwd).digest('hex');\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /auth/register - hash password, insert user, return token\n"
                    "// TODO: POST /auth/login   - verify hash, return token or 401\n"
                    "// TODO: GET  /auth/me      - verify Bearer token, return user\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "auth-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Rate Limited API",
        "slug": "rate-limited-api",
        "short_description": "Implement an API with a sliding-window rate limiter rejecting excess requests.",
        "description": (
            "### Rate Limited API\n\n"
            "Build an API with a rate limiter middleware:\n"
            "- Limit: max **5 requests per 10 seconds** per IP\n"
            "- `GET /ping` — return `{message: 'pong', remaining: N}` where N = requests remaining\n"
            "- Rejected requests return `429 Too Many Requests` with `{error: 'Rate limit exceeded', retryAfter: N}`\n"
            "- `GET /health` — `{status: 'ok'}`\n\n"
            "Use an in-memory store (no DB needed)."
        ),
        "domain": "APIs", "difficulty": "Medium",
        "tags": ["Rate Limiting", "Middleware", "REST", "Security"],
        "technologies": ["javascript", "python"],
        "concepts": ["Rate Limiting", "Sliding Window", "Middleware Pattern"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 300, "estimated_time_minutes": 40,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst app = express();\napp.use(express.json());\n\n"
                    "const LIMIT = 5;\nconst WINDOW_MS = 10000;\nconst store = {}; // { ip: [{timestamp}] }\n\n"
                    "function rateLimiter(req, res, next) {\n"
                    "    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '127.0.0.1';\n"
                    "    const now = Date.now();\n"
                    "    // TODO: Filter old requests, count recent ones, block if over limit\n"
                    "    next();\n"
                    "}\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n"
                    "app.get('/ping', rateLimiter, (req, res) => {\n"
                    "    res.json({ message: 'pong', remaining: LIMIT });\n"
                    "});\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "rl-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Bookmarks API",
        "slug": "bookmarks-api",
        "short_description": "Build a bookmark manager API with tagging and search support.",
        "description": (
            "### Bookmarks API\n\n"
            "Build a bookmark management service:\n"
            "- `POST /bookmarks` — create `{title, url, tags[]}`, return created bookmark\n"
            "- `GET /bookmarks` — list all bookmarks (supports `?tag=foo` filter)\n"
            "- `GET /bookmarks/:id` — get single bookmark\n"
            "- `DELETE /bookmarks/:id` — remove bookmark\n"
            "- `GET /bookmarks/tags` — list all unique tags\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "APIs", "difficulty": "Medium",
        "tags": ["REST", "MongoDB", "Tagging", "Search"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Tagging System", "Query Filtering", "RESTful Design"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 250, "estimated_time_minutes": 40,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient, ObjectId } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet bookmarks;\nclient.connect().then(() => { bookmarks = client.db('bookmarks_db').collection('bookmarks'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /bookmarks\n// TODO: GET /bookmarks (with optional ?tag= filter)\n// TODO: GET /bookmarks/tags (all unique tags)\n// TODO: GET /bookmarks/:id\n// TODO: DELETE /bookmarks/:id\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "bm-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Polling Queue API",
        "slug": "polling-queue-api",
        "short_description": "Build a job queue API supporting enqueue, dequeue, and status polling.",
        "description": (
            "### Polling Queue API\n\n"
            "Build an in-memory job queue system:\n"
            "- `POST /jobs` — enqueue `{type, payload}`, return `{jobId, status: 'queued'}`\n"
            "- `GET /jobs/:id` — return job status `{jobId, status, result}` (status: queued/processing/done/failed)\n"
            "- `POST /jobs/process` — dequeue the oldest job, simulate processing, set status to `done`\n"
            "- `GET /jobs` — list all jobs with their statuses\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "APIs", "difficulty": "Hard",
        "tags": ["Queue", "Job Processing", "REST", "Async Patterns"],
        "technologies": ["javascript", "python"],
        "concepts": ["Message Queue", "Job Scheduling", "State Machine"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 55,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst app = express();\napp.use(express.json());\n\n"
                    "const jobs = {};\nconst queue = [];\nlet jobCounter = 0;\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /jobs - enqueue job, add to queue[], return {jobId, status: 'queued'}\n"
                    "// TODO: GET /jobs/:id - return job status\n"
                    "// TODO: POST /jobs/process - shift from queue, set status 'done', return job\n"
                    "// TODO: GET /jobs - list all jobs\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "pq-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Comments Thread API",
        "slug": "comments-thread-api",
        "short_description": "Build a nested-comments API supporting threaded replies and voting.",
        "description": (
            "### Comments Thread API\n\n"
            "Build a nested comments system:\n"
            "- `POST /comments` — create `{text, author, parentId?}`, return new comment\n"
            "- `GET /comments` — list root comments (no parentId), sorted by votes desc\n"
            "- `GET /comments/:id/replies` — list direct replies to a comment\n"
            "- `POST /comments/:id/vote` — accept `{type: 'up'|'down'}`, increment vote count\n"
            "- `DELETE /comments/:id` — soft-delete (mark deleted: true, preserve thread)\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "Fullstack", "difficulty": "Hard",
        "tags": ["REST", "MongoDB", "Nested Data", "Voting"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Nested Comments", "Tree Structure", "Voting System"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient, ObjectId } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet comments;\nclient.connect().then(() => { comments = client.db('comments_db').collection('comments'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /comments\n// TODO: GET /comments (root-level, sorted by votes)\n// TODO: GET /comments/:id/replies\n// TODO: POST /comments/:id/vote\n// TODO: DELETE /comments/:id (soft-delete)\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "ct-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Analytics Event Tracker API",
        "slug": "analytics-tracker-api",
        "short_description": "Build an analytics API that ingests events and returns aggregated metrics.",
        "description": (
            "### Analytics Event Tracker\n\n"
            "Build a lightweight analytics backend:\n"
            "- `POST /events` — ingest `{event, userId, properties{}, timestamp?}`, return `{recorded: true}`\n"
            "- `GET /metrics/:event` — return `{event, count, uniqueUsers, firstSeen, lastSeen}`\n"
            "- `GET /events/user/:userId` — return all events for a specific user\n"
            "- `GET /events/summary` — return top 5 events by count\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "Fullstack", "difficulty": "Hard",
        "tags": ["REST", "Analytics", "MongoDB", "Aggregation"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Event Sourcing", "Aggregation", "Time Series"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet events;\nclient.connect().then(() => { events = client.db('analytics_db').collection('events'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /events\n// TODO: GET /metrics/:event (aggregated stats)\n// TODO: GET /events/user/:userId\n// TODO: GET /events/summary (top 5 events)\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "at-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    # ═══════════════════════ DATABASES — (7) ═════════════════════════════════

    {
        "title": "SQL JOIN Query Builder",
        "slug": "sql-join-builder",
        "short_description": "Identify the correct JOIN type and produce the output given table data and a query.",
        "description": (
            "### SQL JOIN Simulation\n\n"
            "Given two tables and a JOIN type, produce the result set as a JSON array.\n\n"
            "**Input:**\n```json\n{\"type\": \"INNER\", \"left\": [{\"id\":1,\"name\":\"Alice\"},{\"id\":2,\"name\":\"Bob\"},{\"id\":3,\"name\":\"Carol\"}], \"right\": [{\"userId\":1,\"dept\":\"Eng\"},{\"userId\":2,\"dept\":\"Sales\"},{\"userId\":4,\"dept\":\"HR\"}], \"on\": [\"id\", \"userId\"]}\n```\n\n"
            "**Output:** Rows where `left.id == right.userId` (INNER JOIN only matches)."
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["SQL", "Joins", "Data Processing"],
        "technologies": ["javascript", "python"],
        "hints": ["INNER JOIN: only matching rows from both sides.", "LEFT JOIN: all left rows, NULL fill for unmatched right rows."],
        "concepts": ["SQL Joins", "Set Operations", "Relational Algebra"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function join(type, left, right, on) {\n"
                "    const [lKey, rKey] = on;\n"
                "    if (type === 'INNER') {\n"
                "        // TODO: Return rows where left[lKey] === right[rKey], merge objects\n"
                "        return [];\n"
                "    }\n"
                "    if (type === 'LEFT') {\n"
                "        // TODO: All left rows, null fill from right if no match\n"
                "        return [];\n"
                "    }\n"
                "    return [];\n"
                "}\n\n"
                "const { type, left, right, on } = input;\n"
                "console.log(JSON.stringify(join(type, left, right, on)));\n"
            ),
            "python": py_cli(
                "def join_tables(join_type, left, right, on):\n"
                "    l_key, r_key = on\n"
                "    right_map = {r[r_key]: r for r in right}\n"
                "    if join_type == 'INNER':\n"
                "        # TODO: Return merged rows for matching keys only\n"
                "        return []\n"
                "    if join_type == 'LEFT':\n"
                "        # TODO: All left rows + merged right (None if no match)\n"
                "        return []\n"
                "    return []\n\n"
                "result = join_tables(data['type'], data['left'], data['right'], data['on'])\n"
                "print(json.dumps(result))\n"
            ),
        },
        "test_cases": [
            {"id": "jb-1", "name": "INNER JOIN", "hidden": False, "weight": 1,
             "stdin": json.dumps({"type": "INNER", "left": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}, {"id": 3, "name": "Carol"}], "right": [{"userId": 1, "dept": "Eng"}, {"userId": 2, "dept": "Sales"}, {"userId": 4, "dept": "HR"}], "on": ["id", "userId"]}),
             "expected_output": json.dumps([{"id": 1, "name": "Alice", "userId": 1, "dept": "Eng"}, {"id": 2, "name": "Bob", "userId": 2, "dept": "Sales"}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Aggregation Pipeline",
        "slug": "aggregation-pipeline",
        "short_description": "Implement a MongoDB-style aggregation pipeline with match, group, and sort.",
        "description": (
            "### Aggregation Pipeline\n\n"
            "Implement a simple aggregation engine that processes an array of documents through a pipeline of stages:\n\n"
            "- `$match: {field: value}` — filter documents\n"
            "- `$group: {_id: field, total: {$sum: field2}, count: {$sum: 1}}` — group and aggregate\n"
            "- `$sort: {field: 1 or -1}` — sort results\n\n"
            "### Input (stdin)\n```json\n{\"docs\": [...], \"pipeline\": [{\"$match\":{...}},{\"$group\":{...}},{\"$sort\":{...}}]}\n```"
        ),
        "domain": "Databases", "difficulty": "Hard",
        "tags": ["Databases", "Aggregation", "MongoDB", "Functional"],
        "technologies": ["javascript", "python"],
        "hints": ["Process stages sequentially.", "For $group, build a map keyed by _id value."],
        "concepts": ["MongoDB Aggregation", "Data Pipeline", "Functional Programming"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 350, "estimated_time_minutes": 45,
        "starter_code": {
            "javascript": js_cli(
                "function aggregate(docs, pipeline) {\n"
                "    let result = [...docs];\n"
                "    for (const stage of pipeline) {\n"
                "        if (stage['$match']) {\n"
                "            // TODO: Filter docs by match criteria\n"
                "        } else if (stage['$group']) {\n"
                "            // TODO: Group docs and aggregate\n"
                "        } else if (stage['$sort']) {\n"
                "            // TODO: Sort by specified field\n"
                "        }\n"
                "    }\n"
                "    return result;\n"
                "}\n\n"
                "console.log(JSON.stringify(aggregate(input.docs, input.pipeline)));\n"
            ),
            "python": py_cli(
                "def aggregate(docs, pipeline):\n"
                "    result = list(docs)\n"
                "    for stage in pipeline:\n"
                "        if '$match' in stage:\n"
                "            # TODO: Filter docs by match criteria\n"
                "            pass\n"
                "        elif '$group' in stage:\n"
                "            # TODO: Group docs and aggregate\n"
                "            pass\n"
                "        elif '$sort' in stage:\n"
                "            # TODO: Sort by specified field\n"
                "            pass\n"
                "    return result\n\n"
                "print(json.dumps(aggregate(data['docs'], data['pipeline'])))\n"
            ),
        },
        "test_cases": [
            {"id": "ap-1", "name": "match and group", "hidden": False, "weight": 1,
             "stdin": json.dumps({"docs": [{"dept": "Eng", "salary": 100}, {"dept": "Eng", "salary": 120}, {"dept": "HR", "salary": 80}], "pipeline": [{"$match": {"dept": "Eng"}}, {"$group": {"_id": "dept", "total": {"$sum": "salary"}, "count": {"$sum": 1}}}]}),
             "expected_output": json.dumps([{"_id": "Eng", "total": 220, "count": 2}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Schema Migration Simulator",
        "slug": "schema-migration",
        "short_description": "Write a migration script that transforms a v1 schema into a v2 schema.",
        "description": (
            "### Schema Migration Simulator\n\n"
            "Given an array of `v1` documents, migrate them to the `v2` schema by applying transformation rules.\n\n"
            "**Migration rules:**\n"
            "- `full_name` → split into `first_name` + `last_name`\n"
            "- `created` (Unix timestamp) → `created_at` (ISO 8601 string)\n"
            "- Remove the `legacy_id` field\n"
            "- Add `version: 2`\n\n"
            "### Input (stdin)\n```json\n[{\"full_name\": \"Alice Smith\", \"created\": 1700000000, \"legacy_id\": \"L001\", \"email\": \"a@b.com\"}]\n```"
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["Databases", "Migration", "Data Transform"],
        "technologies": ["javascript", "python"],
        "hints": ["Split name on the first space.", "Use `new Date(timestamp * 1000).toISOString()` in JS."],
        "concepts": ["Schema Migration", "Data Transformation", "ETL"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 25,
        "starter_code": {
            "javascript": js_cli(
                "function migrate(docs) {\n"
                "    return docs.map(doc => {\n"
                "        // TODO: Transform each doc from v1 to v2 schema\n"
                "        // - split full_name into first_name + last_name\n"
                "        // - convert created to created_at (ISO string)\n"
                "        // - remove legacy_id\n"
                "        // - add version: 2\n"
                "        return doc;\n"
                "    });\n"
                "}\n\n"
                "console.log(JSON.stringify(migrate(input)));\n"
            ),
            "python": py_cli(
                "from datetime import datetime, timezone\n\n"
                "def migrate(docs):\n"
                "    result = []\n"
                "    for doc in docs:\n"
                "        # TODO: Transform each doc from v1 to v2 schema\n"
                "        result.append(doc)\n"
                "    return result\n\n"
                "print(json.dumps(migrate(data)))\n"
            ),
        },
        "test_cases": [
            {"id": "sm-1", "name": "migrate single doc", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"full_name": "Alice Smith", "created": 1700000000, "legacy_id": "L001", "email": "a@b.com"}]),
             "expected_output": json.dumps([{"first_name": "Alice", "last_name": "Smith", "created_at": "2023-11-14T22:13:20+00:00", "email": "a@b.com", "version": 2}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Index Advisor",
        "slug": "index-advisor",
        "short_description": "Analyze query patterns and recommend optimal database indexes.",
        "description": (
            "### Index Advisor\n\n"
            "Given a list of query patterns (fields used in WHERE/filter clauses), recommend which indexes to create based on frequency and selectivity.\n\n"
            "**Rules:**\n"
            "- Fields appearing in 3+ queries → create a single-field index\n"
            "- Two fields always queried together → create a compound index\n"
            "- Return indexes sorted by estimated impact (frequency)\n\n"
            "### Input (stdin)\n```json\n{\"queries\": [[\"userId\"],[\"userId\",\"status\"],[\"userId\"],[\"userId\",\"status\"],[\"email\"]]}\n```"
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["Databases", "Performance", "Indexing", "Query Optimization"],
        "technologies": ["javascript", "python"],
        "hints": ["Count individual field frequency.", "Track pairs of fields that appear together."],
        "concepts": ["Database Indexing", "Query Optimization", "Performance"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function advisedIndexes(queries) {\n"
                "    // TODO: Return [{type, fields, frequency}] sorted by frequency desc\n"
                "    // type: 'single' or 'compound'\n"
                "    return [];\n"
                "}\n\n"
                "console.log(JSON.stringify(advisedIndexes(input.queries)));\n"
            ),
            "python": py_cli(
                "from collections import Counter\n\n"
                "def advised_indexes(queries):\n"
                "    # TODO: Return [{'type', 'fields', 'frequency'}] sorted by frequency desc\n"
                "    return []\n\n"
                "print(json.dumps(advised_indexes(data['queries'])))\n"
            ),
        },
        "test_cases": [
            {"id": "idx-1", "name": "recommend compound index", "hidden": False, "weight": 1,
             "stdin": json.dumps({"queries": [["userId"], ["userId", "status"], ["userId"], ["userId", "status"], ["email"]]}),
             "expected_output": json.dumps([{"type": "compound", "fields": ["userId", "status"], "frequency": 2}, {"type": "single", "fields": ["userId"], "frequency": 4}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Query Cost Estimator",
        "slug": "query-cost-estimator",
        "short_description": "Estimate the relative cost of SQL operations given table statistics.",
        "description": (
            "### Query Cost Estimator\n\n"
            "Given a simplified SQL-like query and table statistics, estimate the query cost.\n\n"
            "**Cost model:**\n"
            "- Full table scan: cost = `rowCount`\n"
            "- Index lookup: cost = `log2(rowCount)`\n"
            "- JOIN cost: cost = `left.rowCount * right.rowCount` (nested loop), or `left + right` (hash join)\n\n"
            "### Input\n```json\n{\"operation\": \"scan\", \"table\": {\"name\": \"users\", \"rowCount\": 1000, \"hasIndex\": false}}\n```\n\n"
            "### Output\n```json\n{\"cost\": 1000, \"type\": \"full_scan\"}\n```"
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["Databases", "Query Planning", "Performance", "Estimation"],
        "technologies": ["javascript", "python"],
        "hints": ["Check `hasIndex` to decide between scan and lookup.", "Use `Math.log2(n)` for index cost."],
        "concepts": ["Query Planning", "Cost-Based Optimization", "Database Internals"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 250, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function estimateCost(operation, table) {\n"
                "    const n = table.rowCount;\n"
                "    // TODO: Return {cost, type} based on operation and index availability\n"
                "    // operation: 'scan' | 'lookup'\n"
                "    // type: 'full_scan' | 'index_scan'\n"
                "    return { cost: 0, type: 'unknown' };\n"
                "}\n\n"
                "const result = estimateCost(input.operation, input.table);\n"
                "console.log(JSON.stringify(result));\n"
            ),
            "python": py_cli(
                "import math\n\n"
                "def estimate_cost(operation, table):\n"
                "    n = table['rowCount']\n"
                "    # TODO: Return {'cost': ..., 'type': 'full_scan'|'index_scan'}\n"
                "    return {'cost': 0, 'type': 'unknown'}\n\n"
                "result = estimate_cost(data['operation'], data['table'])\n"
                "print(json.dumps(result))\n"
            ),
        },
        "test_cases": [
            {"id": "qce-1", "name": "full scan cost", "hidden": False, "weight": 1,
             "stdin": json.dumps({"operation": "scan", "table": {"name": "users", "rowCount": 1000, "hasIndex": False}}),
             "expected_output": json.dumps({"cost": 1000, "type": "full_scan"}) + "\n",
             "comparison_mode": "json"},
            {"id": "qce-2", "name": "index scan cost", "hidden": True, "weight": 1,
             "stdin": json.dumps({"operation": "lookup", "table": {"name": "users", "rowCount": 1024, "hasIndex": True}}),
             "expected_output": json.dumps({"cost": 10, "type": "index_scan"}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "N+1 Query Detector",
        "slug": "n-plus-one-detector",
        "short_description": "Detect and fix N+1 query patterns by rewriting queries to use batch loading.",
        "description": (
            "### N+1 Query Detector\n\n"
            "Given a sequence of database queries, detect if there is an N+1 pattern (1 query that fetches N IDs, followed by N individual queries).\n\n"
            "**Input:**\n```json\n{\"queries\": [{\"type\": \"find\", \"collection\": \"posts\"}, {\"type\": \"findById\", \"collection\": \"users\", \"id\": 1}, {\"type\": \"findById\", \"collection\": \"users\", \"id\": 2}, {\"type\": \"findById\", \"collection\": \"users\", \"id\": 3}]}\n```\n\n"
            "**Output:**\n```json\n{\"hasNPlusOne\": true, \"offendingCollection\": \"users\", \"individualQueries\": 3, \"suggestion\": \"Use find({_id: {$in: [1,2,3]}}) instead\"}\n```"
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["Databases", "Performance", "Query Optimization", "ORM"],
        "technologies": ["javascript", "python"],
        "hints": ["Count consecutive `findById` calls on the same collection.", "If count >= 3 consecutive individual lookups, flag as N+1."],
        "concepts": ["N+1 Problem", "Batch Loading", "Performance Patterns"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 25,
        "starter_code": {
            "javascript": js_cli(
                "function detectNPlusOne(queries) {\n"
                "    // TODO: Detect if sequential findById calls on same collection appear 3+ times\n"
                "    // Return {hasNPlusOne, offendingCollection, individualQueries, suggestion}\n"
                "    return { hasNPlusOne: false, offendingCollection: null, individualQueries: 0, suggestion: null };\n"
                "}\n\n"
                "console.log(JSON.stringify(detectNPlusOne(input.queries)));\n"
            ),
            "python": py_cli(
                "def detect_n_plus_one(queries):\n"
                "    # TODO: Detect N+1 pattern — consecutive findById on same collection\n"
                "    return {'hasNPlusOne': False, 'offendingCollection': None, 'individualQueries': 0, 'suggestion': None}\n\n"
                "print(json.dumps(detect_n_plus_one(data['queries'])))\n"
            ),
        },
        "test_cases": [
            {"id": "np1-1", "name": "detect N+1 pattern", "hidden": False, "weight": 1,
             "stdin": json.dumps({"queries": [{"type": "find", "collection": "posts"}, {"type": "findById", "collection": "users", "id": 1}, {"type": "findById", "collection": "users", "id": 2}, {"type": "findById", "collection": "users", "id": 3}]}),
             "expected_output": json.dumps({"hasNPlusOne": True, "offendingCollection": "users", "individualQueries": 3, "suggestion": "Use find({_id: {$in: [1,2,3]}}) instead"}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Query Result Paginator",
        "slug": "query-paginator",
        "short_description": "Implement cursor-based and offset-based pagination for a list of records.",
        "description": (
            "### Query Result Paginator\n\n"
            "Implement two pagination strategies:\n\n"
            "**Offset-based:** Given `{records, page, perPage}` return the slice plus metadata.\n\n"
            "**Cursor-based:** Given `{records, cursor, limit}` where cursor is a record's `id`, return records after that ID.\n\n"
            "### Input (stdin)\n```json\n{\"strategy\": \"offset\", \"records\": [...], \"page\": 2, \"perPage\": 3}\n```\n\n"
            "### Output\n```json\n{\"data\": [...], \"total\": 9, \"page\": 2, \"totalPages\": 3, \"hasNext\": false}\n```"
        ),
        "domain": "Databases", "difficulty": "Medium",
        "tags": ["Databases", "Pagination", "Performance", "API Design"],
        "technologies": ["javascript", "python"],
        "hints": ["Offset: `data = records.slice((page-1)*perPage, page*perPage)`", "Cursor: find the cursor record's index, return the next `limit` records."],
        "concepts": ["Pagination", "Cursor-based vs Offset", "API Design"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 150, "estimated_time_minutes": 25,
        "starter_code": {
            "javascript": js_cli(
                "function paginate(strategy, records, opts) {\n"
                "    if (strategy === 'offset') {\n"
                "        const { page, perPage } = opts;\n"
                "        // TODO: Return {data, total, page, totalPages, hasNext}\n"
                "        return {};\n"
                "    }\n"
                "    if (strategy === 'cursor') {\n"
                "        const { cursor, limit } = opts;\n"
                "        // TODO: Return {data, nextCursor, hasNext}\n"
                "        return {};\n"
                "    }\n"
                "    return {};\n"
                "}\n\n"
                "const { strategy, records, ...opts } = input;\n"
                "console.log(JSON.stringify(paginate(strategy, records, opts)));\n"
            ),
            "python": py_cli(
                "def paginate(strategy, records, opts):\n"
                "    if strategy == 'offset':\n"
                "        page, per_page = opts['page'], opts['perPage']\n"
                "        # TODO: Return {data, total, page, totalPages, hasNext}\n"
                "        return {}\n"
                "    if strategy == 'cursor':\n"
                "        cursor, limit = opts.get('cursor'), opts['limit']\n"
                "        # TODO: Return {data, nextCursor, hasNext}\n"
                "        return {}\n"
                "    return {}\n\n"
                "strategy = data.pop('strategy')\nrecords = data.pop('records')\n"
                "print(json.dumps(paginate(strategy, records, data)))\n"
            ),
        },
        "test_cases": [
            {"id": "qp-1", "name": "offset page 2", "hidden": False, "weight": 1,
             "stdin": json.dumps({"strategy": "offset", "records": [{"id": i} for i in range(1, 10)], "page": 2, "perPage": 3}),
             "expected_output": json.dumps({"data": [{"id": 4}, {"id": 5}, {"id": 6}], "total": 9, "page": 2, "totalPages": 3, "hasNext": True}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    # ═══════════════════════ DEVOPS — (5) ════════════════════════════════════

    {
        "title": "ENV File Parser",
        "slug": "env-file-parser",
        "short_description": "Parse a .env file format into a key-value object, handling comments and quotes.",
        "description": (
            "### .env File Parser\n\n"
            "Parse a `.env` formatted string into a JSON object. Handle:\n"
            "- `KEY=value` — basic assignment\n"
            "- Lines starting with `#` — comments (skip)\n"
            "- `KEY=\"quoted value\"` — strip surrounding quotes\n"
            "- `KEY='single quoted'` — strip single quotes\n"
            "- Empty lines — skip\n\n"
            "### Input (stdin)\nRaw `.env` file content as a string.\n\n"
            "### Output (stdout)\nJSON object of key-value pairs."
        ),
        "domain": "DevOps", "difficulty": "Easy",
        "tags": ["DevOps", "Parsing", "Configuration", "Strings"],
        "technologies": ["javascript", "python"],
        "hints": ["Split by newline, then process each line.", "Strip the surrounding quotes after splitting on the first `=`."],
        "concepts": ["Configuration Parsing", "String Manipulation"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 100, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_raw(
                "function parseEnv(content) {\n"
                "    const result = {};\n"
                "    for (const line of content.split('\\n')) {\n"
                "        const trimmed = line.trim();\n"
                "        // TODO: Skip empty lines and comments (#)\n"
                "        // TODO: Split on first '=', strip quotes from value\n"
                "    }\n"
                "    return result;\n"
                "}\n\n"
                "console.log(JSON.stringify(parseEnv(input)));\n"
            ),
            "python": py_raw(
                "def parse_env(content):\n"
                "    result = {}\n"
                "    for line in content.split('\\n'):\n"
                "        line = line.strip()\n"
                "        # TODO: Skip empty lines and comments (#)\n"
                "        # TODO: Split on first '=', strip quotes from value\n"
                "    return result\n\n"
                "print(json.dumps(parse_env(input_data)))\n"
                "import json\n"
            ),
        },
        "test_cases": [
            {"id": "ef-1", "name": "parse env with comments and quotes", "hidden": False, "weight": 1,
             "stdin": "# Database config\nDB_HOST=localhost\nDB_PORT=5432\nDB_NAME=\"myapp\"\nSECRET='mysecret'\n\n# End",
             "expected_output": json.dumps({"DB_HOST": "localhost", "DB_PORT": "5432", "DB_NAME": "myapp", "SECRET": "mysecret"}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Cron Expression Parser",
        "slug": "cron-parser",
        "short_description": "Parse and describe a cron expression in human-readable form.",
        "description": (
            "### Cron Expression Parser\n\n"
            "Parse a standard 5-field cron expression and return a human-readable description and the next 3 trigger times from a given start time.\n\n"
            "**Fields:** `minute hour day-of-month month day-of-week`\n\n"
            "### Input (stdin)\n```json\n{\"cron\": \"0 9 * * 1-5\", \"description\": true}\n```\n\n"
            "### Output (stdout)\n```json\n{\"description\": \"At 09:00 on every day-of-week from Monday through Friday\", \"fields\": {\"minute\": \"0\", \"hour\": \"9\", \"dom\": \"*\", \"month\": \"*\", \"dow\": \"1-5\"}}\n```"
        ),
        "domain": "DevOps", "difficulty": "Medium",
        "tags": ["DevOps", "Cron", "Parsing", "Scheduling"],
        "technologies": ["javascript", "python"],
        "hints": ["Split the cron string by spaces into 5 fields.", "Map field values to English: `*` = every, `0-5` = range, `*/2` = every 2."],
        "concepts": ["Cron Syntax", "Scheduling", "String Parsing"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function parseCron(cron) {\n"
                "    const [minute, hour, dom, month, dow] = cron.split(' ');\n"
                "    // TODO: Build a human-readable description\n"
                "    // Return {description, fields: {minute, hour, dom, month, dow}}\n"
                "    return {\n"
                "        description: 'TODO: implement description',\n"
                "        fields: { minute, hour, dom, month, dow }\n"
                "    };\n"
                "}\n\n"
                "console.log(JSON.stringify(parseCron(input.cron)));\n"
            ),
            "python": py_cli(
                "def parse_cron(cron):\n"
                "    parts = cron.split()\n"
                "    minute, hour, dom, month, dow = parts\n"
                "    # TODO: Build a human-readable description\n"
                "    return {\n"
                "        'description': 'TODO: implement description',\n"
                "        'fields': {'minute': minute, 'hour': hour, 'dom': dom, 'month': month, 'dow': dow}\n"
                "    }\n\n"
                "print(json.dumps(parse_cron(data['cron'])))\n"
            ),
        },
        "test_cases": [
            {"id": "cp2-1", "name": "parse basic cron fields", "hidden": False, "weight": 1,
             "stdin": json.dumps({"cron": "0 9 * * 1-5", "description": True}),
             "expected_output": json.dumps({"description": "At 09:00 on every day-of-week from Monday through Friday", "fields": {"minute": "0", "hour": "9", "dom": "*", "month": "*", "dow": "1-5"}}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Log Level Filter",
        "slug": "log-level-filter",
        "short_description": "Parse structured logs and filter/aggregate by severity level.",
        "description": (
            "### Log Level Filter\n\n"
            "Given a list of log entries (each with `level`, `message`, `timestamp`), return a summary grouped by level with counts.\n\n"
            "**Levels (ascending severity):** DEBUG, INFO, WARN, ERROR, FATAL\n\n"
            "### Input (stdin)\n```json\n{\"logs\": [{\"level\": \"INFO\", \"message\": \"Server started\", \"timestamp\": \"2024-01-01T10:00:00Z\"}, ...], \"minLevel\": \"WARN\"}\n```\n\n"
            "### Output (stdout)\nFiltered logs (≥ minLevel) plus summary `{DEBUG: 0, INFO: 0, WARN: N, ERROR: M}`"
        ),
        "domain": "DevOps", "difficulty": "Easy",
        "tags": ["DevOps", "Logging", "Filtering", "Operations"],
        "technologies": ["javascript", "python"],
        "hints": ["Define level order as an array and compare indices.", "Filter logs where LEVELS.indexOf(log.level) >= LEVELS.indexOf(minLevel)."],
        "concepts": ["Log Management", "Severity Levels", "Data Filtering"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 120, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_cli(
                "const LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'];\n\n"
                "function filterLogs(logs, minLevel) {\n"
                "    const minIdx = LEVELS.indexOf(minLevel);\n"
                "    // TODO: Filter logs where level index >= minIdx\n"
                "    const filtered = [];\n"
                "    // TODO: Build summary object {DEBUG: 0, INFO: 0, WARN: N, ...} from filtered logs\n"
                "    const summary = {};\n"
                "    return { filtered, summary };\n"
                "}\n\n"
                "console.log(JSON.stringify(filterLogs(input.logs, input.minLevel)));\n"
            ),
            "python": py_cli(
                "LEVELS = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']\n\n"
                "def filter_logs(logs, min_level):\n"
                "    min_idx = LEVELS.index(min_level)\n"
                "    # TODO: Filter logs where level index >= min_idx\n"
                "    filtered = []\n"
                "    # TODO: Build summary dict from filtered logs\n"
                "    summary = {}\n"
                "    return {'filtered': filtered, 'summary': summary}\n\n"
                "print(json.dumps(filter_logs(data['logs'], data['minLevel'])))\n"
            ),
        },
        "test_cases": [
            {"id": "llf-1", "name": "filter by WARN level", "hidden": False, "weight": 1,
             "stdin": json.dumps({"logs": [{"level": "INFO", "message": "Started", "timestamp": "2024-01-01T10:00:00Z"}, {"level": "WARN", "message": "Slow query", "timestamp": "2024-01-01T10:01:00Z"}, {"level": "ERROR", "message": "DB failed", "timestamp": "2024-01-01T10:02:00Z"}], "minLevel": "WARN"}),
             "expected_output": json.dumps({"filtered": [{"level": "WARN", "message": "Slow query", "timestamp": "2024-01-01T10:01:00Z"}, {"level": "ERROR", "message": "DB failed", "timestamp": "2024-01-01T10:02:00Z"}], "summary": {"WARN": 1, "ERROR": 1}}) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Docker Log Parser",
        "slug": "docker-log-parser",
        "short_description": "Parse Docker container log output into structured events with metadata.",
        "description": (
            "### Docker Log Parser\n\n"
            "Parse Docker-style log lines (with timestamps and stream indicators) into structured objects.\n\n"
            "**Docker log format:** `2024-01-15T10:23:45.123456789Z stdout F Server started on port 3000`\n\n"
            "**Fields:** `timestamp`, `stream` (stdout/stderr), `log` (message after F/P indicator)\n\n"
            "### Input (stdin)\nMultiline Docker log string.\n\n"
            "### Output\nJSON array of `{timestamp, stream, log}` objects."
        ),
        "domain": "DevOps", "difficulty": "Easy",
        "tags": ["DevOps", "Docker", "Logging", "Parsing"],
        "technologies": ["javascript", "python"],
        "hints": ["Split each line by spaces. Fields: [0]=timestamp, [1]=stream, [2]=flag(F/P), [3..]=message.", "Join remaining parts for the log message."],
        "concepts": ["Log Parsing", "Docker", "Structured Logging"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 120, "estimated_time_minutes": 15,
        "starter_code": {
            "javascript": js_raw(
                "function parseDockerLogs(content) {\n"
                "    // TODO: Parse each line into {timestamp, stream, log}\n"
                "    // Format: '<timestamp> <stream> <F|P> <message...>'\n"
                "    return content.split('\\n')\n"
                "        .filter(l => l.trim())\n"
                "        .map(line => {\n"
                "            const parts = line.split(' ');\n"
                "            // TODO: Extract timestamp, stream, log message\n"
                "            return { timestamp: '', stream: '', log: '' };\n"
                "        });\n"
                "}\n\n"
                "console.log(JSON.stringify(parseDockerLogs(input)));\n"
            ),
            "python": py_raw(
                "def parse_docker_logs(content):\n"
                "    result = []\n"
                "    for line in content.split('\\n'):\n"
                "        line = line.strip()\n"
                "        if not line: continue\n"
                "        parts = line.split(' ', 3)\n"
                "        # TODO: Extract timestamp=parts[0], stream=parts[1], log=parts[3]\n"
                "        result.append({'timestamp': '', 'stream': '', 'log': ''})\n"
                "    return result\n\n"
                "import json\n"
                "print(json.dumps(parse_docker_logs(input_data)))\n"
            ),
        },
        "test_cases": [
            {"id": "dlp-1", "name": "parse docker log lines", "hidden": False, "weight": 1,
             "stdin": "2024-01-15T10:23:45.123Z stdout F Server started on port 3000\n2024-01-15T10:23:46.456Z stderr F Warning: low memory",
             "expected_output": json.dumps([{"timestamp": "2024-01-15T10:23:45.123Z", "stream": "stdout", "log": "Server started on port 3000"}, {"timestamp": "2024-01-15T10:23:46.456Z", "stream": "stderr", "log": "Warning: low memory"}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Dependency Graph Resolver",
        "slug": "dependency-resolver",
        "short_description": "Resolve package dependency install order avoiding circular dependencies.",
        "description": (
            "### Dependency Graph Resolver\n\n"
            "Given a set of packages and their dependencies, compute the correct installation order.\n\n"
            "**Input:**\n```json\n{\"packages\": {\"A\": [\"B\",\"C\"], \"B\": [\"D\"], \"C\": [\"D\"], \"D\": []}}\n```\n\n"
            "**Output:** Install order where each package appears after all its dependencies.\n```json\n[\"D\", \"B\", \"C\", \"A\"]\n```\n\n"
            "If there's a circular dependency, return `{\"error\": \"Circular dependency detected\"}`."
        ),
        "domain": "DevOps", "difficulty": "Medium",
        "tags": ["DevOps", "Graphs", "Package Management", "Topological Sort"],
        "technologies": ["javascript", "python"],
        "hints": ["This is topological sort on a dependency DAG.", "Use post-order DFS or Kahn's algorithm."],
        "concepts": ["Dependency Resolution", "Topological Sort", "Package Management"],
        "runtime": "algorithm", "execution_mode": "cli",
        "xp_reward": 200, "estimated_time_minutes": 30,
        "starter_code": {
            "javascript": js_cli(
                "function resolveDeps(packages) {\n"
                "    const visited = new Set();\n"
                "    const result = [];\n"
                "    const visiting = new Set(); // cycle detection\n\n"
                "    function dfs(pkg) {\n"
                "        if (visiting.has(pkg)) return false; // cycle!\n"
                "        if (visited.has(pkg)) return true;\n"
                "        visiting.add(pkg);\n"
                "        for (const dep of (packages[pkg] || [])) {\n"
                "            if (!dfs(dep)) return false;\n"
                "        }\n"
                "        visiting.delete(pkg);\n"
                "        visited.add(pkg);\n"
                "        result.push(pkg);\n"
                "        return true;\n"
                "    }\n\n"
                "    for (const pkg of Object.keys(packages)) {\n"
                "        if (!dfs(pkg)) {\n"
                "            console.log(JSON.stringify({ error: 'Circular dependency detected' }));\n"
                "            return;\n"
                "        }\n"
                "    }\n"
                "    console.log(JSON.stringify(result));\n"
                "}\n\n"
                "resolveDeps(input.packages);\n"
            ),
            "python": py_cli(
                "def resolve_deps(packages):\n"
                "    visited = set()\n"
                "    visiting = set()\n"
                "    result = []\n\n"
                "    def dfs(pkg):\n"
                "        if pkg in visiting: return False\n"
                "        if pkg in visited: return True\n"
                "        visiting.add(pkg)\n"
                "        for dep in packages.get(pkg, []):\n"
                "            if not dfs(dep): return False\n"
                "        visiting.discard(pkg)\n"
                "        visited.add(pkg)\n"
                "        result.append(pkg)\n"
                "        return True\n\n"
                "    for pkg in packages:\n"
                "        if not dfs(pkg):\n"
                "            return {'error': 'Circular dependency detected'}\n"
                "    return result\n\n"
                "print(json.dumps(resolve_deps(data['packages'])))\n"
            ),
        },
        "test_cases": [
            {"id": "dr-1", "name": "resolve dependency order", "hidden": False, "weight": 1,
             "stdin": json.dumps({"packages": {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}}),
             "expected_output": json.dumps(["D", "B", "C", "A"]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    # ═══════════════════════ FULLSTACK — (4) ═════════════════════════════════

    {
        "title": "Shopping Cart API",
        "slug": "shopping-cart-api",
        "short_description": "Build a shopping cart API with product management, cart operations, and checkout.",
        "description": (
            "### Shopping Cart API\n\n"
            "Build an e-commerce cart backend:\n"
            "- `POST /products` — create `{name, price, stock}`, return product\n"
            "- `POST /cart` — add `{productId, qty}` to session cart\n"
            "- `GET /cart` — return current cart with line items and `total`\n"
            "- `DELETE /cart/:productId` — remove item from cart\n"
            "- `POST /cart/checkout` — validate stock, decrement, return `{orderId, total, items}`\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "Fullstack", "difficulty": "Hard",
        "tags": ["REST", "E-Commerce", "MongoDB", "Business Logic"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Shopping Cart", "Inventory Management", "Checkout Flow"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient, ObjectId } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet products;\nconst cart = {}; // in-memory cart: {productId: {qty, price, name}}\nclient.connect().then(() => { products = client.db('shop_db').collection('products'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /products\n// TODO: POST /cart\n// TODO: GET /cart\n// TODO: DELETE /cart/:productId\n// TODO: POST /cart/checkout\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "sc-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Notification Preferences API",
        "slug": "notification-prefs-api",
        "short_description": "Build a user notification preference management API with channel routing.",
        "description": (
            "### Notification Preferences API\n\n"
            "Build a notification system backend:\n"
            "- `POST /users/:id/preferences` — set notification preferences `{email, push, sms}` (each boolean)\n"
            "- `GET /users/:id/preferences` — return user notification settings\n"
            "- `POST /notifications/send` — accept `{userId, message, channels[]}`, route to enabled channels only, return `{sent: [], skipped: []}`\n"
            "- `GET /notifications/history/:userId` — list notifications sent to user\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "Fullstack", "difficulty": "Hard",
        "tags": ["REST", "Notifications", "MongoDB", "User Settings"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Notification Systems", "User Preferences", "Channel Routing"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 55,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet prefs, history;\nclient.connect().then(() => {\n    const db = client.db('notify_db');\n    prefs = db.collection('preferences');\n    history = db.collection('history');\n});\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /users/:id/preferences\n// TODO: GET /users/:id/preferences\n// TODO: POST /notifications/send\n// TODO: GET /notifications/history/:userId\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "np2-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "File Storage API",
        "slug": "file-storage-api",
        "short_description": "Build an S3-like file storage API with upload, list, download, and delete.",
        "description": (
            "### File Storage API (S3-like)\n\n"
            "Build a simplified file storage service:\n"
            "- `POST /files` — accept `{filename, content, contentType}`, store and return `{fileId, filename, size, url}`\n"
            "- `GET /files` — list all files `{fileId, filename, size, contentType, uploadedAt}`\n"
            "- `GET /files/:id` — return file metadata + content\n"
            "- `DELETE /files/:id` — delete file\n"
            "- `GET /files/:id/download` — return the raw content as the response body\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "Fullstack", "difficulty": "Hard",
        "tags": ["REST", "File Storage", "MongoDB", "S3-like"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["File Storage", "Binary Data", "Object Storage"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient, ObjectId } = require('mongodb');\nconst app = express();\napp.use(express.json({ limit: '10mb' }));\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet files;\nclient.connect().then(() => { files = client.db('storage_db').collection('files'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /files - store {filename, content, contentType}\n// TODO: GET /files - list all files\n// TODO: GET /files/:id - get file with content\n// TODO: DELETE /files/:id\n// TODO: GET /files/:id/download - serve raw content\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "fs-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },

    {
        "title": "Leaderboard API",
        "slug": "leaderboard-api",
        "short_description": "Build a competitive leaderboard API with real-time ranking and score submission.",
        "description": (
            "### Leaderboard API\n\n"
            "Build a game leaderboard service:\n"
            "- `POST /scores` — submit `{userId, username, score, gameId}`, return rank position\n"
            "- `GET /leaderboard/:gameId` — return top-N (default 10) scores sorted descending\n"
            "- `GET /leaderboard/:gameId/rank/:userId` — return user's current rank and score\n"
            "- `DELETE /scores/:userId/:gameId` — remove user's score\n"
            "- `GET /leaderboard/:gameId/around/:userId` — 5 users above and below this user\n"
            "- `GET /health` — `{status: 'ok'}`"
        ),
        "domain": "Fullstack", "difficulty": "Hard",
        "tags": ["REST", "MongoDB", "Ranking", "Gaming", "Sorted Sets"],
        "technologies": ["javascript", "python", "mongodb"],
        "concepts": ["Leaderboard Design", "Ranking Algorithms", "Score Submission"],
        "runtime": "api", "execution_mode": "http",
        "xp_reward": 400, "estimated_time_minutes": 60,
        "starter_code": {
            "js_mongodb": json.dumps({
                "solution.js": (
                    "const express = require('express');\nconst { MongoClient } = require('mongodb');\nconst app = express();\napp.use(express.json());\n\n"
                    "const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');\nlet scores;\nclient.connect().then(() => { scores = client.db('leaderboard_db').collection('scores'); });\n\n"
                    "app.get('/health', (req, res) => res.json({ status: 'ok' }));\n\n"
                    "// TODO: POST /scores - upsert score, return {rank, score, userId}\n// TODO: GET /leaderboard/:gameId - top 10 scores\n// TODO: GET /leaderboard/:gameId/rank/:userId - user's rank\n// TODO: DELETE /scores/:userId/:gameId\n// TODO: GET /leaderboard/:gameId/around/:userId\n\n"
                    "const PORT = process.env.PORT || 3000;\napp.listen(PORT, () => console.log('Server on port ' + PORT));\n"
                )
            })
        },
        "test_cases": [
            {"id": "lb-1", "name": "health check", "hidden": False, "weight": 1,
             "stdin": json.dumps([{"method": "GET", "path": "/health"}]),
             "expected_output": json.dumps([{"request": {"method": "GET", "path": "/health"}, "response": {"status": 200, "headers": {}, "body": {"status": "ok"}}}]) + "\n",
             "comparison_mode": "json"},
        ],
    },
]

print(f"Total new challenges defined: {len(CHALLENGES)}")


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    print("Fetching existing slugs to avoid duplicates...")
    existing = await db.problems.distinct("slug")
    existing_set = set(existing)
    print(f"Existing challenges: {len(existing_set)}")

    inserted = 0
    skipped = 0
    for c in CHALLENGES:
        if c["slug"] in existing_set:
            print(f"  SKIP (already exists): {c['slug']}")
            skipped += 1
            continue

        doc = {
            "challenge_id": str(uuid4()),
            "title": c["title"],
            "slug": c["slug"],
            "short_description": c["short_description"],
            "description": c["description"],
            "domain": c["domain"],
            "difficulty": c["difficulty"],
            "tags": c.get("tags", []),
            "technologies": c.get("technologies", []),
            "hints": c.get("hints", []),
            "concepts": c.get("concepts", []),
            "starter_code": c.get("starter_code", {}),
            "test_cases": c.get("test_cases", []),
            "xp_reward": c.get("xp_reward", 100),
            "rating_reward": 10,
            "estimated_time_minutes": c.get("estimated_time_minutes", 30),
            "runtime": c.get("runtime"),
            "execution_mode": c.get("execution_mode"),
            "is_published": True,
            "is_featured": False,
            "is_archived": False,
        }
        await db.problems.insert_one(doc)
        print(f"  INSERT: {c['title']} [{c['domain']}] ({c['difficulty']})")
        inserted += 1

    print(f"\nDone — inserted {inserted}, skipped {skipped}.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
