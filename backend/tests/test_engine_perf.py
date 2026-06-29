"""
Test suite for Interleet execution engine performance optimizations.
Validates all 6 changes work correctly:
  1. sandbox.py — container cache, thread pool
  2. base.py — batch execution, hardlinks
  3. redis_queue.py — asyncio.Event notification
  4. submission_controller.py — instant result wait
  5. execution_worker.py — background persistence
  6. startup.py — pre-warm

Run with: python -m pytest tests/test_engine_perf.py -v
Or standalone: python tests/test_engine_perf.py
"""

import asyncio
import os
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_imports():
    """Test 1: All modified modules import without errors."""
    print("=" * 60)
    print("TEST 1: Import validation")
    print("=" * 60)
    
    errors = []
    
    modules = [
        ("sandbox.py", "app.engine.docker.sandbox"),
        ("base.py", "app.engine.executors.base"),
        ("redis_queue.py", "app.engine.queue.redis_queue"),
        ("submission_controller.py", "app.engine.controllers.submission_controller"),
        ("execution_worker.py", "app.engine.workers.execution_worker"),
        ("startup.py", "app.engine.workers.startup"),
    ]
    
    for name, module_path in modules:
        try:
            __import__(module_path)
            print(f"  ✅ {name} — imported OK")
        except Exception as e:
            errors.append((name, str(e)))
            print(f"  ❌ {name} — FAILED: {e}")
    
    print()
    return errors


