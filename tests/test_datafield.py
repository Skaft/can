from math import ceil

import pytest

from can.datafield import DataField
from tests.utils import SPEED_SIGNAL, RPM_SIGNAL, FULL_FIELD


@pytest.fixture
def full_field():
    return DataField(FULL_FIELD["data"])


@pytest.fixture
def empty_field():
    return DataField()


@pytest.fixture
def empty_field_gen():
    return lambda: DataField()


@pytest.fixture
def empty_bytestrings():
    return ["0" * 8 for _ in range(8)]


def test_building_field(empty_field, full_field):
    expected_empty_field_bytes = [[0] * 8 for _ in range(8)]
    expected_full_field_bytes = FULL_FIELD["bytes"]

    assert empty_field.bytes == expected_empty_field_bytes
    assert full_field.bytes == expected_full_field_bytes


def test_displaying_field(full_field):
    expected_display = FULL_FIELD["display"]
    display = full_field.display(print_it=False)
    assert display == expected_display


def test_pack_scaling_on_off(empty_field_gen):
    field_1 = empty_field_gen()
    field_2 = empty_field_gen()

    field_1.pack(SPEED_SIGNAL, 96.3, rescale=True)
    field_2.pack(SPEED_SIGNAL, 963, rescale=False)

    assert field_1.bytes == field_2.bytes


def test_pack_speed(empty_field, empty_bytestrings):
    empty_field.pack(SPEED_SIGNAL, 96.3)
    result = empty_field.display(print_it=False)

    empty_bytestrings[4:6] = ["00011110", "00011000"]
    expected = "\n".join(empty_bytestrings)

    assert result == expected


def test_pack_rpm(empty_field, empty_bytestrings):
    empty_field.pack(RPM_SIGNAL, 14431)
    result = empty_field.display(print_it=False)

    empty_bytestrings[2:4] = ["11100001", "01111100"]
    expected = "\n".join(empty_bytestrings)

    assert result == expected


def test_unpack_speed(full_field):
    speed = full_field.unpack(SPEED_SIGNAL)
    expected = FULL_FIELD["speed"]
    assert speed == expected


def test_unpack_rpm(full_field):
    rpm = full_field.unpack(RPM_SIGNAL)
    expected = FULL_FIELD["rpm"]
    assert rpm == expected
