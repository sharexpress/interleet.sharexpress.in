# Copyright 2026 Sharexpress Contributors
# SQL Comprehensive Curriculum Package (53 Challenges across 5 Modules)

from sql_curriculum.module1_basic_commands import MODULE1_CHALLENGES
from sql_curriculum.module2_aggregates_codechef import MODULE2_CHALLENGES
from sql_curriculum.module3_joins_cab_booking import MODULE3_CHALLENGES
from sql_curriculum.module4_subqueries_rental import MODULE4_CHALLENGES
from sql_curriculum.module5_case_library import MODULE5_CHALLENGES

ALL_SQL_CHALLENGES = (
    MODULE1_CHALLENGES +
    MODULE2_CHALLENGES +
    MODULE3_CHALLENGES +
    MODULE4_CHALLENGES +
    MODULE5_CHALLENGES
)

__all__ = [
    "MODULE1_CHALLENGES",
    "MODULE2_CHALLENGES",
    "MODULE3_CHALLENGES",
    "MODULE4_CHALLENGES",
    "MODULE5_CHALLENGES",
    "ALL_SQL_CHALLENGES",
]
