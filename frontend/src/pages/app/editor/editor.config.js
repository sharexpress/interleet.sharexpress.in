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

export const LANG_TO_MONACO = {
  ts: "typescript", js: "javascript", py: "python", go: "go",
  html: "html", css: "css",
  java: "java", cpp: "cpp", rust: "rust",
  shell: "shell", yaml: "yaml", dockerfile: "dockerfile", plaintext: "plaintext",
  javascript: "javascript", typescript: "typescript", python: "python",
  multi: "shell",
};

export const LANG_LABEL = { ts: "TypeScript", js: "JavaScript", py: "Python", go: "Go", java: "Java", cpp: "C++", rust: "Rust" };
export const LANG_BADGE = { ts: "node v20.10", js: "node v20.10", py: "python 3.12", go: "go 1.22", java: "openjdk 21", cpp: "gcc 13.2", rust: "rustc 1.75" };
export const LANG_FILE = { ts: "solution.ts", js: "solution.js", py: "solution.py", go: "main.go", java: "Solution.java", cpp: "solution.cpp", rust: "solution.rs" };

export const BACKEND_LANG_TO_SHORT = {
  typescript: "ts",
  javascript: "js",
  python: "py",
  go: "go",
  cpp: "cpp",
  rust: "rust",
  java: "java",
  multi: "multi",
  html: "html",
};

// All starter codes are served dynamically from the MongoDB database table.
// All starter codes are served dynamically from the MongoDB database table (`interleet.problems`).
export const STARTERS = {};
export const DEFAULT_STARTER = {};

export function getStarter(slug, lang, dbChallenge, selectedDb = "sqlite") {
  if (!dbChallenge || !dbChallenge.starter_code) {
    return "";
  }

  const dbKey = selectedDb ? `${lang}_${selectedDb}` : lang;
  if (lang === "multi" && dbChallenge.starter_code.multi) {
    return dbChallenge.starter_code.multi;
  }
  if (lang === "html" && dbChallenge.starter_code.html) {
    return dbChallenge.starter_code.html;
  }
  if (dbKey && dbChallenge.starter_code[dbKey]) {
    return dbChallenge.starter_code[dbKey];
  }
  // Check exact short language key match
  if (dbChallenge.starter_code[lang]) {
    return dbChallenge.starter_code[lang];
  }
  // Check backend language name key (e.g. "javascript", "python")
  const backendKey = lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang;
  if (dbChallenge.starter_code[backendKey]) {
    return dbChallenge.starter_code[backendKey];
  }

  // Check any starter_code key matching target language (e.g. "js_mongodb" or "py_mongodb")
  const langPrefixMatch = Object.keys(dbChallenge.starter_code).find(
    (k) => k.startsWith(`${lang}_`) || k.startsWith(`${backendKey}_`)
  );
  if (langPrefixMatch && dbChallenge.starter_code[langPrefixMatch]) {
    return dbChallenge.starter_code[langPrefixMatch];
  }

  // Strictly return from database (no local fallbacks)
  const firstVal = Object.values(dbChallenge.starter_code)[0];
  return typeof firstVal === "string" ? firstVal : "";
}
