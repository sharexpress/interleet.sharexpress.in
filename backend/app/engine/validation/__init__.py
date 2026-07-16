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

"""
Interleet Challenge Validation Framework
Ensures challenge quality through coverage analysis, mutation testing,
test generation, and differential testing.
"""

from app.engine.validation.coverage_analyzer import CoverageAnalyzer
from app.engine.validation.quality_gate import QualityGate

__all__ = ["CoverageAnalyzer", "QualityGate"]
