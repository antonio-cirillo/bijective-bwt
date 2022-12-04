from huffman.huffman import huffman_encoding
from huffman.huffman import huffman_decoding

from util.file import RANDOM_FILE_NAME
from util.file import COMPRESSED_FILE_NAME

from util.file import generate_random_file
from util.file import write_compressed_file
from util.file import read_compressed_file

# declare sizes in byte
# 10 byte, 100 byte, 1 kB, 10 kB, 100 kB, 1 MB, 10 MB
SIZES = [10, 100, 1000, 10000, 100000, 1000000, 10000000]

# for each size
for size in SIZES:
    # create file name of generated file
    file_name: str = RANDOM_FILE_NAME.format(size=size)
    # generate random file
    file_path: str = generate_random_file(file_name, size)

    # read generated file
    with open(file_path, 'r') as file:
        data: str = file.read()

    # use huffman encoding
    compressed_data, tree = huffman_encoding(data)
    # generate file name of compressed file
    compressed_file_name: str = COMPRESSED_FILE_NAME.format(size=size)
    # write compressed file
    compressed_file_path: str = write_compressed_file(compressed_file_name, compressed_data)

    # read compressed file
    compressed_data: str = read_compressed_file(compressed_file_name)
    # use huffman decoding
    decompressed_data: str = huffman_decoding(compressed_data, tree)

    # check if data is equal to decompressed_data
    if data != decompressed_data:
        print("decompressed data is not equal to original data")
