from test.huffman.huffman import huffman
from test.huffman.bwt_m2f_huffman import bwt_m2f_huffman
from test.huffman.bbwt_m2f_huffman import bbwt_m2f_huffman
from test.huffman.bwt_m2f_rle_huffman import bwt_m2f_rle_huffman
from test.huffman.bbwt_m2f_rle_huffman import bbwt_m2f_rle_huffman

from test.arithmetic_coding.arithmetic_coding import arithmetic_coding
from test.arithmetic_coding.bwt_m2f_arithmetic_coding import bwt_m2f_arithmetic_coding
from test.arithmetic_coding.bbwt_m2f_arithmetic_coding import bbwt_m2f_arithmetic_coding
from test.arithmetic_coding.bwt_m2f_rle_arithmetic_coding import bwt_m2f_rle_arithmetic_coding
from test.arithmetic_coding.bbwt_m2f_rle_arithmetic_coding import bbwt_m2f_rle_arithmetic_coding

from test.lzw.lzw import lzw
from test.lzw.bwt_m2f_lzw import bwt_m2f_lzw
from test.lzw.bbwt_m2f_lzw import bbwt_m2f_lzw
from test.lzw.bwt_m2f_rle_lzw import bwt_m2f_rle_lzw
from test.lzw.bbwt_m2f_rle_lzw import bbwt_m2f_rle_lzw

import os

# declare path of test files
PATH_DIR_TEST_FILES = os.path.join(os.getcwd(), "files")
# declare alphabet
ALPHABET: list[chr] = [chr(i) for i in range(128)]

# for each file inside files directory
for file_name in os.listdir(PATH_DIR_TEST_FILES):
    # HUFFMAN TEST
    huffman(PATH_DIR_TEST_FILES, file_name)
    bwt_m2f_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bwt_m2f_rle_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_rle_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)

    # ARITHMETIC-CODING TEST
    arithmetic_coding(PATH_DIR_TEST_FILES, file_name)
    bwt_m2f_arithmetic_coding(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_arithmetic_coding(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bwt_m2f_rle_arithmetic_coding(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_rle_arithmetic_coding(PATH_DIR_TEST_FILES, file_name, ALPHABET)

    # LZW TEST
    lzw(PATH_DIR_TEST_FILES, file_name)
    bwt_m2f_lzw(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_lzw(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bwt_m2f_rle_lzw(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_rle_lzw(PATH_DIR_TEST_FILES, file_name, ALPHABET)
