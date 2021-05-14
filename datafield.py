from helpers import int_to_bitsequence


class DataField:
    """A representation of a CAN data field."""

    def __init__(self, data=0, bytes=8):
        length = bytes * 8
        bits = int_to_bitsequence(data, length)
        bytes = []
        for byte_start in range(0, length, 8):
            byte = bits[byte_start: byte_start+8]
            byte.reverse()
            bytes.append(byte)
        self.bytes = bytes

    def __repr__(self):
        hex = self.to_hex()
        num_bytes = len(self.bytes)
        return f'DataField(data={hex}, bytes={num_bytes})'

    def to_hex(self):
        bits = []
        for byte in self.bytes:
            bits.extend(map(str, reversed(byte)))
        binary = ''.join(bits)
        dec = int(binary, 2)
        return hex(dec)

    def display(self, print_it=True):
        mirrored_bits = []
        for byte in self.bytes:
            reversed_bitstring = ''.join(str(b) for b in reversed(byte))
            mirrored_bits.append(reversed_bitstring)
        output = '\n'.join(mirrored_bits)
        if print_it:
            print(output)
        else:
            return output

    def pack(self, signal, value, rescale=True):
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
            byte = self.bytes[byte_index]
            byte[bit_index] = bit
            bit_index += 1

            # switching which byte to write to
            if bit_index == 8:
                bit_index = 0
                byte_index += byte_step

    def unpack(self, signal, rescale=True):
        byte_index, bit_index = divmod(signal.start_bit, 8)

        if signal.byte_order == 'motorola':
            byte_step = -1
        else:
            byte_step = 1

        bits = []
        for _ in range(signal.length):
            byte = self.bytes[byte_index]
            bits.append(byte[bit_index])
            bit_index += 1
            if bit_index == 8:
                bit_index = 0
                byte_index += byte_step
        
        # reverse bit order to get msb first
        bits.reverse()
        return signal.to_dec(bits, rescale=rescale)
