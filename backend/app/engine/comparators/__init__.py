"""
Interleet Judge Engine — Custom Comparators Registry
Allows registering custom validation functions by problem slug.
"""

from typing import Callable, Dict, Optional

# Registry maps problem_slug -> comparator function
# Function signature: (actual: str, expected: str) -> bool
CUSTOM_COMPARATORS: Dict[str, Callable[[str, str], bool]] = {}


def register_comparator(slug: str):
    """Decorator to register a custom comparator for a problem slug."""
    def decorator(func: Callable[[str, str], bool]):
        CUSTOM_COMPARATORS[slug] = func
        return func
    return decorator


def get_custom_comparator(slug: str) -> Optional[Callable[[str, str], bool]]:
    """Retrieve a custom comparator by slug, if registered."""
    return CUSTOM_COMPARATORS.get(slug)


# ─── Example / Pre-configured custom comparators ────────────────────────────

@register_comparator("build-a-rate-limiter")
def compare_rate_limiter(actual: str, expected: str) -> bool:
    """
    Rate limiter output might have timing variations.
    We compare line by line but ignore slight timing debug outputs
    and check actual allowed/denied sequence counts.
    """
    act_lines = [l.strip().lower() for l in actual.splitlines() if l.strip()]
    exp_lines = [l.strip().lower() for l in expected.splitlines() if l.strip()]

    # Filter out timer / wait lines from comparison
    act_filtered = [l for l in act_lines if not l.startswith("[waiting") and not l.startswith("✓ run")]
    exp_filtered = [l for l in exp_lines if not l.startswith("[waiting") and not l.startswith("✓ run")]

    return act_filtered == exp_filtered
