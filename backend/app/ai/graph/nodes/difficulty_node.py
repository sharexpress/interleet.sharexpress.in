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

from app.ai.graph.state import InterviewState


_DIFFICULTY_ORDER = ["easy", "medium", "hard", "staff"]


async def difficulty_node(state: InterviewState):
    evaluation = state.get("last_evaluation") or {}
    current = state.get("difficulty", "easy")
    index = _DIFFICULTY_ORDER.index(current) if current in _DIFFICULTY_ORDER else 0
    score = float(evaluation.get("score", 0.0))
    threshold = float(state.get("threshold_score", 7.0))

    # Check active tree node recommendation
    tree_nodes = state.get("tree_nodes", [])
    active_id = state.get("active_node_id", "")
    active_node = next((n for n in tree_nodes if n.get("id") == active_id), None)
    
    if active_node and active_node.get("difficulty"):
        rec_diff = active_node["difficulty"].lower()
        if rec_diff in _DIFFICULTY_ORDER:
            rec_idx = _DIFFICULTY_ORDER.index(rec_diff)
            # Use active node difficulty as baseline
            index = max(index, rec_idx)

    # Adaptive progression based on score vs threshold
    if score >= threshold + 0.5 and index < len(_DIFFICULTY_ORDER) - 1:
        index += 1
    elif score < 4.5 and index > 0:
        index -= 1

    return {
        "difficulty": _DIFFICULTY_ORDER[index],
        "current_tree_depth": index,
    }
