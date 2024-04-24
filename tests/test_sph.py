from nta_lab2.sph import silver_pohlig_hellman

# ((a,b,p), ...)
TEST_SETS = (
    (5, 11, 73),
    (1414, 8882, 39439),
    (874578, 4152702, 21378421),
    (1691324, 2256687, 8282327),
    (8806623, 9601633, 33723379),
    (184557166, 381163683, 499478311),
    (4216705361681, 546941527639, 5992080474691),
)


def test_sph():
    for ts in TEST_SETS:
        x = silver_pohlig_hellman(*ts)
        assert pow(ts[0], x, ts[2]) == ts[1]
