from test.huffman.huffman import huffman
from test.huffman.bwt_m2f_huffman import bwt_m2f_huffman
from test.huffman.bbwt_m2f_huffman import bbwt_m2f_huffman
from test.huffman.bwt_m2f_rle_huffman import bwt_m2f_rle_huffman
from test.huffman.bbwt_m2f_rle_huffman import bbwt_m2f_rle_huffman

import os

# declare path of test files
PATH_DIR_TEST_FILES = os.path.join(os.getcwd(), "files")
# declare alphabet
ALPHABET: list[chr] = [chr(i) for i in range(128)]

# for each file inside files directory
for file_name in os.listdir(PATH_DIR_TEST_FILES):
    huffman(PATH_DIR_TEST_FILES, file_name)
    bwt_m2f_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bwt_m2f_rle_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
    bbwt_m2f_rle_huffman(PATH_DIR_TEST_FILES, file_name, ALPHABET)
