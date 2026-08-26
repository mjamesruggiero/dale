# learnings

## first one: generators

`lazy_lines` (generator) consumes OOM less memory than the old "file->list" habit. 
Running a test on the same ~1500 line CSV, here's the meat test:

```python
import tracemalloc
from dale.lazy_lines import lazy_lines

TEST_FILE = "/Users/michaelruggiero/Desktop/debris/2026_08_10_checking.csv"

def list_version(path):
    payload = []
    with open(path) as fh:
        for line in fh:
            l = line.strip()
            if l:
                payload.append(l)
    return payload


def measure(fun):
    tracemalloc.start()
    result = fun()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{fun.__name__}: current={current/1024:.1f} KB, peak={peak/1024:.1f} KB")
    return result


def build_list():
    return list_version(TEST_FILE)


def build_generator():
    return sum(1 for _ in lazy_lines(TEST_FILE))


if __name__ == "__main__":
    measure(build_list)
    measure(build_generator)

```
And the result:

```
build_list: current=304.2 KB, peak=317.8 KB
build_generator: current=0.1 KB, peak=22.4 KB
```
