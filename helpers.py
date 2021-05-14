def int_to_bitsequence(value, length=None):
    bits = format(value, 'b')
    if length:
        bits = bits.zfill(length)
    return [int(b) for b in bits]