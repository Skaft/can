from can.helpers import int_to_bitsequence, pad_sequence


class BaseFrame:
    def __init__(self, identifier, payload, num_bytes, use_crc=False):
        self.fields = {
            "sof": [0],
            "identifier": int_to_bitsequence(identifier, 11),
            "rtr": [0],
            "ide": [0],
            "r0": [0],
            "dlc": int_to_bitsequence(num_bytes, 4),
            "data": int_to_bitsequence(payload, num_bytes * 8),
            "crc": [0] * 15,
            "crc-d": [1],
            "ack": [1],
            "ack-d": [1],
            "eof": [1] * 7,
        }

        if use_crc:
            self.set_crc()

    def get_bit_sequence(self, bit_stuffing=True):
        sequence = [bit for bits in self.fields.values() for bit in bits]
        if bit_stuffing:
            to_stuff = sequence[:-10]
            tail = sequence[-10:]
            stuffed = pad_sequence(to_stuff)
            sequence = stuffed + tail
        return sequence

    def set_crc(self):

        content_keys = ["sof", "identifier", "rtr", "ide", "r0", "dlc", "data"]
        content = [bit for key in content_keys for bit in self.fields[key]]
        input_bitstring = "".join(str(bit) for bit in content)
        polynomial_bitstring = "1100010110011001"
        initial_filler = "0"

        # Code from https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Computation
        polynomial_bitstring = polynomial_bitstring.lstrip("0")
        len_input = len(input_bitstring)
        initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
        input_padded_array = list(input_bitstring + initial_padding)
        while "1" in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index("1")
            for i in range(len(polynomial_bitstring)):
                input_padded_array[cur_shift + i] = str(
                    int(polynomial_bitstring[i] != input_padded_array[cur_shift + i])
                )
        crc = "".join(input_padded_array)[len_input:]

        self.fields["crc"] = [int(b) for b in crc]
