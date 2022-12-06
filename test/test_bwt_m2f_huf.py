from bwt.encode import encode as bwt_encode
from bwt.decode import decode as bwt_decode
from mtf.mtf import m2f_d, m2f_e
from huffman.huffman import huffman_decoding, huffman_encoding
from util.file import COMPRESSED_FILE_NAME
from util.file import write_compressed_file
from util.file import read_compressed_file
import string


def encode_bwt_m2f_huf(data, alphabet):
    alphabet = alphabet+["^"]+["|"]
    bwtencoded = bwt_encode(data)
    m2fencoded = m2f_e(bwtencoded,alphabet[::])
    huffencoded, tree = huffman_encoding(m2fencoded)
    return huffencoded, tree


def decode_bwt_m2f_huf(data, alphabet, tree):
    alphabet = alphabet+["^"]+["|"]
    huffdecoded = huffman_decoding(data, tree)
    m2fdecoded = m2f_d(huffdecoded, alphabet[::])
    bwtdecoded = bwt_decode(m2fdecoded)

    return bwtdecoded

if __name__ =="__main__":
    alphabet: str = list(string.ascii_letters)
    a,tree = encode_bwt_m2f_huf("banana",alphabet)
    print(a)
    dec_a = decode_bwt_m2f_huf(a, alphabet, tree)
    print(dec_a)