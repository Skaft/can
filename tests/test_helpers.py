from can.helpers import pad_sequence, int_to_bitsequence


def test_make_simple_bitsequence():
    assert int_to_bitsequence(10) == [1, 0, 1, 0]


def test_make_padded_bitsequence():
    assert int_to_bitsequence(10, length=7) == [0, 0, 0, 1, 0, 1, 0]


def test_simple_bit_stuffing():
    bits = [1, 1, 1, 1, 1, 1, 1]
    expected = [1, 1, 1, 1, 1, 0, 1, 1]
    assert pad_sequence(bits) == expected


def test_many_bit_stuffings():
    # fmt: off
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
    # fmt: on
    assert pad_sequence(bits) == expected


def test_connected_long_regions():
    bits = [0, 0, 0, 0, 0, 1, 1, 1, 1]
    expected = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
    assert pad_sequence(bits) == expected
