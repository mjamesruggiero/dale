"""Week 1, Day 4 drill — a class-based context manager (__enter__/__exit__).

    python -m pytest tests/test_timer.py -v

Contract for `Timer`:
- `Timer(label="block", logger=None)`; use as `with Timer() as t: ...`.
- `__enter__` returns the Timer instance (so `as t` binds it).
- After the block, `t.elapsed` is a float (seconds) >= 0, measured with
  time.perf_counter.
- `Timer` does NOT swallow exceptions: an exception raised in the block
  PROPAGATES. (I.e. `__exit__` returns a falsy value.)
- Even when the block raises, `t.elapsed` is still populated (measure in a
  finally-ish way -- __exit__ always runs).
- On a clean exit, it logs the duration at INFO, including the label.
"""
import logging
import time

import pytest

from dale.timer import Timer


def test_enter_returns_the_timer():
    with Timer() as t:
        assert isinstance(t, Timer)


def test_elapsed_is_a_nonnegative_float():
    with Timer() as t:
        pass
    assert isinstance(t.elapsed, float)
    assert t.elapsed >= 0.0


def test_elapsed_measures_the_block():
    with Timer() as t:
        time.sleep(0.02)
    assert t.elapsed >= 0.015  # slack for timer resolution


def test_exception_propagates_but_elapsed_is_set():
    t = Timer()
    with pytest.raises(ValueError):
        with t:
            raise ValueError("boom")
    # __exit__ ran, so timing was still recorded
    assert isinstance(t.elapsed, float)
    assert t.elapsed >= 0.0


def test_logs_duration_at_info(caplog):
    with caplog.at_level(logging.INFO):
        with Timer(label="ingest"):
            pass
    assert any("ingest" in rec.message for rec in caplog.records)
