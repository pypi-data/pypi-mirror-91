from .decoder import count_k, array_count_xor


def encode(string: str, block_len: int) -> str:
    """
    In Ham-Code (12,8) block_len == 8
    """
    k = count_k(block_len)
    array = list(map(int, string))
    kbit_mas = []
    for i in range(1, k+1):
        b = 2**i//2
        array.insert(b-1,0)
        kbit_mas.append(b)

    for kbit in kbit_mas:
        array[kbit-1] = array_count_xor(array, kbit)

    res = ''
    for i in array:
        res += str(i)
    return res


