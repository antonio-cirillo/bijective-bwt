from test.huffman import COMPRESSED_HUFFMAN_DIR_PATH
from test.huffman import generate_file_name

from bwt.encode import encode as bwt_encode
from bwt.decode import decode as bwt_decode

from mtf.mtf import m2f_e
from mtf.mtf import m2f_d

from huffman.huffman import huffman_encoding
from huffman.huffman import huffman_decoding

from util.file import write_compressed_file
from util.file import read_compressed_file

import numpy as np
import os

PRE_PROCESSING: str = "bwt_m2f"


def bwt_m2f_huffman(file_path: str, file_name: str, alphabet: list[str]) -> None:
    # open file
    _file = open(os.path.join(file_path, file_name))
    # generate file name and file path of compressed file
    compressed_file_name: str = generate_file_name(file_name, PRE_PROCESSING)

    # clone alphabet
    _alphabet = alphabet[:]

    # apply m2f for each line
    m2f_encoded_lines = []
    for _ in range(10):
        line = _file.readline()
        # use bwt encoding
        bwt_encoded_line = bwt_encode(line)
        # use m2f encoding
        m2f_encoded_line = m2f_e(bwt_encoded_line, _alphabet)
        # append line
        m2f_encoded_lines += m2f_encoded_line

    compressed_data, tree = huffman_encoding(m2f_encoded_lines)

    decompressed_data: str = huffman_decoding(compressed_data, tree)
    _alphabet = alphabet[:]
    m2f_decoded_lines = m2f_d(decompressed_data, _alphabet)

    for m2f_decoded_line in m2f_decoded_lines.splitlines():
        print(m2f_decoded_line)
        bwt_decoded_line = bwt_decode(m2f_decoded_line + "\n")
        print(bwt_decoded_line)
        break

    """
    _alphabet = alphabet[:]
    for m2f_encoded_line in m2f_encoded_lines:
        m2f_decoded_line = m2f_d(m2f_encoded_line, _alphabet)
        bwt_decoded_line = bwt_decode(m2f_decoded_line)
        print(bwt_decoded_line[:-1])
    """

