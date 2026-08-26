def lazy_lines(path):
    with open(path) as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:
                yield stripped
