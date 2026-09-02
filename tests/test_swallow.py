"""Week 1, Day 4 drill — a generator-based context manager (@contextmanager).

    python -m pytest tests/test_swallow.py -v

Contract for `swallow(*exc_types)`:
- A context manager built with `@contextlib.contextmanager`.
- Suppresses exceptions whose type is in `exc_types` (execution continues
  after the `with` block, as if nothing was raised).
- Lets any OTHER exception propagate.
- With no exception, the block runs normally.

The point: in a generator context manager, an exception in the body is
THROWN INTO the generator at the `yield`. Catching it and returning normally
suppresses it (the generator analog of `__exit__` returning True); re-raising
(or not catching) lets it propagate.
"""
import pytest

from dale.swallow import swallow


def test_suppresses_named_exception():
    reached_after = False
    with swallow(ValueError):
        raise ValueError("nope")
        # (unreachable)
    reached_after = True  # we only get here if the exception was suppressed
    assert reached_after


def test_lets_other_exceptions_propagate():
    with pytest.raises(KeyError):
        with swallow(ValueError):
            raise KeyError("different type")


def test_multiple_types():
    with swallow(ValueError, KeyError):
        raise KeyError("caught")
    with swallow(ValueError, KeyError):
        raise ValueError("also caught")


def test_no_exception_runs_normally():
    out = []
    with swallow(ValueError):
        out.append(1)
        out.append(2)
    assert out == [1, 2]
