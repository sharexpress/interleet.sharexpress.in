#!/usr/bin/env python3
"""
Seed & Enrich all 339+ problems in MongoDB (`interleet.problems`) so every single
problem contains explicit `starter_code` keys for all supported languages and databases directly in the database.
"""

import os
import json
from pymongo import MongoClient

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    return client["interleet"]

# Standard starter code templates for API / DB challenges
def build_api_starter(lang, db_type, slug, title):
    if lang == "js":
        if db_type == "sqlite":
            code = f"""const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
app.use(express.json());

const db = new sqlite3.Database(':memory:');

db.serialize(() => {{
  db.run(`
    CREATE TABLE IF NOT EXISTS items (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
}});

app.get('/health', (req, res) => res.json({{ status: 'ok' }}));

// TODO: Implement API endpoints for {title}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
"""
        elif db_type == "mongodb":
            code = f"""const express = require('express');
const {{ MongoClient }} = require('mongodb');
const app = express();
app.use(express.json());

const client = new MongoClient(process.env.MONGO_URI || 'mongodb://localhost:27017');
let db;

app.get('/health', (req, res) => res.json({{ status: 'ok' }}));

// TODO: Implement API endpoints for {title}

const PORT = process.env.PORT || 3000;
client.connect().then(() => {{
  db = client.db('app_db');
  app.listen(PORT, () => console.log('Server running on port ' + PORT));
}});
"""
        elif db_type == "postgres":
            code = f"""const express = require('express');
const {{ Pool }} = require('pg');
const app = express();
app.use(express.json());

const pool = new Pool({{ connectionString: process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/app_db' }});

app.get('/health', (req, res) => res.json({{ status: 'ok' }}));

// TODO: Implement API endpoints for {title}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
"""
        else: # mysql
            code = f"""const express = require('express');
const mysql = require('mysql2');
const app = express();
app.use(express.json());

const connection = mysql.createConnection(process.env.DATABASE_URL || 'mysql://root:root@127.0.0.1:3306/app_db');

app.get('/health', (req, res) => res.json({{ status: 'ok' }}));

// TODO: Implement API endpoints for {title}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server running on port ' + PORT));
"""
        return json.dumps({"solution.js": code})

    elif lang == "py":
        if db_type == "sqlite":
            code = f"""from fastapi import FastAPI
import sqlite3, os

app = FastAPI()

@app.get('/health')
def health():
    return {{'status': 'ok'}}

# TODO: Implement API endpoints for {title}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
        elif db_type == "mongodb":
            code = f"""from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017'))

@app.get('/health')
def health():
    return {{'status': 'ok'}}

# TODO: Implement API endpoints for {title}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
        elif db_type == "postgres":
            code = f"""from fastapi import FastAPI
import psycopg2, os

app = FastAPI()

@app.get('/health')
def health():
    return {{'status': 'ok'}}

# TODO: Implement API endpoints for {title}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
        else: # mysql
            code = f"""from fastapi import FastAPI
import os

app = FastAPI()

@app.get('/health')
def health():
    return {{'status': 'ok'}}

# TODO: Implement API endpoints for {title}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 3000))
    uvicorn.run(app, host='127.0.0.1', port=port)
"""
        return json.dumps({"main.py": code})

    elif lang == "go":
        if db_type == "sqlite":
            code = f"""package main

import (
	"database/sql"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/glebarez/go-sqlite"
)

func main() {{
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {{
		c.JSON(http.StatusOK, gin.H{{"status": "ok"}})
	}})

	// TODO: Implement API endpoints for {title}

	port := os.Getenv("PORT")
	if port == "" {{
		port = "3000"
	}}
	r.Run("127.0.0.1:" + port)
}}
"""
        elif db_type == "mongodb":
            code = f"""package main

import (
	"context"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {{
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {{
		c.JSON(http.StatusOK, gin.H{{"status": "ok"}})
	}})

	// TODO: Implement API endpoints for {title}

	port := os.Getenv("PORT")
	if port == "" {{
		port = "3000"
	}}
	r.Run("127.0.0.1:" + port)
}}
"""
        elif db_type == "postgres":
            code = f"""package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {{
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {{
		c.JSON(http.StatusOK, gin.H{{"status": "ok"}})
	}})

	// TODO: Implement API endpoints for {title}

	port := os.Getenv("PORT")
	if port == "" {{
		port = "3000"
	}}
	r.Run("127.0.0.1:" + port)
}}
"""
        else: # mysql
            code = f"""package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func main() {{
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {{
		c.JSON(http.StatusOK, gin.H{{"status": "ok"}})
	}})

	// TODO: Implement API endpoints for {title}

	port := os.Getenv("PORT")
	if port == "" {{
		port = "3000"
	}}
	r.Run("127.0.0.1:" + port)
}}
"""
        return json.dumps({"main.go": code})

    return ""


def build_backend_starter(lang, title):
    if lang in ["javascript", "js"]:
        return f"""// Write your JavaScript solution for {title}
const fs = require('fs');

