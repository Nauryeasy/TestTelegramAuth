from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Any, Generic
from uuid import uuid4


@dataclass(frozen=True)
class BaseEvent(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )
    created_at: datetime = field(
        default_factory=lambda: datetime.now().date(),
        kw_only=True
    )


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass
class BaseEventHandler(ABC, Generic[ET, ER]):
    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...
