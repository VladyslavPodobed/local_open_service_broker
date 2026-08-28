from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar('T')


@dataclass
class Success(Generic[T]):
    return_value: T | None = None


@dataclass
class Failure(Generic[T]):
    error_description: str = ""
