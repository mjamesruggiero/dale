class Ledger:
    def __init__(self, items=None):
        self._items = list(items) if items is not None else []

    def append(self, item):
        self._items.append(item)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        # return a fresh iterator for every call
        return iter(self._items)
