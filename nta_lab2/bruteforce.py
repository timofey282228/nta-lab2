def bruteforce(a, b, p) -> int | None:
    if not a in range(1, p) or not b in range(1, p):
        raise ValueError

    for x in range(0, p - 2):
        if pow(a, x, p) == b:
            return x
