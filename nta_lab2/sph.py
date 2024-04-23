from collections import OrderedDict

import numpy as np
from nta_lab1 import canonical
from nta_lab1.miller_rabin import miller_rabin_test


def calc_modppowl(a, b, p, pi, l, table: dict[int, int]):
    x = np.zeros((l,), dtype=np.dtypes.Int64DType)
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


def crt(x, pi, li, nn):
    m = np.zeros((len(x),), dtype=np.dtypes.Int64DType)
    n = np.zeros((len(x),), dtype=np.dtypes.Int64DType)

    for i in range(pi.shape[0]):
        m[i] = (np.power(pi, li).prod()) // np.power(pi[i], li[i])
        n[i] = pow(int(m[i]), -1, int(np.power(pi[i], li[i])))

    return int((np.multiply(x, np.multiply(m, n)) % nn).sum())


def silver_pohlig_hellman(a, b, p, *, pt_iters=10):
    assert miller_rabin_test(p, pt_iters)

    n = p - 1
    n_canon = OrderedDict(canonical(n))
    r_tables = [{} for _ in range(len(n_canon))]
    for i, pi in enumerate(n_canon.keys()):
        t = n // pi
        for j in range(0, pi):
            r_tables[i][pow(a, t * j, p)] = j

    x = np.zeros((len(n_canon),), dtype=np.dtypes.Int64DType)
    for i, (pi, li) in enumerate(n_canon.items()):
        x[i] = calc_modppowl(a, b, p, pi, li, r_tables[i])

    solution = (
        crt(x, np.array(tuple(n_canon.keys())), np.array(tuple(n_canon.values())), n)
        % n
    )

    return solution % n
