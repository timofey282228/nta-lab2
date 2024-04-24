from nta_lab2.sph import silver_pohlig_hellman
from samples import TEST_SETS


def test_sph():
    for ts in TEST_SETS:
        x = silver_pohlig_hellman(*ts)
        assert pow(ts[0], x, ts[2]) == ts[1]
