from collections import defaultdict
from dataclasses import dataclass, field
from typing import Type, Iterable

from core.apps.telegram_auth.events.base import ET, ER, BaseEventHandler


@dataclass(eq=False)
class Mediator:
    events_map: dict[Type[ET], list[BaseEventHandler[ET, ER]]] = field(
        default_factory=lambda: defaultdict[Type[ET], list[BaseEventHandler[ET, ER]]](list),
        kw_only=True,
    )

    def register_event(self, event_type: Type[ET], handler: BaseEventHandler):
        self.events_map[event_type].append(handler)

    def handle_event(self, event: ET) -> Iterable[ER]:

        event_type = event.__class__
        handlers = self.events_map[event_type]

        if not handlers:
            raise Exception(f'No handlers for {event_type}')

        return [handler.handle(event) for handler in handlers]
