from uuid import uuid4

from pydantic import BaseModel, Field


class TestCaseModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    problem_slug: str
    name: str
    stdin: str = ""
    expected_output: str = ""
    hidden: bool = False
    weight: float = 1.0
    time_limit: float | None = None
    memory_limit: int | None = None
