import bitarray


def _to_bytes(data: str) -> bytes:
    # get size of padding
    n_padding: int = 16 - (len(data) % 16)
    # convert size of padding in bytes
    n_padding_bytes: bytes = n_padding.to_bytes(1, 'big')
    # create bitarray from data + padding
    ba = bitarray.bitarray(data + "0" * n_padding)
    # return in bytes n_padding + data + padding
    return n_padding_bytes + ba.tobytes()


def _to_binary(data: bytes) -> str:
    # get size of padding
    n_padding: int = data[0]
    ba = bitarray.bitarray()
    # create bit array from bytes of data without n_padding
    ba.frombytes(data[1:])
    # convert to bitstring data without padding
    return ba.to01()[:-n_padding]
