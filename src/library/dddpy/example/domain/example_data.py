from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateExampleData:
    code: str
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class UpdateExampleData:
    name: Optional[str] = None
    description: Optional[str] = None
