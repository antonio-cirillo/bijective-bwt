from test.huffman import COMPRESSED_HUFFMAN_DIR_PATH
from test.huffman import DECOMPRESSED_HUFFMAN_DIR_PATH
from test.huffman import generate_file_name

from bbwt_cfl.encode import encode as bbwt_encode
from bbwt_cfl.decode import decode as bbwt_decode

from mtf.mtf import m2f_e
from mtf.mtf import m2f_d

from huffman.huffman import huffman_encoding
from huffman.huffman import huffman_decoding

from util.file import read_in_chunks
from util.file import write_compressed_file
from util.file import read_compressed_file
from util.file import write_decompressed_file

import os
import io

PRE_PROCESSING: str = "bbwt_m2f"
CHUNK_SIZE = io.DEFAULT_BUFFER_SIZE


def bbwt_m2f_huffman(file_path: str, file_name: str, alphabet: list[str]) -> str:
    # open file
    _file = open(os.path.join(file_path, file_name))
    # generate file name of compressed file
    _file_name: str = os.path.splitext(file_name)[0]
    compressed_file_name: str = generate_file_name(_file_name, PRE_PROCESSING)

    # clone alphabet
    _alphabet = alphabet[:]

    # apply bbwt and m2f for each chunk
    m2f_encoded_chunks = []
    for chunk in read_in_chunks(_file, chunk_size=CHUNK_SIZE):
        # use bbwt encoding
        bbwt_encoded_chunk = bbwt_encode(chunk)
        # use m2f encoding
        m2f_encoded_chunk = m2f_e(bbwt_encoded_chunk, _alphabet)
        # append chunk
        m2f_encoded_chunks += m2f_encoded_chunk

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
    # for each chunk use m2f decoding and bbwt decoding
    for chunk in [decompressed_data[i:i + CHUNK_SIZE]
                  for i in range(0, len(decompressed_data), CHUNK_SIZE)]:
        # use m2f decoding
        m2f_decoded_chunk = m2f_d(chunk, _alphabet)
        # use bbwt decoding
        bbwt_decoded_chunk = bbwt_decode(m2f_decoded_chunk)
        write_decompressed_file(DECOMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name, bbwt_decoded_chunk)

    return os.path.join(DECOMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name)
