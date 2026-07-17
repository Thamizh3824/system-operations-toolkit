from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class LogEntry:
    """
    Represents a single parsed log entry.
    """

    timestamp: datetime
    level: str
    message: str