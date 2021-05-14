from dataclasses import dataclass


@dataclass(frozen=True)
class CanSignal:
    start_bit: int
    length: int
    byte_order: str = 'motorola'
    offset: int = 0
    factor: float = 1.0
    unit: str = ''

    def to_bin(self, dec_val, rescale=True):
        """Converts a measured value to a bitstring according to signal specifications:
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
        bits = int_to_bitstring(int_value, self.length)
        return bits

    def to_dec(self, binary):
        pass


def int_to_bitstring(value, length=None):
    bits = format(value, 'b')
    if length:
        bits = bits.zfill(length)
    return bits


def make_frame(data=0, bytes=8):
    """Builds a representation of a CAN data field.

    Note: Bits within each byte are ordered least significant first, which
    is opposite to how we've seen them displayed in data field diagrams.
    So when displaying a frame, each byte should be reversed, in order to match the diagrams:

    >>> for byte in frame:
    ...   print(byte[::-1])

    The point of reversing each byte internally is so that a lower bit address also means
    a lower list index, making it a little easier to reason about the structure (I think).
    """
    length = bytes * 8
    bits = int_to_bitstring(data, length)
    frame = []
    for byte_start in range(0, length, 8):
        byte_str = bits[byte_start: byte_start+8]
        byte = [int(b) for b in reversed(byte_str)]
        frame.append(byte)
    return frame


def display_frame(frame, print_it=True):
    mirrored_bits = []
    for byte in frame:
        reversed_bitstring = ''.join(str(b) for b in reversed(byte))
        mirrored_bits.append(reversed_bitstring)
    output = '\n'.join(mirrored_bits)
    if print_it:
        print(output)
    else:
        return output


def pack_signal(frame_data, signal, value, rescale=True):
    # converting start bit number to specific byte and position within that byte
    byte_index, bit_index = divmod(signal.start_bit, 8)

    # the bit sequence to write
    bits = signal.to_bin(value, rescale=rescale)

    # whether to iterate bytes upwards or downwards
    if signal.byte_order == 'motorola':
        byte_step = -1
    else:
        byte_step = 1

    # reversing bit sequence to write least significants first
    for bit in reversed(bits):
        byte = frame_data[byte_index]
        byte[bit_index] = int(bit)
        bit_index += 1

        # switching which byte to write to
        if bit_index == 8:
            bit_index = 0
            byte_index += byte_step

