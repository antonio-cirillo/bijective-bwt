from test.arithmetic_coding import COMPRESSED_ARITHMETIC_CODING_DIR_PATH
from test.arithmetic_coding import DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH
from test.arithmetic_coding import generate_file_name

from pre_processing.bwt.encode import encode as bwt_encode
from pre_processing.bwt.decode import decode as bwt_decode

from pre_processing.mtf import m2f_e
from pre_processing.mtf import m2f_d

from pre_processing.rle import rle_e
from pre_processing.rle import rle_d

from compression.arithmetic_coding import arithmetic_encoding
from compression.arithmetic_coding import arithmetic_decoding

from util.file import read_in_chunks
from util.file import write_decompressed_file
from util.file import write_compressed_file_path_folder

import os
import io

PRE_PROCESSING: str = "bwt_m2f_rle"
CHUNK_SIZE = io.DEFAULT_BUFFER_SIZE


def _convert_str_in_tuple(string: str) -> (int, int):
    _strings: [str] = string.split("-")
    return int(_strings[0]), int(_strings[1])


def bwt_m2f_rle_arithmetic_coding(file_path: str, file_name: str, alphabet: list[str]) -> str:
    # open and read file
    _file = open(os.path.join(file_path, file_name))
    # generate file name and file path of compressed file
    _file_name: str = os.path.splitext(file_name)[0]
    compressed_file_name: str = generate_file_name(_file_name, PRE_PROCESSING)
    compressed_file_path: str = write_compressed_file_path_folder(COMPRESSED_ARITHMETIC_CODING_DIR_PATH,
                                                                  compressed_file_name)
    # clone alphabet
    _alphabet = alphabet[:] + ['§']

    # apply bwt for each chunk
    bwt_encoded = ""
    for chunk in read_in_chunks(_file, chunk_size=CHUNK_SIZE):
        # use bwt encoding
        bwt_encoded_chunk = bwt_encode(chunk)
        bwt_encoded += bwt_encoded_chunk
    # use m2f encoding
    m2f_encoded = m2f_e(bwt_encoded, _alphabet)
    # use rle encoding
    rle_encoded = rle_e(m2f_encoded)
    # convert m2f encoding into a string
    rle_encoded_string = ""
    for rle_item in rle_encoded:
        rle_encoded_string += str(rle_item[0]) + '-' + str(rle_item[1]) + ' '
    rle_encoded_string = rle_encoded_string[:-1].encode()
    # use arithmetic encoding and write compressed file
    arithmetic_encoding(rle_encoded_string, compressed_file_path)

    # read file and use arithmetic decoding
    decompressed_data = arithmetic_decoding(compressed_file_path)
    # convert decompressed_data into a tuple list
    decompressed_data = list(map(str, decompressed_data.split(" ")))
    decompressed_data = list(map(_convert_str_in_tuple, decompressed_data))
    # use rle decoding
    rle_decoded = rle_d(decompressed_data)
    # init _alphabet
    _alphabet = alphabet[:] + ['§']
    # use m2f decoding
    m2f_decoded = m2f_d(rle_decoded, _alphabet)
    # use bwt decoding for each chunk
    for chunk in [m2f_decoded[i:i + CHUNK_SIZE + 1]
                  for i in range(0, len(m2f_decoded), CHUNK_SIZE + 1)]:
        bwt_decoded_chunk = bwt_decode(chunk)
        write_decompressed_file(DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH, compressed_file_name, bwt_decoded_chunk)

    return compressed_file_path
