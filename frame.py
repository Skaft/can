from helpers import int_to_bitsequence, pad_sequence


class BaseFrame:
    def __init__(self, identifier, payload, num_bytes):
        self.fields = {
            'sof': [0],
            'identifier': int_to_bitsequence(identifier, 11),
            'rtr': [0],
            'ide': [0],
            'r0': [0],
            'dlc': int_to_bitsequence(num_bytes, 4),
            'data': int_to_bitsequence(payload, num_bytes * 8),
            'crc': [0] * 15,
            'crc-d': [1],
            'ack': [1],
            'ack-d': [1],
            'eof': [1] * 7
        }

    def get_bit_sequence(self, bit_stuffing=True):
        sequence = [bit for bits in self.fields.values() for bit in bits]
        if bit_stuffing:
            to_stuff = sequence[:-10]
            tail = sequence[-10:]
            stuffed = pad_sequence(to_stuff)
            sequence = stuffed + tail        
        return sequence
