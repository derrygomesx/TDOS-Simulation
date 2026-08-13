"""
Track Digital Operations Sandbox (TDOS)

event_bus.py

Central event bus for communication between TDOS modules.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, DefaultDict

from tdos.config.logging import log

# ==========================================================
# Event
# ==========================================================


@dataclass(slots=True)
class Event:
    """
    Represents a TDOS event.
    """

    event_type: str

    source: str

    payload: dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.now)


# ==========================================================
# Event Bus
# ==========================================================


class EventBus:
    """
    Publish / Subscribe event bus.

    Every TDOS subsystem communicates through this class.
    """

    def __init__(self) -> None:

        self._subscribers: DefaultDict[str, list[Callable[[Event], None]]] = defaultdict(list)

    # ======================================================
    # Subscription
    # ======================================================

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[Event], None],
    ) -> None:
        """
        Subscribe to an event.
        """

        self._subscribers[event_type].append(callback)

        log.debug(f"Subscriber added -> {event_type}")

    # ======================================================
    # Unsubscribe
    # ======================================================

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[[Event], None],
    ) -> None:
        """
        Remove an event subscriber.
        """

        if callback in self._subscribers[event_type]:

            self._subscribers[event_type].remove(callback)

    # ======================================================
    # Publish
    # ======================================================

    def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event.
        """

        log.debug(f"Publishing {event.event_type}")

        for callback in self._subscribers[event.event_type]:

            callback(event)

    # ======================================================
    # Utilities
    # ======================================================

    def clear(self) -> None:
        """
        Remove all subscribers.
        """

        self._subscribers.clear()

    @property
    def subscriber_count(self) -> int:
        """
        Total registered subscribers.
        """

        return sum(len(v) for v in self._subscribers.values())

    def event_count(
        self,
        event_type: str,
    ) -> int:
        """
        Number of subscribers for one event.
        """

        return len(self._subscribers[event_type])
