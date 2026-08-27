"""
- Yields successive length-`n` windows (as tuples) sliding one element at a time.
- `windowed([1,2,3,4], 2)` -> (1,2), (2,3), (3,4)
- Works over any iterable, a one-shot iterator/generator (not just sequences you can index) 
- Lazy: pulling one window must not consume the whole (possibly infinite) input.
- If `n` is larger than the input length, yields nothing.
- `n < 1` raises ValueError.
"""
import inspect
from itertools import count, islice

import pytest

from dale.windowed import windowed


def test_basic_pairs():
    assert list(windowed([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]


def test_window_of_three():
    assert list(windowed([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]


def test_window_equal_to_length_yields_one():
    assert list(windowed([1, 2, 3], 3)) == [(1, 2, 3)]


def test_window_larger_than_input_yields_nothing():
    assert list(windowed([1, 2], 3)) == []


def test_yields_tuples():
    first = next(windowed([1, 2, 3], 2))
    assert isinstance(first, tuple)


def test_returns_a_generator():
    assert inspect.isgenerator(windowed([1, 2, 3], 2))


def test_works_on_a_one_shot_iterator():
    # A generator can't be indexed or re-iterated -- windowed must still work.
    src = (x for x in [1, 2, 3, 4])
    assert list(windowed(src, 2)) == [(1, 2), (2, 3), (3, 4)]


def test_is_lazy_over_infinite_input():
    # itertools.count() is infinite; if windowed weren't lazy this would hang.
    gen = windowed(count(1), 2)
    assert list(islice(gen, 3)) == [(1, 2), (2, 3), (3, 4)]


def test_invalid_n_raises():
    with pytest.raises(ValueError):
        list(windowed([1, 2, 3], 0))
