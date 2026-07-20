from pydantic import BaseModel, Field
from app.ai.graph.state import InterviewState, TreeNodeState


class ExtractedTreeTopic(BaseModel):
    topic: str
    difficulty: str = "easy"
    category: str = "technical"


class ExtractedTreeSchema(BaseModel):
    topics: list[ExtractedTreeTopic] = Field(default_factory=list)


async def context_node(state: InterviewState):
    topic    = state.get("current_topic") or state.get("last_answer_topic", "")
    is_intro = topic == "self_introduction"

    # ── Append the completed turn ─────────────────────────────────────────────
    last_eval = state.get("last_evaluation") or {}
    turn = {
        "question":   state.get("current_question", ""),
        "answer":     state.get("last_answer", ""),
        "topic":      topic,
        "difficulty": state.get("difficulty", "easy"),
        "evaluation": {} if is_intro else last_eval,
    }
    turns = [*state.get("turns", []), turn]

    target_topics = list(state.get("target_topics", []))
    covered_topics = list(state.get("covered_topics", []))
    weak_topics = list(state.get("weak_topics", []))
    tree_nodes: list[TreeNodeState] = [dict(n) for n in state.get("tree_nodes", [])]
    active_node_id = state.get("active_node_id", "")
    threshold = float(state.get("threshold_score", 7.0))

    if is_intro:
        # Construct initial dynamic decision tree from candidate's introduction
        tree_nodes, target_topics = await _build_dynamic_decision_tree(state, state.get("last_answer", ""))
        active_node_id = tree_nodes[1]["id"] if len(tree_nodes) > 1 else tree_nodes[0]["id"]
    else:
        # Update active tree node status based on evaluation threshold
        score = float(last_eval.get("score", 0.0))
        if active_node_id:
            for node in tree_nodes:
                if node["id"] == active_node_id:
                    node["depth_score"] = score
                    if score >= threshold:
                        node["status"] = "mastered"
                    elif score < 4.5:
                        node["status"] = "weak"
                        if topic and topic not in weak_topics:
                            weak_topics.append(topic)
                    else:
                        node["status"] = "probing"
                    break

        # If high performance (score >= threshold), dynamically spawn deeper sub-topic node
        if score >= threshold and len(tree_nodes) < 25:
            last_ans = state.get("last_answer", "")
            sub_topic = _extract_sub_technology(last_ans, topic)
            if sub_topic and not any(n["topic"].lower() == sub_topic.lower() for n in tree_nodes):
                new_id = f"node_{len(tree_nodes)}"
                next_diff = "hard" if score >= 8.5 else "medium"
                tree_nodes.append({
                    "id": new_id,
                    "topic": sub_topic,
                    "difficulty": next_diff,
                    "status": "unvisited",
                    "depth_score": 0.0,
                    "parent_id": active_node_id,
                    "category": "deep_probing",
                })
                target_topics.append(sub_topic)

        # Update covered topics
        for matched in _detect_covered_topics(state, topic):
            if matched not in covered_topics:
                covered_topics.append(matched)

        # Select next unvisited/probing node in tree
        unvisited = [n for n in tree_nodes if n.get("status") in ("unvisited", "probing") and n["topic"] != "self_introduction"]
        if unvisited:
            active_node_id = unvisited[0]["id"]

    remaining_topics = [
        t for t in target_topics
        if t not in covered_topics
    ]

    interview_phase = (
        "adaptive_questions"
        if is_intro
        else state.get("interview_phase", "adaptive_questions")
    )

    return {
        "turns":                  turns,
        "target_topics":          target_topics,
        "tree_nodes":             tree_nodes,
        "active_node_id":         active_node_id,
        "covered_topics":         covered_topics,
        "remaining_topics":       remaining_topics,
        "weak_topics":            weak_topics,
        "candidate_introduction": state.get("last_answer", "")
                                  if is_intro
                                  else state.get("candidate_introduction", ""),
        "interview_phase":        interview_phase,
        # Clear transient fields
        "last_answer":       "",
        "last_answer_topic": "",
    }


def _detect_covered_topics(state: InterviewState, generated_topic: str) -> list[str]:
    target_topics = state.get("target_topics", [])
    haystack = " ".join([
        generated_topic,
        state.get("current_question", ""),
        state.get("last_answer", ""),
    ]).lower()

    matched = [
        t for t in target_topics
        if t.lower() in haystack or haystack in t.lower()
    ]
    return matched if matched else ([generated_topic] if generated_topic else [])


def _extract_sub_technology(text: str, parent_topic: str) -> str | None:
    import re
    # Match technical terms or frameworks mentioned in text
    candidates = re.findall(r'\b[A-Z][a-zA-Z0-9\+\#\.\-]{2,}\b', text)
    stopwords = {"I", "The", "This", "My", "We", "And", "For", "With", "Using", "From", "Also"}
    for cand in candidates:
        if cand not in stopwords and cand.lower() not in parent_topic.lower() and len(cand) > 3:
            return f"{parent_topic}: {cand} Integration"
    return None


async def _build_dynamic_decision_tree(state: InterviewState, intro_text: str) -> tuple[list[TreeNodeState], list[str]]:
    from app.ai.prompts.system_prompt import INTRO_TOPICS_PROMPT
    from app.ai.services.ai_client import ai_client

    user_prompt = f"""
Role: {state.get("role", "")}
Interview type: {state.get("interview_type", "")}
JD Context: {(state.get("jd") or "")[:1000]}
Skills context: {state.get("skills", [])}
Candidate Self-Introduction:
{intro_text}
"""
    nodes: list[TreeNodeState] = [
        {
            "id": "node_0",
            "topic": "self_introduction",
            "difficulty": "easy",
            "status": "mastered",
            "depth_score": 10.0,
            "parent_id": None,
            "category": "warmup",
        }
    ]
    target_topics: list[str] = []

    try:
        res = await ai_client.generate_json(
            system=INTRO_TOPICS_PROMPT + "\nReturn 5-7 structured topic nodes matching candidate's introduction and role requirements.",
            user=user_prompt,
            schema=ExtractedTreeSchema,
            temperature=0.3,
        )
        if res.topics:
            for idx, item in enumerate(res.topics, start=1):
                clean_topic = item.topic.strip()
                if clean_topic:
                    nodes.append({
                        "id": f"node_{idx}",
                        "topic": clean_topic,
                        "difficulty": item.difficulty or "easy",
                        "status": "unvisited",
                        "depth_score": 0.0,
                        "parent_id": "node_0",
                        "category": item.category or "technical",
                    })
                    target_topics.append(clean_topic)
            return nodes, target_topics
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning(f"[context_node] Dynamic tree generation fallback: {exc}")

    # Fallback if LLM fails or returns empty
    fallback_topics = state.get("target_topics", ["Core Fundamentals", "Architecture & Projects", "Problem Solving"])
    for idx, t in enumerate(fallback_topics, start=1):
        nodes.append({
            "id": f"node_{idx}",
            "topic": t,
            "difficulty": "easy" if idx == 1 else "medium",
            "status": "unvisited",
            "depth_score": 0.0,
            "parent_id": "node_0",
            "category": "technical",
        })
        target_topics.append(t)

    return nodes, target_topics
