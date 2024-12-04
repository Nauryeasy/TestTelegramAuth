from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseUseCase(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...
