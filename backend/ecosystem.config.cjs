module.exports = {
  apps: [
    {
      name: "interleet-8001",
      script: "/usr/bin/bash",
      args: "-c '.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001 --proxy-headers --forwarded-allow-ips \"*\"'",
      cwd: "/home/santusht/desktop/projects/interleet/backend",
      env: {
        SERVER_PORT: "8001",
        WORKER_COUNT: "2"
      }
    },
    {
      name: "interleet-8003",
      script: "/usr/bin/bash",
      args: "-c '.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8003 --proxy-headers --forwarded-allow-ips \"*\"'",
      cwd: "/home/santusht/desktop/projects/interleet/backend",
      env: {
        SERVER_PORT: "8003",
        WORKER_COUNT: "2"
      }
    },
    {
      name: "interleet-8004",
      script: "/usr/bin/bash",
      args: "-c '.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8004 --proxy-headers --forwarded-allow-ips \"*\"'",
      cwd: "/home/santusht/desktop/projects/interleet/backend",
      env: {
        SERVER_PORT: "8004",
        WORKER_COUNT: "2"
      }
    },
    {
      name: "interleet-8005",
      script: "/usr/bin/bash",
      args: "-c '.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8005 --proxy-headers --forwarded-allow-ips \"*\"'",
      cwd: "/home/santusht/desktop/projects/interleet/backend",
      env: {
        SERVER_PORT: "8005",
        WORKER_COUNT: "2"
      }
    }
  ]
};
