import os.path as path
import os

COMPRESSED_ARITHMETIC_CODING_DIR_PATH: str = path.join(os.getcwd(), 'compressed', 'arithmetic_coding')
DECOMPRESSED_ARITHMETIC_CODING_DIR_PATH: str = path.join(os.getcwd(), 'decompressed', 'arithmetic_coding')
COMPRESSED_ARITHMETIC_CODING_FILE_NAME: str = "{name}_{pre_processing}_arithmetic_coding"


def generate_file_name(name: str, pre_processing: str) -> str:
    return COMPRESSED_ARITHMETIC_CODING_FILE_NAME.format(name=name, pre_processing=pre_processing)
