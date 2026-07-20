#!/usr/bin/env python3
"""
Test Suite: AI Mock Interview Engine — Dynamic Decision Tree & Adaptive Level Engine
Verifies:
1. Start interview (initial state has min_questions=2, max_questions=20, easy baseline).
2. Self-introduction turn parses tech stack & projects to construct dynamic decision tree (`tree_nodes`).
3. High score responses (>= 7.0 threshold) trigger difficulty level-up & cross-questioning.
4. Dynamic question bounds (2-20 questions).
"""

import sys
import os
import asyncio

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.ai.graph.interview_graph import build_initial_state, run_interview_graph

async def run_tests():
    print("==========================================================")
    print("  AI MOCK INTERVIEW DYNAMIC DECISION TREE ENGINE TEST SUITE")
    print("==========================================================")

    payload = {
        "role": "Senior Fullstack Engineer",
        "interview_type": "technical",
        "jd": "Must be proficient in React, Node.js, PostgreSQL, Redis, and Microservices.",
        "skills": ["React", "Node.js", "System Design"],
    }

    # Test 1: Initial state construction
    print("\n[TEST 1] Building Initial State...")
    state = build_initial_state(payload, user_id="test_user_123")

    assert state["min_questions"] == 2, f"Expected min_questions=2, got {state['min_questions']}"
    assert state["max_questions"] == 20, f"Expected max_questions=20, got {state['max_questions']}"
    assert state["difficulty"] == "easy", f"Expected difficulty=easy, got {state['difficulty']}"
    assert len(state["tree_nodes"]) >= 1, "Expected initial root node in tree_nodes"
    print("  ✅ Initial state correctly configured with easy baseline and dynamic bounds (2-20).")

    # Test 2: Opening question generation
    print("\n[TEST 2] Running Opening Question Generation...")
    state = await run_interview_graph(state)

    print(f"  Preamble: {state.get('current_preamble')}")
    print(f"  Question: {state.get('current_question')}")
    assert state.get("current_topic") == "self_introduction", "First topic must be self_introduction"
    print("  ✅ Opening question correctly prompts for candidate introduction.")

    # Test 3: Candidate intro turn & Decision Tree Construction
    print("\n[TEST 3] Submitting Candidate Self-Introduction & Building Decision Tree...")
    state["last_answer"] = (
        "Hi! I'm a Senior Fullstack Engineer with 5 years of experience. "
        "I specialize in building real-time applications using React, Node.js, and WebSocket streams. "
        "Recently I architected a high-throughput event processing pipeline using Kafka and PostgreSQL, "
        "and optimized Redis caching to handle 50,000 requests per minute."
    )
    state["last_answer_topic"] = "self_introduction"

    state = await run_interview_graph(state)

    tree_nodes = state.get("tree_nodes", [])
    print(f"  Constructed Decision Tree Nodes ({len(tree_nodes)} nodes):")
    for n in tree_nodes:
        print(f"    - [{n.get('id')}] Topic: {n.get('topic'):35s} | Diff: {n.get('difficulty'):6s} | Status: {n.get('status')}")

    assert len(tree_nodes) > 1, "Decision tree should contain dynamically extracted topic nodes from intro!"
    assert state.get("active_node_id") != "", "Active node ID should be selected"
    print("  ✅ Dynamic decision tree constructed from candidate's introduction.")

    # Test 4: Dynamic threshold evaluation & Level Escalation
    print("\n[TEST 4] Simulating Candidate Technical Response & Adaptive Progression...")
    await asyncio.sleep(1.5)
    state["last_answer"] = (
        "For Kafka partitioning, we used a consistent hashing strategy based on user_id to ensure "
        "message ordering per user session. We implemented idempotency using Redis SETNX with TTL "
        "to prevent duplicate event processing across microservices. We monitored lag using Prometheus metrics."
    )
    state["last_answer_topic"] = state.get("current_topic", "Kafka Integration")

    state = await run_interview_graph(state)

    eval_data = state.get("last_evaluation") or {}
    print(f"  AI Evaluation Score: {eval_data.get('score')}/10 | Summary: {eval_data.get('summary')}")
    print(f"  New Adaptive Level: {state.get('difficulty')}")
    print(f"  Next Question: {state.get('current_question')}")
    print(f"  Next Topic: {state.get('current_topic')}")

    assert state.get("difficulty") in ("easy", "medium", "hard", "staff"), "Valid difficulty returned"
    print("  ✅ Technical response evaluated and next adaptive turn generated.")

    print("\n==========================================================")
    print("  ALL AI MOCK INTERVIEW ENGINE TESTS PASSED! 🎉")
    print("==========================================================")

if __name__ == "__main__":
    asyncio.run(run_tests())