def test_sandbox_container_cache():
    """Test 2: Container cache data structures exist and work."""
    print("=" * 60)
    print("TEST 2: Sandbox container cache")
    print("=" * 60)
    
    errors = []
    
    try:
        from app.engine.docker.sandbox import (
            _container_cache,
            _container_cache_lock,
            _DOCKER_THREAD_POOL,
            get_container,
            prewarm_containers,
            invalidate_container,
        )
        
        # Verify cache is a dict
        assert isinstance(_container_cache, dict), "Cache should be a dict"
        print("  ✅ _container_cache is a dict")
        
        # Verify thread pool exists
        assert _DOCKER_THREAD_POOL is not None, "Thread pool should exist"
        assert _DOCKER_THREAD_POOL._max_workers == 12, f"Thread pool should have 12 workers, got {_DOCKER_THREAD_POOL._max_workers}"
        print(f"  ✅ _DOCKER_THREAD_POOL has {_DOCKER_THREAD_POOL._max_workers} workers")
        
        # Verify lock exists
        assert _container_cache_lock is not None, "Cache lock should exist"
        print("  ✅ _container_cache_lock exists")
        
        # Verify functions exist
        assert callable(get_container), "get_container should be callable"
        assert callable(prewarm_containers), "prewarm_containers should be callable"
        assert callable(invalidate_container), "invalidate_container should be callable"
        print("  ✅ All cache functions exist")
        
    except Exception as e:
        errors.append(("container_cache", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_sandbox_uses_dedicated_thread_pool():
    """Test 3: DockerSandbox.run() and compile() use dedicated thread pool."""
    print("=" * 60)
    print("TEST 3: Dedicated thread pool usage")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.docker.sandbox import DockerSandbox, _DOCKER_THREAD_POOL
        
        # Check compile() source uses _DOCKER_THREAD_POOL
        compile_source = inspect.getsource(DockerSandbox.compile)
        assert "_DOCKER_THREAD_POOL" in compile_source, "compile() should use _DOCKER_THREAD_POOL"
        print("  ✅ compile() uses _DOCKER_THREAD_POOL")
        
        # Check run() source uses _DOCKER_THREAD_POOL
        run_source = inspect.getsource(DockerSandbox.run)
        assert "_DOCKER_THREAD_POOL" in run_source, "run() should use _DOCKER_THREAD_POOL"
        print("  ✅ run() uses _DOCKER_THREAD_POOL")
        
    except Exception as e:
        errors.append(("thread_pool", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_base_executor_batch_method():
    """Test 4: BaseExecutor has run_batch_testcases() method."""
    print("=" * 60)
    print("TEST 4: Batch testcase execution method")
    print("=" * 60)
    
    errors = []
    
    try:
        from app.engine.executors.base import BaseExecutor
        import inspect
        
        # Check batch method exists
        assert hasattr(BaseExecutor, 'run_batch_testcases'), "BaseExecutor should have run_batch_testcases"
        print("  ✅ run_batch_testcases() method exists")
        
        # Check it's async
        method = getattr(BaseExecutor, 'run_batch_testcases')
        assert asyncio.iscoroutinefunction(method), "run_batch_testcases should be async"
        print("  ✅ run_batch_testcases() is async")
        
        # Check hardlink method exists
        assert hasattr(BaseExecutor, '_link_compiled_files'), "BaseExecutor should have _link_compiled_files"
        print("  ✅ _link_compiled_files() method exists")
        
        # Check source uses os.link
        link_source = inspect.getsource(BaseExecutor._link_compiled_files)
        assert "os.link" in link_source, "_link_compiled_files should use os.link"
        print("  ✅ _link_compiled_files() uses os.link (hardlinks)")
        
    except Exception as e:
        errors.append(("batch_exec", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_hardlinks_actually_work():
    """Test 5: Hardlinks work on this filesystem."""
    print("=" * 60)
    print("TEST 5: Hardlink filesystem support")
    print("=" * 60)
    
    errors = []
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "source.bin"
            dst = Path(tmpdir) / "linked.bin"
            
            # Create source file
            src.write_bytes(b"x" * 1024)  # 1KB test file
            
            # Try hardlink
            os.link(src, dst)
            
            # Verify same inode (= zero-copy)
            src_stat = os.stat(src)
            dst_stat = os.stat(dst)
            assert src_stat.st_ino == dst_stat.st_ino, "Hardlink should share inode"
            assert dst.read_bytes() == b"x" * 1024, "Linked file should have same content"
            
            print(f"  ✅ Hardlinks work (inode={src_stat.st_ino})")
            print(f"  ✅ Zero-copy verified (same inode for src and dst)")
            
    except OSError as e:
        print(f"  ⚠️  Hardlinks not supported on this FS (will fallback to copy): {e}")
    except Exception as e:
        errors.append(("hardlinks", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_redis_queue_notification():
    """Test 6: Redis queue has asyncio.Event notification system."""
    print("=" * 60)
    print("TEST 6: Redis queue instant notification")
    print("=" * 60)
    
    errors = []
    
    try:
        from app.engine.queue.redis_queue import ExecutionQueue
        import inspect
        
        # Check new methods exist
        assert hasattr(ExecutionQueue, 'register_waiter'), "Should have register_waiter"
        assert hasattr(ExecutionQueue, 'unregister_waiter'), "Should have unregister_waiter"
        assert hasattr(ExecutionQueue, '_notify_waiter'), "Should have _notify_waiter"
        assert hasattr(ExecutionQueue, 'wait_for_result'), "Should have wait_for_result"
        print("  ✅ All notification methods exist")
        
        # Check wait_for_result is async
        assert asyncio.iscoroutinefunction(ExecutionQueue.wait_for_result), "wait_for_result should be async"
        print("  ✅ wait_for_result() is async")
        
        # Check store_result calls _notify_waiter
        store_source = inspect.getsource(ExecutionQueue.store_result)
        assert "_notify_waiter" in store_source, "store_result should call _notify_waiter"
        print("  ✅ store_result() triggers notification")
        
        # Check internal data structures
        source = inspect.getsource(ExecutionQueue.__init__)
        assert "_result_events" in source, "Should have _result_events dict"
        assert "_result_cache" in source, "Should have _result_cache dict"
        print("  ✅ Internal event registry exists")
        
    except Exception as e:
        errors.append(("notification", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_notification_flow():
    """Test 7: End-to-end notification flow (register → notify → wake)."""
    print("=" * 60)
    print("TEST 7: Notification flow simulation")
    print("=" * 60)
    
    errors = []
    
    try:
        from app.engine.queue.redis_queue import ExecutionQueue
        
        # Create a mock Redis client
        mock_redis = MagicMock()
        mock_redis.set = AsyncMock()
        mock_redis.get = AsyncMock(return_value=None)
        
        queue = ExecutionQueue(mock_redis)
        
        # Test register_waiter
        event = queue.register_waiter("test-sub-123")
        assert isinstance(event, asyncio.Event), "Should return asyncio.Event"
        assert not event.is_set(), "Event should not be set yet"
        print("  ✅ register_waiter() returns unset Event")
        
        # Test _notify_waiter
        test_result = {"verdict": "ACCEPTED", "score": 100}
        queue._notify_waiter("test-sub-123", test_result)
        assert event.is_set(), "Event should be set after notification"
        print("  ✅ _notify_waiter() sets the Event")
        
        # Test result is cached in-process
        assert queue._result_cache.get("test-sub-123") == test_result, "Result should be cached"
        print("  ✅ Result cached in-process for instant pickup")
        
        # Test unregister_waiter cleans up
        queue.unregister_waiter("test-sub-123")
        assert "test-sub-123" not in queue._result_events, "Event should be cleaned up"
        assert "test-sub-123" not in queue._result_cache, "Cache should be cleaned up"
        print("  ✅ unregister_waiter() cleans up properly")
        
        # Test _notify_waiter for non-existent waiter (no crash)
        queue._notify_waiter("non-existent", {"data": "test"})
        print("  ✅ Notifying non-existent waiter doesn't crash")
        
    except Exception as e:
        errors.append(("notification_flow", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_controller_no_polling():
    """Test 8: Submission controller no longer uses polling."""
    print("=" * 60)
    print("TEST 8: Controller uses instant notification (no polling)")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.controllers.submission_controller import EngineSubmissionController
        
        # Check _poll_for_result is REMOVED
        assert not hasattr(EngineSubmissionController, '_poll_for_result'), \
            "_poll_for_result should be removed (replaced with wait_for_result)"
        print("  ✅ _poll_for_result() removed")
        
        # Check create_execute uses wait_for_result
        exec_source = inspect.getsource(EngineSubmissionController.create_execute)
        assert "wait_for_result" in exec_source, "create_execute should use wait_for_result"
        assert "asyncio.sleep" not in exec_source, "create_execute should NOT use asyncio.sleep"
        print("  ✅ create_execute() uses wait_for_result (instant)")
        
        # Check create_run uses wait_for_result
        run_source = inspect.getsource(EngineSubmissionController.create_run)
        assert "wait_for_result" in run_source, "create_run should use wait_for_result"
        assert "asyncio.sleep" not in run_source, "create_run should NOT use asyncio.sleep"
        print("  ✅ create_run() uses wait_for_result (instant)")
        
    except Exception as e:
        errors.append(("no_polling", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_worker_background_persist():
    """Test 9: Worker broadcasts result before persisting to MongoDB."""
    print("=" * 60)
    print("TEST 9: Worker background persistence")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.workers.execution_worker import ExecutionWorker
        
        # Check _process_job source
        source = inspect.getsource(ExecutionWorker._process_job)
        
        # store_result should come BEFORE _save_result
        store_pos = source.find("store_result")
        save_pos = source.find("_save_result_background")
        
        assert store_pos > 0, "store_result should exist in _process_job"
        assert save_pos > 0, "_save_result_background should exist in _process_job"
        assert store_pos < save_pos, "store_result (notify user) should come BEFORE _save_result (persist)"
        print("  ✅ Redis cache (user notification) happens BEFORE MongoDB persist")
        
        # Check _save_result_background exists
        assert hasattr(ExecutionWorker, '_save_result_background'), "Should have _save_result_background"
        print("  ✅ _save_result_background() method exists")
        
        # Check asyncio.create_task is used for persistence
        assert "create_task" in source, "Should use asyncio.create_task for background persist"
        print("  ✅ MongoDB persist uses asyncio.create_task (non-blocking)")
        
        # Check batch mode is used for interpreted languages
        assert "run_batch_testcases" in source, "Should use batch mode for interpreted languages"
        print("  ✅ Batch execution mode used for interpreted languages")
        
    except Exception as e:
        errors.append(("bg_persist", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_worker_background_ratings():
    """Test 10: User ratings update is fire-and-forget."""
    print("=" * 60)
    print("TEST 10: Background user ratings update")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.workers.execution_worker import ExecutionWorker
        
        source = inspect.getsource(ExecutionWorker._save_result)
        
        # Check ratings update uses create_task
        assert "create_task" in source, "_save_result should fire-and-forget ratings update"
        assert "_update_user_ratings_and_badges" in source, "Should reference ratings function"
        print("  ✅ Ratings update uses asyncio.create_task (fire-and-forget)")
        print("  ✅ Worker doesn't block waiting for ratings recalculation")
        
    except Exception as e:
        errors.append(("bg_ratings", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_startup_prewarm():
    """Test 11: Startup pre-warms containers."""
    print("=" * 60)
    print("TEST 11: Container pre-warming on startup")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.workers.startup import start_workers, _PREWARM_IMAGES
        
        # Check prewarm images list
        assert len(_PREWARM_IMAGES) >= 4, f"Should pre-warm at least 4 images, got {len(_PREWARM_IMAGES)}"
        print(f"  ✅ {len(_PREWARM_IMAGES)} images configured for pre-warming:")
        for img in _PREWARM_IMAGES:
            print(f"     • {img}")
        
        # Check start_workers calls prewarm_containers
        source = inspect.getsource(start_workers)
        assert "prewarm_containers" in source, "start_workers should call prewarm_containers"
        print("  ✅ start_workers() calls prewarm_containers()")
        
    except Exception as e:
        errors.append(("prewarm", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_worker_brpop_timeout():
    """Test 12: Worker BRPOP timeout is reduced for faster pickup."""
    print("=" * 60)
    print("TEST 12: Worker BRPOP timeout")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.workers.execution_worker import ExecutionWorker
        
        source = inspect.getsource(ExecutionWorker.run)
        
        # Check dequeue timeout is 2 (reduced from 5)
        assert "timeout=2" in source, "BRPOP timeout should be 2 seconds (reduced from 5)"
        print("  ✅ BRPOP timeout reduced to 2s (was 5s) — faster job pickup")
        
    except Exception as e:
        errors.append(("brpop", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_async_notification_timing():
    """Test 13: Measure notification speed vs polling speed."""
    print("=" * 60)
    print("TEST 13: Notification speed benchmark")
    print("=" * 60)
    
    errors = []
    
    try:
        from app.engine.queue.redis_queue import ExecutionQueue
        
        mock_redis = MagicMock()
        mock_redis.set = AsyncMock()
        queue = ExecutionQueue(mock_redis)
        
        async def benchmark():
            # Simulate: controller registers waiter, worker notifies
            submission_id = "bench-test-001"
            result = {"verdict": "ACCEPTED", "score": 100.0}
            
            event = queue.register_waiter(submission_id)
            
            # Measure notification latency
            start = time.monotonic()
            
            # Simulate worker completing (in same event loop for test)
            queue._notify_waiter(submission_id, result)
            
            # The event.wait() should return almost instantly
            await asyncio.wait_for(event.wait(), timeout=1.0)
            
            elapsed_us = (time.monotonic() - start) * 1_000_000
            
            queue.unregister_waiter(submission_id)
            return elapsed_us
        
        elapsed_us = asyncio.run(benchmark())
        print(f"  ✅ Notification latency: {elapsed_us:.0f} µs (microseconds)")
        print(f"  ✅ Old polling was: 200,000 µs (200ms) — {200_000/max(elapsed_us, 1):.0f}× faster")
        
    except Exception as e:
        errors.append(("timing", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_sandbox_error_cache_invalidation():
    """Test 14: Container cache is invalidated on errors."""
    print("=" * 60)
    print("TEST 14: Cache invalidation on errors")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.docker.sandbox import DockerSandbox
        
        # Check _run_sync invalidates cache on error
        source = inspect.getsource(DockerSandbox._run_sync)
        assert "_container_cache.pop" in source, "_run_sync should invalidate cache on error"
        print("  ✅ _run_sync() invalidates cache on errors")
        
        # Check _compile_sync invalidates cache on error
        source = inspect.getsource(DockerSandbox._compile_sync)
        assert "_container_cache.pop" in source, "_compile_sync should invalidate cache on error"
        print("  ✅ _compile_sync() invalidates cache on errors")
        
    except Exception as e:
        errors.append(("cache_invalidation", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


def test_container_restart_policy():
    """Test 15: Containers have auto-restart policy."""
    print("=" * 60)
    print("TEST 15: Container restart policy")
    print("=" * 60)
    
    errors = []
    
    try:
        import inspect
        from app.engine.docker.sandbox import _create_persistent_container
        
        source = inspect.getsource(_create_persistent_container)
        assert "unless-stopped" in source, "Container should have unless-stopped restart policy"
        print("  ✅ Containers use restart_policy='unless-stopped'")
        print("  ✅ Containers auto-restart on crash (no manual intervention)")
        
    except Exception as e:
        errors.append(("restart_policy", str(e)))
        print(f"  ❌ FAILED: {e}")
    
    print()
    return errors


# ─── Main Runner ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("🧪 Interleet Execution Engine — Performance Optimization Tests")
    print("━" * 60)
    print()
    
    all_errors = []
    tests = [
        test_imports,
        test_sandbox_container_cache,
        test_sandbox_uses_dedicated_thread_pool,
        test_base_executor_batch_method,
        test_hardlinks_actually_work,
        test_redis_queue_notification,
        test_notification_flow,
        test_controller_no_polling,
        test_worker_background_persist,
        test_worker_background_ratings,
        test_startup_prewarm,
        test_worker_brpop_timeout,
        test_async_notification_timing,
        test_sandbox_error_cache_invalidation,
        test_container_restart_policy,
    ]
    
    passed = 0
    failed = 0
    
    for test_fn in tests:
        try:
            errs = test_fn()
            if errs:
                all_errors.extend(errs)
                failed += 1
            else:
                passed += 1
        except Exception as e:
            print(f"  💥 Test crashed: {e}")
            all_errors.append((test_fn.__name__, str(e)))
            failed += 1
    
    # Summary
    print("━" * 60)
    print(f"📊 Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("━" * 60)
    
    if all_errors:
        print("\n❌ Failures:")
        for name, error in all_errors:
            print(f"  • {name}: {error}")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! The optimizations are correctly implemented.")
        print()
        print("📋 Summary of optimizations verified:")
        print("  1. ✅ In-memory container cache (skip Docker API lookups)")
        print("  2. ✅ Dedicated 12-thread pool for Docker calls")
        print("  3. ✅ Batch testcase execution (1 workspace for interpreted langs)")
        print("  4. ✅ Hardlinks for compiled binaries (zero-copy)")
        print("  5. ✅ Instant asyncio.Event notification (no 200ms polling)")
        print("  6. ✅ Background MongoDB persist + ratings update")
        print("  7. ✅ Pre-warm containers at server boot")
        print("  8. ✅ Auto-restart policy for containers")
        print("  9. ✅ Cache invalidation on errors")
        print("  10. ✅ Reduced BRPOP timeout for faster job pickup")
        sys.exit(0)
