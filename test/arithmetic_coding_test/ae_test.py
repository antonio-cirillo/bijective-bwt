from compression.arithmetic_coding.arithmetic_coding import interface_compress,interface_decompress
from test.arithmetic_coding_test import COMPRESSED_ARITHMETIC_CODING_DIR_PATH, DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH
from test.arithmetic_coding_test import generate_file_name
import os
from util.file import write_compressed_file_path_folder
from util.file import write_decompressed_file_path_folder
PRE_PROCESSING: str = ""

def ae(file_path: str, file_name: str):

    # generate file name of compressed file
    _file_name: str = os.path.splitext(file_name)[0]
    compressed_file_name: str = generate_file_name(_file_name, PRE_PROCESSING)


    output_path = write_compressed_file_path_folder(COMPRESSED_ARITHMETIC_CODING_DIR_PATH,compressed_file_name)

    # use arithmetic encoding

    interface_compress((file_path+file_name), output_path)

    dec_output_path = write_decompressed_file_path_folder(DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH,compressed_file_name)

    # use arithmetic decoding
    interface_decompress(output_path, dec_output_path)


    return os.path.join(COMPRESSED_ARITHMETIC_CODING_DIR_PATH, compressed_file_name)


if __name__ == "__main__":
    ae("file/","pro.txt")

