"""
Interleet Challenge Validation Framework
Ensures challenge quality through coverage analysis, mutation testing,
test generation, and differential testing.
"""

from app.engine.validation.coverage_analyzer import CoverageAnalyzer
from app.engine.validation.quality_gate import QualityGate

__all__ = ["CoverageAnalyzer", "QualityGate"]
