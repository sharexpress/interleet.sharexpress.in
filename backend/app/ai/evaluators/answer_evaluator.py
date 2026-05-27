def evaluate_answer(answer: str, expected_keywords: list):
    score = 0
    matched_keywords = []
    answer_lower = answer.lower()
    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            score += 1
            matched_keywords.append(keyword)
    final_score = round((score / len(expected_keywords)) * 10, 2)
    return {
        "score": final_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": list(set(expected_keywords) - set(matched_keywords)),
    }
