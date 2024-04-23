import pytest

from nta_lab2.bruteforce import bruteforce


def test_bruteforce_error():
    a = 8201
    b = 70843
    p = 70841

    with pytest.raises(ValueError):
        bruteforce(a, b, p)

    with pytest.raises(ValueError):
        bruteforce(b, a, p)


def test_bruteforce_solution():
    a = 8201
    b = 46950
    p = 70841
    assert pow(a, bruteforce(a, b, p), p) == b


