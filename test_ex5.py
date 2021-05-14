from ex5 import *
import pytest
from math import ceil


SPEED_SIGNAL = CanSignal(start_bit=43, length=11, factor=0.1, unit='km/h')
RPM_SIGNAL = CanSignal(start_bit=26, length=14, unit='RPM')
TEST_DATA = {
    'data': 0xee67e17d9e1f0a3b,
    'display': '11101110\n01100111\n11100001\n01111101\n10011110\n00011111\n00001010\n00111011'
}


def test_building_frame():
    empty_frame = [[0] * 8 for _ in range(8)]
    assert Frame().bytes == empty_frame

    data = TEST_DATA['data']
    expected_display = TEST_DATA['display']

    data_length = ceil(data.bit_length() / 8)
    filled_frame = Frame(data, bytes=data_length)
    display = filled_frame.display(print_it=False)

    assert display == expected_display


def test_displaying_frame():
    byte1 = '01000001'
    byte2 = '10001000'

    binary = (byte1 + byte2) * 4
    frame = Frame(int(binary, 2))
    expected_display = '\n'.join([byte1, byte2] * 4)

    display = frame.display(print_it=False)
    assert display == expected_display


def test_pack_scaling_on_off():
    frame_1 = Frame(data=0, bytes=8)
    frame_1.pack(SPEED_SIGNAL, 96.3, rescale=True)

    frame_2 = Frame(data=0, bytes=8)
    frame_2.pack(SPEED_SIGNAL, 963, rescale=False)

    assert frame_1.bytes == frame_2.bytes


def test_signal_conversion():
    signal = SPEED_SIGNAL
    unscaled_bin = signal.to_bin(963, rescale=False)
    scaled_bin = signal.to_bin(96.3, rescale=True)

    expected_bin_string = '01111000011'
    expected = [int(b) for b in expected_bin_string]

    assert unscaled_bin == expected    
    assert scaled_bin == expected

    with pytest.raises(ValueError):
        signal.to_bin(96.3, rescale=False)


def test_pack_speed():
    frame = Frame(data=0, bytes=8)
    frame.pack(SPEED_SIGNAL, 96.3)
    expected = '00000000\n00000000\n00000000\n00000000\n00011110\n00011000\n00000000\n00000000'
    result = frame.display(print_it=False)
    assert result == expected
    
def test_pack_rpm():
    frame = Frame(data=0, bytes=8)
    frame.pack(RPM_SIGNAL, 14431)
    expected = '00000000\n00000000\n11100001\n01111100\n00000000\n00000000\n00000000\n00000000'
    result = frame.display(print_it=False)
    assert result == expected

# def test_unpack_speed():
#     frame = make_frame(TEST_DATA['data'], bytes=8)
