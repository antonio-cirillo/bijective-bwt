from test.arithmetic_coding import COMPRESSED_ARITHMETIC_CODING_DIR_PATH
from test.arithmetic_coding import DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH
from test.arithmetic_coding import generate_file_name

from compression.arithmetic_coding import arithmetic_encoding
from compression.arithmetic_coding import arithmetic_decoding

from util.file import write_compressed_file_path_folder
from util.file import write_decompressed_file

import os

PRE_PROCESSING: str = ""


def arithmetic_coding(file_path: str, file_name: str) -> str:
    # open and read file
    _file = open(os.path.join(file_path, file_name), 'rb')
    data = _file.read()

    # generate file name and file path of compressed file
    _file_name: str = os.path.splitext(file_name)[0]
    compressed_file_name: str = generate_file_name(_file_name, PRE_PROCESSING)
    compressed_file_path: str = write_compressed_file_path_folder(COMPRESSED_ARITHMETIC_CODING_DIR_PATH,
                                                                  compressed_file_name)

    # use arithmetic encoding and write compressed file
    arithmetic_encoding(data, compressed_file_path)

    # read file and use arithmetic decoding
    decompressed_data = arithmetic_decoding(compressed_file_path)
    # write decompressed file
    write_decompressed_file(DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH, compressed_file_name, decompressed_data)

    return compressed_file_path
