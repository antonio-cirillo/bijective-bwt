from test.huffman import COMPRESSED_HUFFMAN_DIR_PATH
from test.huffman import DECOMPRESSED_HUFFMAN_DIR_PATH
from test.huffman import generate_file_name

from pre_processing.bwt import encode as bwt_encode
from pre_processing.bwt import decode as bwt_decode

from pre_processing.mtf import m2f_e
from pre_processing.mtf import m2f_d

from compression.huffman import huffman_encoding
from compression.huffman import huffman_decoding

from util.file import read_in_chunks
from util.file import write_compressed_file
from util.file import read_compressed_file
from util.file import write_decompressed_file

import os

PRE_PROCESSING: str = "bwt_m2f"
CHUNK_SIZE = 100  # io.DEFAULT_BUFFER_SIZE


def bwt_m2f_huffman(file_path: str, file_name: str, alphabet: list[str]) -> str:
    # open file
    _file = open(os.path.join(file_path, file_name))
    # generate file name of compressed file
    _file_name: str = os.path.splitext(file_name)[0]
    compressed_file_name: str = generate_file_name(_file_name, PRE_PROCESSING)

    # clone alphabet
    _alphabet = alphabet[:]

    # apply bwt and m2f for each chunk
    m2f_encoded_chunks = []
    i = 0
    for chunk in read_in_chunks(_file, chunk_size=CHUNK_SIZE):
        # use bwt encoding
        bwt_encoded_chunk = bwt_encode(chunk)
        # use m2f encoding
        m2f_encoded_chunk = m2f_e(bwt_encoded_chunk, _alphabet)
        # append chunk
        m2f_encoded_chunks += m2f_encoded_chunk
        i += 1
        if i > 5:
            break

    # use huffman encoding
    compressed_data, tree = huffman_encoding(m2f_encoded_chunks)
    # write compressed file
    write_compressed_file(COMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name, compressed_data)

    # read compressed file
    compressed_data = read_compressed_file(COMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name)
    # use huffman decoding
    decompressed_data: str = huffman_decoding(compressed_data, tree)

    # init _alphabet
    _alphabet = alphabet[:]
    # for each chunk use m2f decoding and bwt decoding
    for chunk in [decompressed_data[i:i + CHUNK_SIZE + 2]
                  for i in range(0, len(decompressed_data), CHUNK_SIZE + 2)]:
        # use m2f decoding
        m2f_decoded_chunk = m2f_d(chunk, _alphabet)
        # use bwt decoding
        bwt_decoded_chunk = bwt_decode(m2f_decoded_chunk)
        write_decompressed_file(DECOMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name, bwt_decoded_chunk)

    return os.path.join(DECOMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name)
