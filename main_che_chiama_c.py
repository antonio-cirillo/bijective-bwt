import os
import os.path as path
import time
COMPRESSED_DIR_PATH: str = path.join(os.getcwd(), 'compressed')
DECOMPRESSED_DIR_PATH: str = path.join(os.getcwd(), 'decompressed')

def generate_file_name(name: str,pipeline: str) -> str:
    return name+"_"+pipeline

def compression_ratio_from_file(uncompressed_path: str, compressed_path: str, decimal_digits=2) -> float:
    """ returns compression ratio for the input files. """
    uncompressed_size = os.path.getsize(uncompressed_path)
    compressed_size = os.path.getsize(compressed_path)

    if compressed_size == 0:
        return 0

    return round(uncompressed_size / compressed_size, decimal_digits)


PATH_DIR_TEST_FILES = os.path.join(os.getcwd(), "files")
os.makedirs(COMPRESSED_DIR_PATH, exist_ok = True)
os.makedirs(DECOMPRESSED_DIR_PATH, exist_ok = True)

pipelines = ["HUFFMAN",                             
"ARITHMETIC_CODE",                     
"BWT_M2F_HUFFMAN",                     
"BWT_M2F_ARITHMETIC_CODE",           
"BBWT_M2F_HUFFMAN",                  
"BBWT_M2F_ARITHMETIC_CODE",            
"BWT_M2F_RLE_HUFFMAN",                
"BWT_M2F_RLE_ARITHMETIC_CODE",       
"BBWT_M2F_RLE_HUFFMAN",             
"BBWT_M2F_RLE_ARITHMETIC_CODE",        
"RLE_BWT_M2F_RLE_HUFFMAN",           
"RLE_BWT_M2F_RLE_ARITHMETIC_CODE",   
"RLE_BBWT_M2F_RLE_HUFFMAN",          
"RLE_BBWT_M2F_RLE_ARITHMETIC_CODE"]    


map_results = []


for file_name in os.listdir(PATH_DIR_TEST_FILES):
    for pipe in range(len(pipelines)):

        abspath_file = os.path.join(PATH_DIR_TEST_FILES, file_name)
        abspath_compressed_file = os.path.join(COMPRESSED_DIR_PATH, generate_file_name(os.path.splitext(file_name)[0],pipelines[pipe]))
        abspath_decompressed_file = os.path.join(DECOMPRESSED_DIR_PATH, generate_file_name(os.path.splitext(file_name)[0],pipelines[pipe]))

        start_time = time.time()
        
        os.system(f'./main -c {pipe} {abspath_file} {abspath_compressed_file}')
        compression_time = round((time.time() - start_time)*1000)


        start_time = time.time()
        #a=(f'./main d {pipe} {abspath_compressed_file} {abspath_decompressed_file}')
        os.system(f'./main -d {pipe} {abspath_compressed_file} {abspath_decompressed_file}')
        decompression_time = round((time.time() - start_time)*1000)

        result = dict()
        result["filename"] = file_name
        result["pipeline"] = pipelines[pipe]
        result["compression_ratio"] = compression_ratio_from_file(abspath_file,abspath_compressed_file)
        result["compression_time"] = compression_time
        result["decompression_time"] = decompression_time
        lista = []
        lista.append(result)
        map_results.append(lista)
    



print("\n\n\n map \n\n\n",map_results)




