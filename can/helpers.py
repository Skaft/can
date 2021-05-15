from itertools import groupby


def int_to_bitsequence(value, length=None):
    bits = format(value, "b")
    if length:
        bits = bits.zfill(length)
    return [int(b) for b in bits]


def pad_sequence(intlist, max_width=5):
    if intlist == []:
        return []
    digit, group = next(groupby(intlist))
    subsequence = list(group)
    cutoff = min(len(subsequence), max_width)
    head = intlist[:cutoff]
    if cutoff == max_width:
        opposite = 1 - digit
        tail = [opposite] + intlist[cutoff:]
    else:
        tail = intlist[cutoff:]
    return head + pad_sequence(tail)
