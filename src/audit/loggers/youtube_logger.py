import datetime
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class YoutubeLogEntry:
    domain_id: str
    level: Literal["INFO", "WARNING", "ERROR"]
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
