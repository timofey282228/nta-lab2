from collections import OrderedDict

from nta_lab1 import canonical
from nta_lab1.miller_rabin import miller_rabin_test

from .D1IntArray import D1IntArray


def _calc_x(a, b, p, pi, l, table: dict[int, int]):
    x = D1IntArray.zeros(l)
    n = p - 1

    for k in range(0, l):
        apow = 0
        curpowofpi = 0
        for i in range(k):
            apow -= x[i] * pow(pi, curpowofpi, n)
            curpowofpi += 1

        x[k] = table[pow(b * pow(a, apow, p), n // pow(pi, k + 1), p)]

    cx = 0
    for i in range(len(x)):
        cx += (x[i] * pow(pi, i, n)) % n

    return cx % n


def _crt(x, pi, li, nn):
    m = D1IntArray.zeros(len(x))
    n = D1IntArray.zeros(len(x))

    for i in range(len(pi)):
        m[i] = nn // pow(pi[i], li[i])
        n[i] = pow(m[i], -1, pow(pi[i], li[i]))

    return (D1IntArray.multiply(x, D1IntArray.multiply(m, n, nn), nn)).sum()


def silver_pohlig_hellman(a, b, p, *, pt_iters=10):
    if not a in range(1, p) or not b in range(1, p):
        raise ValueError
    assert miller_rabin_test(p, pt_iters)

    n = p - 1
    n_canon = OrderedDict(canonical(n))
    r_tables = [{} for _ in range(len(n_canon))]
    for i, pi in enumerate(n_canon.keys()):
        t = n // pi
        for j in range(0, pi):
            r_tables[i][pow(a, t * j, p)] = j

    x = D1IntArray.zeros(len(n_canon))
    for i, (pi, li) in enumerate(n_canon.items()):
        x[i] = _calc_x(a, b, p, pi, li, r_tables[i])

    solution = _crt(x, D1IntArray(n_canon.keys()), D1IntArray(n_canon.values()), n) % n

    return solution % n
