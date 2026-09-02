from contextlib import contextmanager

@contextmanager
def swallow(*exc_types):
    """Note that except will take a tuple"""
    try:
        yield
    except exc_types:
        # returning normally, i.e. suppressing
        pass
