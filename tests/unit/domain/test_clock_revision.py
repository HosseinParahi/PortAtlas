"""UT-DOM-001: deterministic time and optimistic-revision primitives."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta

from portatlas.domain.clock import FrozenClock, require_utc
from portatlas.domain.revision import Revision


class ClockAndRevisionTests(unittest.TestCase):
    def test_frozen_clock_injects_wall_and_monotonic_time(self) -> None:
        start = datetime(2026, 7, 11, tzinfo=UTC)
        clock = FrozenClock(start, monotonic_value=20.0)

        clock.advance(timedelta(seconds=5))

        self.assertEqual(clock.now(), start + timedelta(seconds=5))
        self.assertEqual(clock.monotonic(), 25.0)

    def test_domain_rejects_naive_or_non_utc_timestamps(self) -> None:
        with self.assertRaises(ValueError):
            require_utc(datetime(2026, 7, 11, tzinfo=None))  # noqa: DTZ001

        non_utc = datetime.fromisoformat("2026-07-11T01:00:00+01:00")
        with self.assertRaises(ValueError):
            require_utc(non_utc)

    def test_revision_starts_at_one_and_increments_immutably(self) -> None:
        first = Revision.initial()

        second = first.next()

        self.assertEqual(first.value, 1)
        self.assertEqual(second.value, 2)
        self.assertNotEqual(first, second)

    def test_revision_rejects_zero_negative_and_boolean_values(self) -> None:
        for value in (0, -1, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Revision(value)


if __name__ == "__main__":
    unittest.main()
