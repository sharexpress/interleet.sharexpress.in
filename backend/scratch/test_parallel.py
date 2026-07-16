# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://interleet-backend.sharexpress.in/"

def make_request(request_id):
    start_time = time.perf_counter()
    try:
        req = urllib.request.Request(
            URL, 
            headers={"User-Agent": "Interleet-Parallel-Tester/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            port = data.get("port")
            elapsed = time.perf_counter() - start_time
            return {"id": request_id, "success": True, "port": port, "time": elapsed}
    except Exception as e:
        elapsed = time.perf_counter() - start_time
        return {"id": request_id, "success": False, "error": str(e), "time": elapsed}

def run_parallel_test(concurrency=16):
    print(f"🚀 Triggering {concurrency} concurrent requests to {URL}...")
    
    start_total = time.perf_counter()
    results = []
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {executor.submit(make_request, i): i for i in range(concurrency)}
        for future in as_completed(futures):
            results.append(future.result())
            
    total_duration = time.perf_counter() - start_total
    
    # ─── Process Results ───
    port_counts = {}
    successes = 0
    failures = 0
    
    print("\nDetailed Request Breakdown:")
    print("-" * 60)
    print(f"{'Req ID':<10} | {'Status':<10} | {'Port':<10} | {'Duration (ms)':<15}")
    print("-" * 60)
    
    for r in sorted(results, key=lambda x: x["id"]):
        if r["success"]:
            successes += 1
            port = r["port"]
            port_counts[port] = port_counts.get(port, 0) + 1
            status_str = "SUCCESS"
            port_str = str(port)
        else:
            failures += 1
            status_str = "FAILED"
            port_str = "N/A"
            
        print(f"{r['id']:<10} | {status_str:<10} | {port_str:<10} | {r['time']*1000:<15.2f}")
        
    print("-" * 60)
    print("\nLoad Balancer Port Distribution Summary:")
    print("=" * 40)
    for port, count in sorted(port_counts.items()):
        percentage = (count / successes) * 100 if successes > 0 else 0
        print(f"Port {port}: {count} requests ({percentage:.1f}%)")
    print("=" * 40)
    
    print(f"\nTest Summary:")
    print(f"  * Total Concurrent Requests: {concurrency}")
    print(f"  * Successful Responses:      {successes}")
    print(f"  * Failed Responses:          {failures}")
    print(f"  * Total Execution Time:      {total_duration:.4f}s")
    print("=" * 40)

if __name__ == "__main__":
    run_parallel_test()
