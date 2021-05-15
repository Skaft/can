from can.helpers import pad_sequence


def test_simple_bit_stuffing():
    bits = [1,1,1,1,1,1,1]
    expected = [1,1,1,1,1,0,1,1]
    assert pad_sequence(bits) == expected

def test_many_bit_stuffings():
    bits = [
        1,0,1,1,1,1,1,
        1,0,1,1,1,1,1,
        1,0,0,0,0,0,0,
        1,0,1,1,1,1,1,
    ]
    expected = [
        1,0,1,1,1,1,1,0,
        1,0,1,1,1,1,1,0,
        1,0,0,0,0,0,1,0,
        1,0,1,1,1,1,1,0,
    ]
    assert pad_sequence(bits) == expected

def test_connected_long_regions():
    bits = [0,0,0,0,0,1,1,1,1]
    expected = [0,0,0,0,0,1,1,1,1,1,0]
    assert pad_sequence(bits) == expected
