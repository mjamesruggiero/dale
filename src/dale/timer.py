import logging, time

logger = logging.getLogger(__name__)


class Timer:
    def __init__(self, label="block", logger=logger):
        self.label = label
        self._logger = logger
        self.elapsed = None 

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self._start
        if exc_type is None:
            self._logger.info("%s took %.4fs", self.label, self.elapsed)
        # should be false-y; don't suppress exceptions
        return False

