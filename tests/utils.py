from can.signals import CanSignal

SPEED_SIGNAL = CanSignal(start_bit=43, length=11, factor=0.1, unit="km/h")
RPM_SIGNAL = CanSignal(start_bit=26, length=14, unit="RPM")

FULL_FIELD = {
    "data": 0xEE67E17D9E1F0A3B,
    "display": "11101110\n01100111\n11100001\n01111101\n10011110\n00011111\n00001010\n00111011",
    "speed": {"value": 96.3, "unit": "km/h"},
    "rpm": {"value": 14431, "unit": "RPM"},
}
FULL_FIELD["bytes"] = [
    [int(b) for b in row] for row in FULL_FIELD["display"].splitlines()
]
