"""
Track Digital Operations Sandbox (TDOS)

scheduler.py

Simulation scheduler responsible for executing timed events.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Callable, List

# ==========================================================
# Scheduled Event
# ==========================================================


@dataclass(order=True)
class ScheduledEvent:
    """
    Represents an event scheduled for execution.
    """

    execute_at: int

    priority: int

    callback: Callable = field(compare=False)

    name: str = field(default="Unnamed Event", compare=False)


# ==========================================================
# Scheduler
# ==========================================================


class SimulationScheduler:
    """
    Controls simulation time and executes scheduled events.
    """

    def __init__(self) -> None:

        self.current_step = 0

        self._queue: List[ScheduledEvent] = []

    # ======================================================
    # Scheduling
    # ======================================================

    def schedule(
        self,
        execute_at: int,
        callback: Callable,
        priority: int = 0,
        name: str = "Event",
    ) -> None:
        """
        Schedule an event.
        """

        heapq.heappush(
            self._queue,
            ScheduledEvent(
                execute_at=execute_at,
                priority=priority,
                callback=callback,
                name=name,
            ),
        )

    # ======================================================
    # Simulation Tick
    # ======================================================

    def tick(self) -> None:
        """
        Advances simulation by one step.
        """

        self.current_step += 1

        while self._queue and self._queue[0].execute_at <= self.current_step:

            event = heapq.heappop(self._queue)

            event.callback()

    # ======================================================
    # Utilities
    # ======================================================

    def clear(self) -> None:
        """
        Removes all scheduled events.
        """

        self._queue.clear()

    @property
    def pending_events(self) -> int:
        """
        Returns the number of queued events.
        """

        return len(self._queue)

    @property
    def empty(self) -> bool:
        """
        Returns True if no events remain.
        """

        return len(self._queue) == 0
