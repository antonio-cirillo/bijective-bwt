import contextlib

from compression.arithmetic_coding import ae

def compress(inp, bitout):
    initfreqs = ae.FlatFrequencyTable(257)
    freqs = ae.SimpleFrequencyTable(initfreqs)
    enc = ae.ArithmeticEncoder(32, bitout)
    while True:
        # Read and encode one byte
        symbol = inp.read(1)
        if len(symbol) == 0:
            break
        enc.write(freqs, symbol[0])
        freqs.increment(symbol[0])
    enc.write(freqs, 256)  # EOF
    enc.finish()  # Flush remaining code bits


def decompress(bitin, out):
    initfreqs = ae.FlatFrequencyTable(257)
    freqs = ae.SimpleFrequencyTable(initfreqs)
    dec = ae.ArithmeticDecoder(32, bitin)
    while True:
        # Decode and write one byte
        symbol = dec.read(freqs)
        if symbol == 256:  # EOF symbol
            break
        out.write(bytes((symbol,)))
        freqs.increment(symbol)



def interface_compress(path,outputpath):
    with open(path, "rb") as inp, \
        contextlib.closing(ae.BitOutputStream(open(outputpath, "wb"))) as bitout:
        compress(inp, bitout)
def interface_decompress(path,outputpath):
    with open(path, "rb") as inp, open(outputpath, "wb") as out:
        bitin = ae.BitInputStream(inp)
        decompress(bitin, out)