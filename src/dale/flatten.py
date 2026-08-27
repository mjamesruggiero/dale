from typing import ItemsView


def flatten(nested):
    for item in nested:
        if isinstance(item, (str, bytes)):
            # atomic leaf
            yield item
        else:
            try:
                # is it iterable?
                iter(item)
            except TypeError:
                # non-iterable leaf (int, etc.)
                yield item
            else:
                # recurse
                yield from flatten(item)
