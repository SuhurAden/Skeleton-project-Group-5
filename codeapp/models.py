from __future__ import annotations

# python built-in imports
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Jobs:
    title: str
    company: str
    location: str
    position_type: str
    job_description: str
    salary: float
    identified_skills: list[str]
