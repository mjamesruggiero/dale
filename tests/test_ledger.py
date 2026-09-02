"""Week 1, Day 3 drill — a custom ITERABLE class (seed of the capstone Ledger).

    python -m pytest tests/test_ledger.py -v

Contract for `Ledger`:
- `Ledger()` starts empty; `Ledger(iterable)` seeds from an iterable.
- `.append(item)` adds an item (append-only log).
- `len(ledger)` returns the number of items.
- Iterating yields items in insertion order.
- **Re-iterable**: iterating twice yields the same items both times.
- `iter(ledger)` returns a FRESH, INDEPENDENT iterator every call -- two
  iterators don't share position, and nested `for a in led: for b in led`
  works. THE TRAP: if you make the class its own iterator (return `self` from
  `__iter__` with a stateful `__next__`), it's one-shot and nested iteration
  breaks. The fix: `__iter__` should hand back a *new* iterator each time
  (e.g. `return iter(self._items)`).
- Usable in a comprehension.
"""
import pytest

from dale.ledger import Ledger


def test_empty_len():
    assert len(Ledger()) == 0


def test_append_grows_len():
    led = Ledger()
    led.append("a")
    led.append("b")
    assert len(led) == 2


def test_seed_from_iterable():
    led = Ledger([1, 2, 3])
    assert len(led) == 3


def test_iterates_in_insertion_order():
    led = Ledger()
    for x in (10, 20, 30):
        led.append(x)
    assert list(led) == [10, 20, 30]


def test_is_reiterable():
    led = Ledger([1, 2, 3])
    assert list(led) == [1, 2, 3]
    assert list(led) == [1, 2, 3]  # second pass must work too


def test_iter_returns_fresh_independent_iterators():
    led = Ledger([1, 2, 3])
    it1 = iter(led)
    it2 = iter(led)
    assert next(it1) == 1
    assert next(it2) == 1  # independent position, not sharing state with it1
    assert next(it1) == 2


def test_nested_iteration_works():
    # This is the tell: a self-as-iterator class produces the wrong count here.
    led = Ledger([1, 2, 3])
    pairs = [(a, b) for a in led for b in led]
    assert len(pairs) == 9


def test_usable_in_comprehension():
    led = Ledger([1, 2, 3, 4])
    assert [x * 2 for x in led] == [2, 4, 6, 8]
