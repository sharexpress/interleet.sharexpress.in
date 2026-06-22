import asyncio
import time
import os
from dotenv import load_dotenv

# Load env from backend
load_dotenv("/Users/santushtkotai/Desktop/interleet/backend/.env")

import sys
sys.path.append("/Users/santushtkotai/Desktop/interleet/backend")

from app.core.db import get_db, db as raw_db

async def run_benchmark():
    cached_db = get_db()
    
    iterations = 200
    print(f"Starting list query benchmark (problems collection, {iterations} iterations)...")
    
    # ─── 1. Benchmark MongoDB (Direct) ───
    print("\n[Direct MongoDB] Running lookups...")
    start_direct = time.perf_counter()
    for _ in range(iterations):
        res = await raw_db.problems.find({}).to_list(length=100)
        _ = len(res)
    end_direct = time.perf_counter()
    time_direct = end_direct - start_direct
    avg_direct = (time_direct / iterations) * 1000  # in ms
    print(f"Direct MongoDB: Total Time = {time_direct:.4f}s | Avg Query Time = {avg_direct:.4f}ms")
    
    # ─── 2. Warm up the Redis Cache ───
    await cached_db.problems.find({}).to_list(length=100)
    
    # ─── 3. Benchmark Redis Cache (Hits) ───
    print("\n[Redis Cache Proxied] Running lookups...")
    start_cached = time.perf_counter()
    for _ in range(iterations):
        res = await cached_db.problems.find({}).to_list(length=100)
        _ = len(res)
    end_cached = time.perf_counter()
    time_cached = end_cached - start_cached
    avg_cached = (time_cached / iterations) * 1000  # in ms
    print(f"Redis Cached: Total Time = {time_cached:.4f}s | Avg Query Time = {avg_cached:.4f}ms")
    
    # ─── 4. Comparison Summary ───
    speedup = time_direct / time_cached
    percent_improvement = ((time_direct - time_cached) / time_direct) * 100
    
    print("\n" + "="*50)
    print("BENCHMARK COMPARISON SUMMARY")
    print("="*50)
    print(f"Direct MongoDB Latency: {avg_direct:.4f} ms")
    print(f"Redis Cache Latency:    {avg_cached:.4f} ms")
    print(f"Latency Reduction:      {avg_direct - avg_cached:.4f} ms ({percent_improvement:.2f}%)")
    print(f"Performance Speedup:    {speedup:.2f}x FASTER with Redis!")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
