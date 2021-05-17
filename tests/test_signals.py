import pytest

from tests.utils import SPEED_SIGNAL


def test_signal_convert_to_bin():
    unscaled_bin = SPEED_SIGNAL.to_bin(963, rescale=False)
    scaled_bin = SPEED_SIGNAL.to_bin(96.3, rescale=True)

    expected = [int(b) for b in "01111000011"]

    assert unscaled_bin == expected
    assert scaled_bin == expected

    with pytest.raises(ValueError):
        SPEED_SIGNAL.to_bin(96.3, rescale=False)
