const fs = require('fs');
const http = require('http');
const { spawn } = require('child_process');
const net = require('net');

function getFreePort() {
  return new Promise((resolve) => {
    const srv = net.createServer();
    srv.listen(0, () => {
      const port = srv.address().port;
      srv.close(() => resolve(port));
    });
  });
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function checkTcp(port) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    socket.setTimeout(100);
    socket.on('connect', () => {
      socket.destroy();
      resolve(true);
    });
    socket.on('timeout', () => {
      socket.destroy();
      resolve(false);
    });
    socket.on('error', () => {
      socket.destroy();
      resolve(false);
    });
    socket.connect(port, '127.0.0.1');
  });
}

function checkHttp(port, path) {
  return new Promise((resolve) => {
    const req = http.get({
      host: '127.0.0.1',
      port: port,
      path: path,
      timeout: 100
    }, (res) => {
      if (res.statusCode < 500) {
        resolve(true);
      } else {
        resolve(false);
      }
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => {
      req.abort();
      resolve(false);
    });
  });
}

function makeRequest(port, reqData) {
  return new Promise((resolve) => {
    const method = reqData.method || 'GET';
    const path = reqData.path || '/';
    const headers = reqData.headers || {};
    let bodyData = null;

    if (reqData.body) {
      if (typeof reqData.body === 'object') {
        bodyData = JSON.stringify(reqData.body);
        if (!headers['Content-Type']) headers['Content-Type'] = 'application/json';
      } else {
        bodyData = String(reqData.body);
      }
      headers['Content-Length'] = Buffer.byteLength(bodyData);
    }

    const options = {
      hostname: '127.0.0.1',
      port: port,
      path: path,
      method: method,
      headers: headers,
      timeout: 5000
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        let parsedBody = data;
        try { parsedBody = JSON.parse(data); } catch (e) {}
        resolve({
          request: reqData,
          response: {
            status: res.statusCode,
            headers: res.headers,
            body: parsedBody
          }
        });
      });
    });

    req.on('error', (e) => {
      resolve({
        request: reqData,
        response: { status: 500, error: e.message }
      });
    });

    req.on('timeout', () => {
      req.abort();
      resolve({
        request: reqData,
        response: { status: 504, error: 'Timeout' }
      });
    });

    if (bodyData) {
      req.write(bodyData);
    }
    req.end();
  });
}

