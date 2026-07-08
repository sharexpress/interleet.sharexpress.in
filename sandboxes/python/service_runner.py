import sys
import json
import time
import urllib.request
import subprocess
import socket
import os

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def main():
    logs = []
    start_time = time.time()
    
    workspace_dir = os.environ.get("WORKSPACE_DIR", ".")
    try:
        with open(f"{workspace_dir}/runtime.json") as f:
            config = json.load(f)
    except Exception as e:
        print(json.dumps({"status": "error", "logs": [f"Failed to read runtime.json: {e}"]}))
        sys.exit(1)

    port = config.get("port", get_free_port())
    cmd = config.get("command")
    health = config.get("health", {})
    health_path = health.get("path", "/health")
    health_type = health.get("type", "http")

    env = dict(os.environ)
    env["PORT"] = str(port)

    # ── Phase 4.1 Database Mocking ──
    db_processes = []
    
    # 1. Redis
    redis_config = config.get("redis", False)
    if redis_config:
        logs.append("Starting in-memory Redis on port 6379...")
        env["REDIS_URL"] = "redis://127.0.0.1:6379"
        try:
            r_proc = subprocess.Popen(
                ["redis-server", "--port", "6379", "--save", ""],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            db_processes.append(r_proc)
        except Exception as e:
            logs.append(f"Failed to start Redis: {e}")

    # 2. SQLite
    sqlite_config = config.get("sqlite", {})
    if sqlite_config or os.path.exists(f"{workspace_dir}/seed.sql"):
        db_file = sqlite_config.get("db_file", "db.sqlite")
        seed_file = sqlite_config.get("seed_file", "seed.sql")
        
        db_path = f"{workspace_dir}/{db_file}"
        env["DATABASE_URL"] = f"sqlite:///{db_path}"
        
        if os.path.exists(db_path):
            os.remove(db_path)
            
        if seed_file:
            seed_path = f"{workspace_dir}/{seed_file}"
            logs.append(f"Hydrating SQLite database from {seed_file}...")
            if os.path.exists(seed_path):
                try:
                    with open(seed_path, "r") as sf:
                        subprocess.run(
                            ["sqlite3", db_path],
                            stdin=sf,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True
                        )
                except subprocess.CalledProcessError as e:
                    logs.append(f"Warning: SQLite seed failed: {e.stderr.decode('utf-8', errors='ignore')}")
            else:
                logs.append(f"Warning: SQLite seed file {seed_file} not found.")

    # Write a simple shell wrapper to ensure command is found
    # If cmd is an array, we execute it directly
    logs.append(f"Starting server with PORT={port}...")
    try:
        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=workspace_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        print(json.dumps({"status": "error", "logs": [f"Failed to start server: {e}"]}))
        sys.exit(1)

    # Health check polling
    is_ready = False
    for _ in range(50): # 5 seconds max
        try:
            if health_type == "tcp":
                with socket.create_connection(("127.0.0.1", port), timeout=1.0):
                    is_ready = True
                    break
            else:
                req = urllib.request.Request(f"http://127.0.0.1:{port}{health_path}", method="GET")
                with urllib.request.urlopen(req, timeout=1.0) as res:
                    if res.status < 500:
                        is_ready = True
                        break
        except Exception:
            pass
        
        # Check if process crashed
        if process.poll() is not None:
            break
            
        time.sleep(0.1)

    startup_time_ms = int((time.time() - start_time) * 1000)

    if not is_ready:
        process.terminate()
        stdout, stderr = process.communicate()
        logs.append(f"Server failed to start or pass health check within 5 seconds.")
        
        for p in db_processes:
            try:
                p.terminate()
            except:
                pass
                
        print(json.dumps({
            "status": "error",
            "startupTime": startup_time_ms,
            "stdout": stdout.splitlines() if stdout else [],
            "stderr": stderr.splitlines() if stderr else [],
            "logs": logs,
            "exitCode": process.returncode
        }))
        sys.exit(1)

    logs.append(f"Server ready in {startup_time_ms}ms.")

    # Read requests from stdin.txt
    requests = []
    try:
        with open(f"{workspace_dir}/stdin.txt") as f:
            raw = f.read()
            if raw.strip():
                requests = json.loads(raw)
    except Exception as e:
        logs.append(f"Warning: Failed to parse stdin.txt requests: {e}")

    # Execute requests
    responses = []
    for req in requests:
        method = req.get("method", "GET")
        path = req.get("path", "/")
        headers = req.get("headers", {})
        body = req.get("body", None)

        url = f"http://127.0.0.1:{port}{path}"
        
        data = None
        if body:
            if isinstance(body, dict) or isinstance(body, list):
                data = json.dumps(body).encode("utf-8")
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            else:
                data = str(body).encode("utf-8")

        req_obj = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        res_data = {
            "request": req,
            "response": {}
        }
        
        try:
            with urllib.request.urlopen(req_obj, timeout=5.0) as res:
                res_body = res.read().decode("utf-8")
                try:
                    parsed_body = json.loads(res_body)
                except:
                    parsed_body = res_body
                    
                res_data["response"] = {
                    "status": res.status,
                    "headers": dict(res.getheaders()),
                    "body": parsed_body
                }
        except urllib.error.HTTPError as e:
            res_body = e.read().decode("utf-8")
            try:
                parsed_body = json.loads(res_body)
            except:
                parsed_body = res_body
            res_data["response"] = {
                "status": e.code,
                "headers": dict(e.headers),
                "body": parsed_body
            }
        except Exception as e:
            res_data["response"] = {
                "status": 500,
                "error": str(e)
            }
            
        responses.append(res_data)

    # Clean up
    process.terminate()
    try:
        stdout, stderr = process.communicate(timeout=2.0)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        
    for p in db_processes:
        try:
            p.terminate()
            p.kill()
        except:
            pass

    # Return structured result
    print(json.dumps({
        "status": "success",
        "startupTime": startup_time_ms,
        "responses": responses,
        "stdout": stdout.splitlines() if stdout else [],
        "stderr": stderr.splitlines() if stderr else [],
        "logs": logs,
        "exitCode": process.returncode
    }))

if __name__ == "__main__":
    main()
