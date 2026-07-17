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

// All starter codes are served from the question database table to avoid conflicts.
export const STARTERS = {};

export const DEFAULT_STARTER = {
  ts: `// Write your TypeScript solution here
import * as fs from 'fs';

function main() {
  const inputJson = fs.readFileSync(0, 'utf-8').trim();
  const input = JSON.parse(inputJson);

  // TODO: Implement your solution using 'input'
  const result = { result: null };
  console.log(JSON.stringify(result));
}

main();
`,
  js: `// Write your JavaScript solution here
const fs = require('fs');

function main() {
  const inputJson = fs.readFileSync(0, 'utf-8').trim();
  const input = JSON.parse(inputJson);

  // TODO: Implement your solution using 'input'
  const result = { result: null };
  console.log(JSON.stringify(result));
}

main();
`,
  py: `# Write your Python solution here
import sys
import json

def main():
    input_json = sys.stdin.read().strip()
    data = json.loads(input_json)

    # TODO: Implement your solution using 'data'
    result = {"result": None}
    print(json.dumps(result))

if __name__ == '__main__':
    main()
`,
  go: `package main

import (
	"encoding/json"
	"fmt"
	"os"
)

func main() {
	var input interface{}
	decoder := json.NewDecoder(os.Stdin)
	if err := decoder.Decode(&input); err != nil {
		fmt.Fprintln(os.Stderr, "Error reading input:", err)
		os.Exit(1)
	}

	// TODO: Implement your solution using 'input'
	result := map[string]interface{}{"result": nil}
	json.NewEncoder(os.Stdout).Encode(result)
}
`,
  go_sqlite: `package main

import (
	"database/sql"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/glebarez/go-sqlite"
)

func main() {
	db, err := sql.Open("sqlite", "db.sqlite")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement your API endpoints here

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`,
  go_postgres: `package main

import (
	"database/sql"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

func main() {
	db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement your API endpoints here

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`,
  go_mongodb: `package main

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
	mongoURI := os.Getenv("MONGO_URI")
	if mongoURI == "" {
		mongoURI = "mongodb://localhost:27017"
	}
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
	if err != nil {
		panic(err)
	}
	defer client.Disconnect(ctx)

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement your API endpoints here

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`,
  go_mysql: `package main

import (
	"database/sql"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

func main() {
	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		dbURL = "root:root@tcp(127.0.0.1:3306)/db"
	}
	db, err := sql.Open("mysql", dbURL)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})

	// TODO: Implement your API endpoints here

	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	r.Run("127.0.0.1:" + port)
}
`,
  java: `import java.util.*;
import java.io.*;

public class Solution {
    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        while (scanner.hasNextLine()) sb.append(scanner.nextLine());
        String inputJson = sb.toString().trim();

        // TODO: Implement your solution using 'inputJson'
        System.out.println("{\"result\": null}");
    }
}
`,
  cpp: `#include <iostream>
#include <string>
#include <sstream>

int main() {
    // Read JSON input from stdin
    std::ostringstream ss;
    ss << std::cin.rdbuf();
    std::string inputJson = ss.str();

    // TODO: Implement your solution using 'inputJson'
    std::cout << "{\"result\": null}" << std::endl;
    return 0;
}
`,
  rust: `use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let input_json = input.trim();

    // TODO: Implement your solution using 'input_json'
    println!("{{\"result\": null}}");
}
`,
};

export function getStarter(slug, lang, dbChallenge, selectedDb = "sqlite") {
  const dbKey = selectedDb ? `${lang}_${selectedDb}` : lang;
  if (dbChallenge?.starter_code) {
    if (lang === "multi" && dbChallenge.starter_code.multi) {
      return dbChallenge.starter_code.multi;
    }
    if (lang === "html" && dbChallenge.starter_code.html) {
      return dbChallenge.starter_code.html;
    }
    if (dbKey && dbChallenge.starter_code[dbKey]) {
      return dbChallenge.starter_code[dbKey];
    }
    // Map short lang key to full language name used in starter_code
    const backendKey = lang === "ts" ? "typescript" : lang === "js" ? "javascript" : lang === "py" ? "python" : lang === "go" ? "go" : lang;
    if (dbChallenge.starter_code[backendKey]) {
      return dbChallenge.starter_code[backendKey];
    }
    if (dbChallenge.starter_code[lang]) {
      return dbChallenge.starter_code[lang];
    }
  }
  return DEFAULT_STARTER[dbKey] ?? DEFAULT_STARTER[lang] ?? DEFAULT_STARTER.ts;
}
