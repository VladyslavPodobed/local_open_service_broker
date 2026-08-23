from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    success: bool
    return_value: Any | None = None
    error: str | None = None
