from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseConsumer(ABC):

    @abstractmethod
    async def subscribe(self):
        ...
