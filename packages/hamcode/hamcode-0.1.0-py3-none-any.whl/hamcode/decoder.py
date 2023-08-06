from typing import Union
from math import ceil, log2


count_k = lambda m: ceil(log2(log2(m + 1) + m + 1))

def array_count_xor(array: list[int], kbit_num: int):
    n = 0#array[kbit_num-1]
    for i in range(kbit_num-1, len(array), 2*kbit_num):
        for j in array[i: i+kbit_num]:
            n ^= j
    return n


def decode_block(array: list[int], k: int):
    kbits = []
    bit_err_ind = -1
    for kbit in range(1, k+1):
        b = 2**kbit//2
        kbits.append(b)
        bit_err_ind += (b) * (array_count_xor(array , b))#==array[b-1])

    if bit_err_ind != -1:
        array[bit_err_ind] ^= 1

    n = -1
    for key in kbits:
        n+=1
        del array[key-1-n]
    return array, bit_err_ind if bit_err_ind != -1 else None


def decode(string: str, block_len: int, return_bit_errors: bool= False) -> Union[tuple[str, list[int]], str]:
    """
    In Ham-Code (12,8) block_len == 8
    """
    array = list(map(int, string))
    k = count_k(block_len)
    block_len += k
    err_bits = []
    res = ''

    n = -1
    for ind in range(block_len, len(array)+1, block_len):
        n+=1
        el, err_bit = decode_block(array[ind-block_len:ind], k)

        if return_bit_errors and err_bit is not None:
            err_bits.append(err_bit*(n+1))
        res+= ''.join(str(e) for e in el)

    if return_bit_errors:
        return res, err_bits
    return res