function main() {{
  const inputJson = fs.readFileSync(0, 'utf-8').trim();
  const input = JSON.parse(inputJson);

  // TODO: Implement solution
  const result = {{ result: null }};
  console.log(JSON.stringify(result));
}}

main();
"""
    elif lang in ["typescript", "ts"]:
        return f"""// Write your TypeScript solution for {title}
import * as fs from 'fs';

function main() {{
  const inputJson = fs.readFileSync(0, 'utf-8').trim();
  const input = JSON.parse(inputJson);

  // TODO: Implement solution
  const result = {{ result: null }};
  console.log(JSON.stringify(result));
}}

main();
"""
    elif lang in ["python", "py"]:
        return f"""# Write your Python solution for {title}
import sys
import json

def main():
    input_json = sys.stdin.read().strip()
    data = json.loads(input_json)

    # TODO: Implement solution
    result = {{"result": None}}
    print(json.dumps(result))

if __name__ == '__main__':
    main()
"""
    elif lang in ["go"]:
        return f"""package main

import (
	"encoding/json"
	"fmt"
	"os"
)

func main() {{
	var input interface{{}}
	decoder := json.NewDecoder(os.Stdin)
	if err := decoder.Decode(&input); err != nil {{
		fmt.Fprintln(os.Stderr, "Error reading input:", err)
		os.Exit(1)
	}}

	// TODO: Implement solution
	result := map[string]interface{{}}{{"result": nil}}
	json.NewEncoder(os.Stdout).Encode(result)
}}
"""
    elif lang in ["java"]:
        return f"""import java.util.*;
import java.io.*;

public class Solution {{
    public static void main(String[] args) throws Exception {{
        Scanner scanner = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        while (scanner.hasNextLine()) sb.append(scanner.nextLine());
        String inputJson = sb.toString().trim();

        // TODO: Implement solution for {title}
        System.out.println("{{\\"result\\": null}}");
    }}
}}
"""
    elif lang in ["cpp"]:
        return f"""#include <iostream>
#include <string>
#include <sstream>

int main() {{
    std::ostringstream ss;
    ss << std::cin.rdbuf();
    std::string inputJson = ss.str();

    // TODO: Implement solution for {title}
    std::cout << "{{\\"result\\": null}}" << std::endl;
    return 0;
}}
"""
    elif lang in ["rust"]:
        return f"""use std::io::{{self, Read}};

fn main() {{
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    // TODO: Implement solution for {title}
    println!("{{\\"result\\": null}}");
}}
"""
    return ""


def seed_database_starter_codes():
    db = get_db()
    problems = list(db.problems.find({}))
    print(f"Loaded {len(problems)} problems from MongoDB.")

    updated_count = 0

    for p in problems:
        slug = p.get("slug", "")
        title = p.get("title", slug)
        domain = p.get("domain", "")

        starter_code = p.get("starter_code")
        if not isinstance(starter_code, dict):
            starter_code = {}

        original_keys = set(starter_code.keys())

        if domain in ["APIs", "Databases", "Fullstack"]:
            langs = ["js", "py", "go"]
            dbs = ["sqlite", "mongodb", "postgres", "mysql"]

            for l in langs:
                for d in dbs:
                    key = f"{l}_{d}"
                    if key not in starter_code or not starter_code[key]:
                        # If a related key exists (e.g. js_mongodb when populating js_sqlite), use it as base if available
                        base_key = next((k for k in starter_code if k.startswith(f"{l}_")), None)
                        if base_key and starter_code[base_key]:
                            starter_code[key] = starter_code[base_key]
                        else:
                            starter_code[key] = build_api_starter(l, d, slug, title)

                # Short aliases
                if l not in starter_code:
                    starter_code[l] = starter_code.get(f"{l}_sqlite") or starter_code.get(f"{l}_mongodb") or ""
                
                # Alias for javascript / python
                long_lang = "javascript" if l == "js" else ("python" if l == "py" else l)
                if long_lang not in starter_code:
                    starter_code[long_lang] = starter_code[l]

        elif domain in ["Backend", "Algorithms"]:
            std_langs = ["javascript", "typescript", "python", "go", "java", "cpp", "rust"]
            short_aliases = {"javascript": "js", "typescript": "ts", "python": "py", "go": "go", "java": "java", "cpp": "cpp", "rust": "rust"}

            for lang in std_langs:
                short = short_aliases[lang]
                if lang not in starter_code and short not in starter_code:
                    code = build_backend_starter(lang, title)
                    starter_code[lang] = code
                    starter_code[short] = code
                elif lang in starter_code and short not in starter_code:
                    starter_code[short] = starter_code[lang]
                elif short in starter_code and lang not in starter_code:
                    starter_code[lang] = starter_code[short]

        if set(starter_code.keys()) != original_keys:
            db.problems.update_one({"_id": p["_id"]}, {"$set": {"starter_code": starter_code}})
            updated_count += 1

    print(f"✅ Successfully seeded and enriched starter_code for {updated_count} / {len(problems)} problems in MongoDB.")

if __name__ == "__main__":
    seed_database_starter_codes()
