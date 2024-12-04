from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseCacheRepository(ABC):

    @abstractmethod
    def set_value(self, key, value, duration) -> None:
        ...

    @abstractmethod
    def get_value(self, key) -> Any:
        ...

    @abstractmethod
    def delete_value(self, key) -> None:
        ...
