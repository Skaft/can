from can.signals import CanSignal

SPEED_SIGNAL = CanSignal(start_bit=43, length=11, factor=0.1, unit="km/h")
RPM_SIGNAL = CanSignal(start_bit=26, length=14, unit="RPM")
