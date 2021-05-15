from dataclasses import dataclass

from can.helpers import int_to_bitsequence


@dataclass(frozen=True)
class CanSignal:
    start_bit: int
    length: int
    byte_order: str = 'motorola'
    offset: int = 0
    factor: float = 1.0
    unit: str = ''

    def to_bin(self, dec_val, rescale=True):
        """Converts a measured value to a binary sequence following signal specifications:
            * Pads with leading zeros to match the signals <length>
            * If rescale=True: Converts the <dec_val> according to <factor> and <offset>
            * If rescale=False: <dec_val> is expected to be converted already. If not given an int, raises ValueError
        
        The bit order is given with msb first.
        """
        if rescale:
            int_value = round((dec_val - self.offset) / self.factor)
        else:
            if not isinstance(dec_val, int):
                raise ValueError
            int_value = dec_val
        bits = int_to_bitsequence(int_value, self.length)
        return bits

    def to_dec(self, bits, rescale=True):
        binary = ''.join(str(b) for b in bits)
        value = int(binary, 2)
        if rescale:
            value = self.factor * value + self.offset
            value = round(value, 2)
        return {'value': value, 'unit': self.unit}


SPEED_SIGNAL = CanSignal(start_bit=43, length=11, factor=0.1, unit='km/h')
RPM_SIGNAL = CanSignal(start_bit=26, length=14, unit='RPM')
