from dataclasses import dataclass, field


@dataclass(eq=False)
class BaseEntity:
    id: int | None = field(default=None, kw_only=True)

    def __eq__(self, other):
        return self.id == other.id
