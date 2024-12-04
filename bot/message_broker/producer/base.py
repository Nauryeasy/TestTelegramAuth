from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class BaseProducer(ABC):

    @abstractmethod
    def publish(self, event: BaseEvent):
        ...
