from test.huffman import COMPRESSED_HUFFMAN_FILE_NAME
from test.huffman import COMPRESSED_HUFFMAN_DIR_PATH

from bbwt_cfl.encode import encode as bbwt_encode
from bbwt_cfl.decode import decode as bbwt_decode

from mtf.mtf import m2f_e
from mtf.mtf import m2f_d

from huffman.huffman import huffman_encoding
from huffman.huffman import huffman_decoding

from util.file import write_compressed_file
from util.file import read_compressed_file

PRE_PROCESSING: str = "bbwt_m2f"


def bbwt_m2f_huffman(size: int, data: str, alphabet: list[str]) -> None:
    # generate file name and file path of compressed file
    compressed_file_name: str = COMPRESSED_HUFFMAN_FILE_NAME \
        .format(size=size, pre_processing=PRE_PROCESSING)

    # use bbwt encoding
    bbwt_encoded_data = bbwt_encode(data)
    # use m2f encoding
    m2f_encoded_data = m2f_e(bbwt_encoded_data, alphabet[:])
    # use huffman encoding
    compressed_data, tree = huffman_encoding(m2f_encoded_data)

    # write compressed file
    write_compressed_file(COMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name, compressed_data)

    # read compressed file
    compressed_data: str = read_compressed_file(COMPRESSED_HUFFMAN_DIR_PATH, compressed_file_name)

    # use huffman decoding
    decompressed_data: str = huffman_decoding(compressed_data, tree)
    # use m2f decoding
    m2f_decoded_data = m2f_d(decompressed_data, alphabet[:])
    # use bbwt decoding
    bbwt_decoded_data = bbwt_decode(m2f_decoded_data)

    assert bbwt_decoded_data == data

    """
    string = ''.join([str(item) for item in decoded_output])
    """
