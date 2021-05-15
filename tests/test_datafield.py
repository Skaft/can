from math import ceil

import pytest

from can.datafield import DataField
from can.signals import *


TEST_DATA = {
    "data": 0xEE67E17D9E1F0A3B,
    "display": "11101110\n01100111\n11100001\n01111101\n10011110\n00011111\n00001010\n00111011",
}


def test_building_field():
    empty_field = [[0] * 8 for _ in range(8)]
    assert DataField().bytes == empty_field

    data = TEST_DATA["data"]
    expected_display = TEST_DATA["display"]

    data_length = ceil(data.bit_length() / 8)
    filled_field = DataField(data, bytes=data_length)
    display = filled_field.display(print_it=False)

    assert display == expected_display


def test_displaying_field():
    byte1 = "01000001"
    byte2 = "10001000"

    binary = (byte1 + byte2) * 4
    field = DataField(int(binary, 2))
    expected_display = "\n".join([byte1, byte2] * 4)

    display = field.display(print_it=False)
    assert display == expected_display


def test_pack_scaling_on_off():
    field_1 = DataField(data=0, bytes=8)
    field_1.pack(SPEED_SIGNAL, 96.3, rescale=True)

    field_2 = DataField(data=0, bytes=8)
    field_2.pack(SPEED_SIGNAL, 963, rescale=False)

    assert field_1.bytes == field_2.bytes


def test_signal_conversion():
    signal = SPEED_SIGNAL
    unscaled_bin = signal.to_bin(963, rescale=False)
    scaled_bin = signal.to_bin(96.3, rescale=True)

    expected_bin_string = "01111000011"
    expected = [int(b) for b in expected_bin_string]

    assert unscaled_bin == expected
    assert scaled_bin == expected

    with pytest.raises(ValueError):
        signal.to_bin(96.3, rescale=False)


def test_pack_speed():
    field = DataField(data=0, bytes=8)
    field.pack(SPEED_SIGNAL, 96.3)
    expected = (
        "00000000\n00000000\n00000000\n00000000\n00011110\n00011000\n00000000\n00000000"
    )
    result = field.display(print_it=False)
    assert result == expected


def test_pack_rpm():
    field = DataField(data=0, bytes=8)
    field.pack(RPM_SIGNAL, 14431)
    expected = (
        "00000000\n00000000\n11100001\n01111100\n00000000\n00000000\n00000000\n00000000"
    )
    result = field.display(print_it=False)
    assert result == expected


def test_unpack_speed():
    field = DataField(TEST_DATA["data"], bytes=8)
    speed = field.unpack(SPEED_SIGNAL)
    assert speed == {"value": 96.3, "unit": "km/h"}


def test_unpack_rpm():
    field = DataField(TEST_DATA["data"], bytes=8)
    speed = field.unpack(RPM_SIGNAL)
    assert speed == {"value": 14431, "unit": "RPM"}
