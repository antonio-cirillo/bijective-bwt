import os
import os.path as path
import time
from matplotlib import pyplot as plt

import numpy as np
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

def plot_time_different_pipeline(file_name: str, results: [dict]):
    os.makedirs('images', exist_ok=True)
    _file_name = f'{file_name}.jpg'

    file_path: str = os.path.join('images', _file_name)

    times_compress = [r1["compression_time"] for r1 in results]
    times_decompress = [r2["decompression_time"] for r2 in results]
    pipelines = [r["pipeline"] for r in results]
    x_pos = np.arange(len(pipelines))

    

    #create plot
    plt.plot(x_pos, times_compress, 'r',label='compression')
    plt.plot(x_pos, times_compress,'ro')

    plt.plot(x_pos, times_decompress, 'b',label='decompression')
    plt.plot(x_pos, times_decompress,'bo')
    plt.legend()

    #rotation of the bar names
    plt.xticks(x_pos, pipelines, rotation = 90)
    #custom the subplot layout
    plt.subplots_adjust(bottom=0.4, top=0.9)

    plt.title(file_name)
    plt.xlabel('pipeline')
    plt.ylabel('time')

    x_locs, x_labs = plt.xticks()
    for i, v in enumerate(times_compress):
        plt.text(x_locs[i] - 0.02, v +0.3, str(v))
    for i, v in enumerate(times_decompress):
        plt.text(x_locs[i] - 0.02, v +0.3, str(v))
    plt.ylim(0, max(max(times_compress),max(times_decompress))+1 + 0.3)
    plt.savefig(file_path)
    plt.clf()

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


map_results_huffman = []
map_results_arith = []
for file_name in os.listdir(PATH_DIR_TEST_FILES):
    for pipe in range(len(pipelines)):

        abspath_file = os.path.join(PATH_DIR_TEST_FILES, file_name)
        abspath_compressed_file = os.path.join(COMPRESSED_DIR_PATH, generate_file_name(os.path.splitext(file_name)[0],pipelines[pipe]))
        abspath_decompressed_file = os.path.join(DECOMPRESSED_DIR_PATH, generate_file_name(os.path.splitext(file_name)[0],pipelines[pipe]))

        start_time = time.time()
        
        os.system(f'./main -c {pipe} {abspath_file} {abspath_compressed_file}')
        compression_time = round((time.time() - start_time)*1000)


        start_time = time.time()
        os.system(f'./main -d {pipe} {abspath_compressed_file} {abspath_decompressed_file}')
        decompression_time = round((time.time() - start_time)*1000)
        if (pipelines[pipe].find("HUFFMAN")!= -1):
            result_huffman = dict()
            result_huffman["pipeline"] = pipelines[pipe]
            result_huffman["compression_ratio"] = compression_ratio_from_file(abspath_file,abspath_compressed_file)
            result_huffman["compression_time"] = compression_time
            result_huffman["filename"] = file_name
            result_huffman["decompression_time"] = decompression_time
            #lista_huffman = []
            #lista_huffman.append(result_huffman)
            map_results_huffman.append(result_huffman)
        else:
            result_arith = dict()
            result_arith["pipeline"] = pipelines[pipe]
            result_arith["compression_ratio"] = compression_ratio_from_file(abspath_file,abspath_compressed_file)
            result_arith["compression_time"] = compression_time
            result_arith["filename"] = file_name
            result_arith["decompression_time"] = decompression_time
            #lista_arith = []
            #lista_arith.append(result_arith)
            map_results_arith.append(result_arith)

    
    #_result_huffman = [r for r in map_results_huffman]
    plot_time_different_pipeline(file_name+"_huffman",map_results_huffman)
    #_result_arithm = [r for r in map_results_arith]
    plot_time_different_pipeline(file_name+"_arithm", map_results_arith)
    map_results_arith.clear()
    map_results_huffman.clear()

#print("\n\n\n map \n\n\n",map_results)




