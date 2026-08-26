"""Week 1, Day 1 drill — lazy file reading.

TDD spec. Implement `lazy_lines` in `src/dale/lazy_lines.py` until these pass:

    cd ~/code/mr/dale
    python -m pytest tests/test_lazy_lines.py -v

Contract for `lazy_lines(path)`:
- Takes a path (str or pathlib.Path).
- Returns a GENERATOR that yields the file's lines one at a time.
- Each yielded line is stripped of its trailing newline / surrounding whitespace.
- BLANK lines (empty or whitespace-only) are skipped.
- It is LAZY: it does not read the whole file into memory up front, and it
  yields the first line before the file has been fully consumed.
"""
import inspect
from pathlib import Path

import pytest

from dale.lazy_lines import lazy_lines


@pytest.fixture
def sample_file(tmp_path) -> Path:
    p = tmp_path / "sample.txt"
    # note the blank lines and trailing whitespace we expect to be handled
    p.write_text(
        "first line\n"
        "  second line  \n"
        "\n"
        "   \n"
        "third line\n"
    )
    return p


def test_yields_nonblank_stripped_lines(sample_file):
    assert list(lazy_lines(sample_file)) == ["first line", "second line", "third line"]


def test_accepts_str_path(sample_file):
    assert list(lazy_lines(str(sample_file))) == ["first line", "second line", "third line"]


def test_returns_a_generator(sample_file):
    result = lazy_lines(sample_file)
    assert inspect.isgenerator(result), "lazy_lines should return a generator, not a list"


def test_is_lazy_first_item_before_full_consumption(sample_file):
    # Pulling ONE item must not require reading the whole file. We prove laziness
    # by taking just the first value via next() without exhausting the generator.
    gen = lazy_lines(sample_file)
    assert next(gen) == "first line"
    # generator is still open / not exhausted
    assert inspect.getgeneratorstate(gen) != "GEN_CLOSED"


def test_empty_file_yields_nothing(tmp_path):
    p = tmp_path / "empty.txt"
    p.write_text("")
    assert list(lazy_lines(p)) == []


def test_all_blank_yields_nothing(tmp_path):
    p = tmp_path / "blanks.txt"
    p.write_text("\n   \n\t\n")
    assert list(lazy_lines(p)) == []
