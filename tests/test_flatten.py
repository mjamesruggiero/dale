"""
- Recursively yields every leaf element from an arbitrarily nested iterable.
- `flatten([1, [2, 3], [4, [5, 6]]])` -> 1, 2, 3, 4, 5, 6
- strings (and bytes) are iterable, but must be treated as ATOMIC
  leaves e.g don't explode "ab" into 'a','b'. Sparks infinite
  recursion, since iterating a 1-char string yields that same 1-char string.
- Handles mixed nested iterable types (lists, tuples, generators).
- Lazy: returns a generator.
"""
import inspect

from dale.flatten import flatten


def test_flat_list_unchanged():
    assert list(flatten([1, 2, 3])) == [1, 2, 3]


def test_one_level_nesting():
    assert list(flatten([1, [2, 3], 4])) == [1, 2, 3, 4]


def test_deep_nesting():
    assert list(flatten([1, [2, [3, [4, [5]]]]])) == [1, 2, 3, 4, 5]


def test_strings_are_atomic():
    # "ab" and "cd" must come through whole, not split into characters.
    assert list(flatten([1, "ab", [2, "cd"]])) == [1, "ab", 2, "cd"]


def test_mixed_iterable_types():
    nested = [1, (2, 3), (x for x in [4, 5])]
    assert list(flatten(nested)) == [1, 2, 3, 4, 5]


def test_empty_and_nested_empty():
    assert list(flatten([])) == []
    assert list(flatten([[], [[]], []])) == []


def test_returns_a_generator():
    assert inspect.isgenerator(flatten([1, [2]]))
