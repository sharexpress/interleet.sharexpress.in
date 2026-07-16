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

import { useEffect, useRef, memo } from "react";
import { LANG_TO_MONACO } from "./editor.config";

// Monaco CDN loader utility
function loadMonaco() {
  return new Promise((resolve) => {
    if (window.__monacoReady) {
      resolve(window.monaco);
      return;
    }
    const s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/monaco-editor@0.50.0/min/vs/loader.js";
    s.onload = () => {
      window.require.config({
        paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.50.0/min/vs" },
      });
      window.require(["vs/editor/editor.main"], (monaco) => {
        window.monaco = monaco;
        window.__monacoReady = true;
        resolve(monaco);
      });
    };
    document.head.appendChild(s);
  });
}

const MonacoEditor = memo(function MonacoEditor({ value, language, onChange }) {
  const containerRef = useRef(null);
  const editorRef = useRef(null);
  const subRef = useRef(null);
  const prevLang = useRef(language);

  // Keep refs of value and language to prevent stale closures when monaco loads asynchronously
  const valueRef = useRef(value);
  valueRef.current = value;
  const languageRef = useRef(language);
  languageRef.current = language;

  // Store latest onChange callback in a ref to avoid stale closures in Monaco listeners
  const onChangeRef = useRef(onChange);
  useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  useEffect(() => {
    let alive = true;
    loadMonaco().then((monaco) => {
      if (!alive || !containerRef.current || editorRef.current) return;

      const editor = monaco.editor.create(containerRef.current, {
        value: valueRef.current,
        language: LANG_TO_MONACO[languageRef.current] ?? "typescript",
        theme: "vs-dark",
        fontSize: 13,
        fontFamily: '"JetBrains Mono", "Fira Code", ui-monospace, monospace',
        fontLigatures: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        lineNumbers: "on",
        renderLineHighlight: "gutter",
        padding: { top: 12, bottom: 12 },
        tabSize: 2,
        wordWrap: "on",
        automaticLayout: true,
        scrollbar: { verticalScrollbarSize: 5, horizontalScrollbarSize: 5 },
        overviewRulerLanes: 0,
        renderWhitespace: "none",
        contextmenu: true,
        glyphMargin: false,
        folding: true,
        suggest: { showKeywords: true },
      });

      editorRef.current = editor;
      subRef.current = editor.onDidChangeModelContent(() => onChangeRef.current?.(editor.getValue()));

      // Sync the latest value and language immediately after the editor mounts
      const model = editor.getModel();
      if (model) {
        monaco.editor.setModelLanguage(model, LANG_TO_MONACO[languageRef.current] ?? "typescript");
        if (model.getValue() !== valueRef.current) {
          model.setValue(valueRef.current || "");
        }
      }
    });

    return () => {
      alive = false;
      subRef.current?.dispose();
      editorRef.current?.dispose();
      editorRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!editorRef.current || !window.monaco) return;
    const model = editorRef.current.getModel();
    if (!model) return;
    window.monaco.editor.setModelLanguage(model, LANG_TO_MONACO[language] ?? "typescript");
    if (prevLang.current !== language || model.getValue() !== value) {
      model.setValue(value || "");
      prevLang.current = language;
    }
  }, [language, value]);

  return <div ref={containerRef} style={{ height: "100%", width: "100%" }} />;
});

export default MonacoEditor;
