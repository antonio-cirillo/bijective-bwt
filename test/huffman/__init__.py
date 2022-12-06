import os.path as path
import os

COMPRESSED_HUFFMAN_DIR_PATH: str = path.join(os.getcwd(), 'compressed', 'huffman')
COMPRESSED_HUFFMAN_FILE_NAME: str = "{name}_{pre_processing}_huffman"


def generate_file_name(name: str, pre_processing: str) -> str:
    return COMPRESSED_HUFFMAN_FILE_NAME.format(name=name, pre_processing=pre_processing)
