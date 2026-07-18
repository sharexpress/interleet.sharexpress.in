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

export function getStarterWithDb(slug, lang, dbChallenge, selectedDb = "sqlite") {
  if (!dbChallenge || !dbChallenge.starter_code) {
    return { code: "", matchedDb: selectedDb };
  }

  const KNOWN_DBS = ["sqlite", "mongodb", "postgres", "mysql"];
  const dbKey = selectedDb ? `${lang}_${selectedDb}` : lang;
  const backendKey = lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang;
  const backendDbKey = selectedDb ? `${backendKey}_${selectedDb}` : backendKey;

  // 1. Exact match for multi or html
  if (lang === "multi" && dbChallenge.starter_code.multi) {
    return { code: dbChallenge.starter_code.multi, matchedDb: selectedDb };
  }
  if (lang === "html" && dbChallenge.starter_code.html) {
    return { code: dbChallenge.starter_code.html, matchedDb: selectedDb };
  }

  // 2. Exact match for specific language + database combination (e.g. "js_sqlite", "py_mongodb", "go_postgres")
  if (dbKey && dbChallenge.starter_code[dbKey]) {
    return { code: dbChallenge.starter_code[dbKey], matchedDb: selectedDb };
  }
  if (backendDbKey && dbChallenge.starter_code[backendDbKey]) {
    return { code: dbChallenge.starter_code[backendDbKey], matchedDb: selectedDb };
  }

  // 3. Match any key starting with `${lang}_` (e.g. "js_mongodb") if specific dbKey wasn't found
  const langPrefixMatch = Object.keys(dbChallenge.starter_code).find(
    (k) => k.startsWith(`${lang}_`) || k.startsWith(`${backendKey}_`)
  );
  if (langPrefixMatch && dbChallenge.starter_code[langPrefixMatch]) {
    const parts = langPrefixMatch.split("_");
    const inferredDbFromKey = parts.length > 1 && KNOWN_DBS.includes(parts[parts.length - 1])
      ? parts[parts.length - 1]
      : selectedDb;
    return { code: dbChallenge.starter_code[langPrefixMatch], matchedDb: inferredDbFromKey };
  }

  // 4. Standalone language keys without DB suffix (e.g. "js", "javascript", "py", "python")
  if (dbChallenge.starter_code[lang]) {
    return { code: dbChallenge.starter_code[lang], matchedDb: selectedDb };
  }
  if (dbChallenge.starter_code[backendKey]) {
    return { code: dbChallenge.starter_code[backendKey], matchedDb: selectedDb };
  }

  // 5. First available entry in MongoDB starter_code
  const firstKey = Object.keys(dbChallenge.starter_code)[0];
  const firstVal = dbChallenge.starter_code[firstKey];
  const firstParts = firstKey ? firstKey.split("_") : [];
  const firstDb = firstParts.length > 1 && KNOWN_DBS.includes(firstParts[firstParts.length - 1])
    ? firstParts[firstParts.length - 1]
    : selectedDb;

  return {
    code: typeof firstVal === "string" ? firstVal : "",
    matchedDb: firstDb,
  };
}

export function getStarter(slug, lang, dbChallenge, selectedDb = "sqlite") {
  return getStarterWithDb(slug, lang, dbChallenge, selectedDb).code;
}
