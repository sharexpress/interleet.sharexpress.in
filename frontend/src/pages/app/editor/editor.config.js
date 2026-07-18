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
export const STARTERS = {};
export const DEFAULT_STARTER = {};

const API_STARTERS = {
  js_sqlite: JSON.stringify({
    "solution.js": `const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
app.use(express.json());

const db = new sqlite3.Database(':memory:');

app.get('/health', (req, res) => res.json({ status: 'ok' }));

// TODO: Implement API endpoints

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
`
  }),
  js_mongodb: JSON.stringify({
    "solution.js": `const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
app.use(express.json());

const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');

app.get('/health', (req, res) => res.json({ status: 'ok' }));

// TODO: Implement API endpoints

const PORT = process.env.PORT || 3000;
client.connect().then(() => {
  app.listen(PORT, () => console.log('Server running on port ' + PORT));
});
`
  }),
  js_postgres: JSON.stringify({
    "solution.js": `const express = require('express');
const { Pool } = require('pg');
const app = express();
app.use(express.json());

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.get('/health', (req, res) => res.json({ status: 'ok' }));

// TODO: Implement API endpoints

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
`
  }),
  js_mysql: JSON.stringify({
    "solution.js": `const express = require('express');
const mysql = require('mysql2');
const app = express();
app.use(express.json());

const connection = mysql.createConnection(process.env.DATABASE_URL || 'mysql://root:root@127.0.0.1:3306/db');

app.get('/health', (req, res) => res.json({ status: 'ok' }));

// TODO: Implement API endpoints

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
`
  }),
  py_sqlite: JSON.stringify({
    "main.py": `from fastapi import FastAPI
import sqlite3, os

app = FastAPI()

@app.get('/health')
def health():
    return {'status': 'ok'}

# TODO: Implement API endpoints

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
`
  }),
  py_mongodb: JSON.stringify({
    "main.py": `from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))

@app.get('/health')
def health():
    return {'status': 'ok'}

# TODO: Implement API endpoints

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
`
  }),
  py_postgres: JSON.stringify({
    "main.py": `from fastapi import FastAPI
import psycopg2, os

app = FastAPI()

@app.get('/health')
def health():
    return {'status': 'ok'}

# TODO: Implement API endpoints

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
`
  }),
  py_mysql: JSON.stringify({
    "main.py": `from fastapi import FastAPI
import os

app = FastAPI()

@app.get('/health')
def health():
    return {'status': 'ok'}

# TODO: Implement API endpoints

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
`
  }),
  go_sqlite: JSON.stringify({
    "main.go": `package main

import (
	"database/sql"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/glebarez/go-sqlite"
)

func main() {
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement API endpoints

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`
  }),
  go_mongodb: JSON.stringify({
    "main.go": `package main

import (
	"context"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement API endpoints

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`
  }),
  go_postgres: JSON.stringify({
    "main.go": `package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement API endpoints

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`
  }),
  go_mysql: JSON.stringify({
    "main.go": `package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement API endpoints

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`
  })
};

export function getStarter(slug, lang, dbChallenge, selectedDb = "sqlite") {
  if (!dbChallenge || !dbChallenge.starter_code) {
    const fallbackKey = `${lang}_${selectedDb}`;
    return API_STARTERS[fallbackKey] || API_STARTERS[`${lang}_sqlite`] || "";
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

  // Return API_STARTERS if available for this lang and DB combination
  const fallbackKey = `${lang}_${selectedDb}`;
  if (API_STARTERS[fallbackKey]) {
    return API_STARTERS[fallbackKey];
  }

  // Fallback to the first available string in database starter_code
  const firstVal = Object.values(dbChallenge.starter_code)[0];
  return typeof firstVal === "string" ? firstVal : "";
}