async function main() {
  const logs = [];
  const startTime = Date.now();
  let config;
  const workspaceDir = process.env.WORKSPACE_DIR || '.';

  try {
    const raw = fs.readFileSync(`${workspaceDir}/runtime.json`, 'utf8');
    config = JSON.parse(raw);
  } catch (e) {
    console.log(JSON.stringify({ status: 'error', logs: [`Failed to read runtime.json: ${e.message}`] }));
    process.exit(1);
  }

  const port = config.port || await getFreePort();
  const cmd = config.command;
  const health = config.health || {};
  const healthType = health.type || 'http';
  const healthPath = health.path || '/health';

  const env = Object.assign({}, process.env, { PORT: port });

  const dbProcesses = [];

  // 1. Redis
  if (config.redis) {
    logs.push("Starting in-memory Redis on port 6379...");
    env.REDIS_URL = "redis://127.0.0.1:6379";
    try {
      const rProc = spawn('redis-server', ['--port', '6379', '--save', ''], { stdio: 'ignore' });
      dbProcesses.push(rProc);
    } catch (e) {
      logs.push(`Failed to start Redis: ${e.message}`);
    }
  }

  // 2. SQLite
  const sqliteConfig = config.sqlite || {};
  const defaultSeedPath = path.join(workspaceDir, 'seed.sql');
  if (Object.keys(sqliteConfig).length > 0 || fs.existsSync(defaultSeedPath)) {
    const dbFile = sqliteConfig.db_file || 'db.sqlite';
    const seedFile = sqliteConfig.seed_file || 'seed.sql';
    const dbPath = `${workspaceDir}/${dbFile}`;
    
    env.DATABASE_URL = `sqlite:///${dbPath}`;

    if (fs.existsSync(dbPath)) {
      try { fs.unlinkSync(dbPath); } catch(e){}
    }

    if (seedFile) {
      const seedPath = `${workspaceDir}/${seedFile}`;
      logs.push(`Hydrating SQLite database from ${seedFile}...`);
      if (fs.existsSync(seedPath)) {
        try {
          const sqliteProc = spawn('sqlite3', [dbPath]);
          const seedContent = fs.readFileSync(seedPath);
          sqliteProc.stdin.write(seedContent);
          sqliteProc.stdin.end();
          // wait synchronously via a simple loop or just let it finish. 
          // For simplicity in a script, we can use spawnSync instead
          const { spawnSync } = require('child_process');
          const res = spawnSync('sqlite3', [dbPath], { input: seedContent });
          if (res.status !== 0) {
            logs.push(`Warning: SQLite seed failed: ${res.stderr.toString()}`);
          }
        } catch (e) {
          logs.push(`Warning: SQLite seed failed: ${e.message}`);
        }
      } else {
        logs.push(`Warning: SQLite seed file ${seedFile} not found.`);
      }
    }
  }

  logs.push(`Starting server with PORT=${port}...`);

  const serverProcess = spawn(cmd[0], cmd.slice(1), {
    env: env,
    cwd: workspaceDir,
    stdio: 'pipe'
  });

  let stdoutStr = '';
  let stderrStr = '';
  serverProcess.stdout.on('data', d => stdoutStr += d.toString());
  serverProcess.stderr.on('data', d => stderrStr += d.toString());

  let processExited = false;
  let exitCode = null;
  serverProcess.on('exit', (code) => {
    processExited = true;
    exitCode = code;
  });

  let isReady = false;
  for (let i = 0; i < 50; i++) {
    if (processExited) break;
    
    if (healthType === 'tcp') {
      isReady = await checkTcp(port);
    } else {
      isReady = await checkHttp(port, healthPath);
    }

    if (isReady) break;
    await delay(100);
  }

  const startupTime = Date.now() - startTime;

  if (!isReady) {
    serverProcess.kill();
    for (const p of dbProcesses) {
      try { p.kill(); } catch(e){}
    }
    logs.push(`Server failed to start or pass health check within 5 seconds.`);
    console.log(JSON.stringify({
      status: 'error',
      startupTime: startupTime,
      stdout: stdoutStr.split('\n'),
      stderr: stderrStr.split('\n'),
      logs: logs,
      exitCode: exitCode
    }));
    process.exit(1);
  }

  logs.push(`Server ready in ${startupTime}ms.`);

  let requests = [];
  try {
    const rawRequests = fs.readFileSync(`${workspaceDir}/stdin.txt`, 'utf8');
    if (rawRequests.trim()) {
      requests = JSON.parse(rawRequests);
    }
  } catch (e) {
    logs.push(`Warning: Failed to parse stdin.txt requests: ${e.message}`);
  }

  const responses = [];
  for (const req of requests) {
    responses.push(await makeRequest(port, req));
  }

  serverProcess.kill();
  
  // Wait slightly for exit
  for(let i=0; i<10; i++) {
    if (processExited) break;
    await delay(100);
  }

  for (const p of dbProcesses) {
    try { p.kill(); } catch(e){}
  }

  console.log(JSON.stringify({
    status: 'success',
    startupTime: startupTime,
    responses: responses,
    stdout: stdoutStr.split('\n').filter(Boolean),
    stderr: stderrStr.split('\n').filter(Boolean),
    logs: logs,
    exitCode: exitCode || 0
  }));
}

main().catch(e => {
  console.log(JSON.stringify({ status: 'error', logs: [e.message] }));
  process.exit(1);
});
