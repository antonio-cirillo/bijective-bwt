from test.huffman import COMPRESSED_HUFFMAN_DIR_PATH
from test.huffman import generate_file_name

from huffman.huffman import huffman_encoding
from huffman.huffman import huffman_decoding

from util.file import write_compressed_file
from util.file import read_compressed_file

import os

PRE_PROCESSING: str = ""


def huffman(file_path: str, file_name: str):
    # open and read file
    _file = open(os.path.join(file_path, file_name))
    data = _file.read()

    # generate file name and file path of compressed file
    compressed_file_name: str = generate_file_name(file_name, PRE_PROCESSING)

    # use huffman encoding
    compressed_data, tree = huffman_encoding(data)

    # write compressed file
    write_compressed_file(COMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name, compressed_data)
    # read compressed file
    compressed_data: str = read_compressed_file(COMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name)

    # use huffman decoding
    decompressed_data: list[str] = huffman_decoding(compressed_data, tree)
    # convert decompressed_data to text
    _data: str = ''.join([str(item) for item in decompressed_data])

    assert _data == data