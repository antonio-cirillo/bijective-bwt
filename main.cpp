#include <string>
#include <string.h>
#include <vector>
#include <iostream>
#include <filesystem>
#include <fstream>

#include "bwtEncode.hpp"
#include "bwtDecode.hpp"

#include "bbwtEncode.hpp"
#include "bbwtDecode.hpp"

#include "m2f.cpp"
#include "rle.hpp"

#include "huffman.hpp"
#include "arithmetic_code.hpp"

// define MODE
#define COMPRESS 0
#define DECOMPRESS 1

// define PIPELINE
#define HUFFMAN                             0
#define ARITHMETIC_CODE                     1
#define BWT_M2F_HUFFMAN                     2
#define BWT_M2F_ARITHMETIC_CODE             3
#define BBWT_M2F_HUFFMAN                    4
#define BBWT_M2F_ARITHMETIC_CODE            5
#define BWT_M2F_RLE_HUFFMAN                 6
#define BWT_M2F_RLE_ARITHMETIC_CODE         7
#define BBWT_M2F_RLE_HUFFMAN                8
#define BBWT_M2F_RLE_ARITHMETIC_CODE        9
#define RLE_BWT_M2F_RLE_HUFFMAN             10
#define RLE_BWT_M2F_RLE_ARITHMETIC_CODE     11
#define RLE_BBWT_M2F_RLE_HUFFMAN            12
#define RLE_BBWT_M2F_RLE_ARITHMETIC_CODE    13

#define N_PIPELINES 14 

#define CHUNK_SIZE 50000

namespace fs = std::filesystem;
using namespace std;

bool compareFiles(const std::string& p1, const std::string& p2) {
  std::ifstream f1(p1, std::ifstream::binary|std::ifstream::ate);
  std::ifstream f2(p2, std::ifstream::binary|std::ifstream::ate);

  if (f1.fail() || f2.fail()) {
    return false; // file problem
  }

  if (f1.tellg() != f2.tellg()) {
    return false; // size mismatch
  }

  // seek back to beginning and use std::equal to compare contents
  f1.seekg(0, std::ifstream::beg);
  f2.seekg(0, std::ifstream::beg);
  return std::equal(std::istreambuf_iterator<char>(f1.rdbuf()),
                    std::istreambuf_iterator<char>(),
                    std::istreambuf_iterator<char>(f2.rdbuf()));
}


int main(int argc, char* argv[]) {

    int OPERATION;
    int PIPELINE;

    if (argc == 5) {

        // get mode of use
        if (strcmp(argv[1], "-c") == 0)
            OPERATION = COMPRESS;
        else if (strcmp(argv[1], "-d") == 0)
            OPERATION = DECOMPRESS;
        else {
            cout << "Using: main <-c/-d> <pipeline> <input_of_file> <output_file>" << endl;
		    return -1;
        }

        // define array of all pipelins
        int PIPELINES[N_PIPELINES] = {
            HUFFMAN,
            ARITHMETIC_CODE,
            BWT_M2F_HUFFMAN,
            BWT_M2F_ARITHMETIC_CODE,
            BBWT_M2F_HUFFMAN,
            BBWT_M2F_ARITHMETIC_CODE,
            BWT_M2F_RLE_HUFFMAN,
            BWT_M2F_RLE_ARITHMETIC_CODE,
            BBWT_M2F_RLE_HUFFMAN,
            BBWT_M2F_RLE_ARITHMETIC_CODE,
            RLE_BWT_M2F_RLE_HUFFMAN,
            RLE_BWT_M2F_RLE_ARITHMETIC_CODE,
            RLE_BBWT_M2F_RLE_HUFFMAN,
            RLE_BBWT_M2F_RLE_ARITHMETIC_CODE 
        };

        int indexPipeline;
        sscanf(argv[2], "%d", &indexPipeline);
        if (indexPipeline < 0 || indexPipeline > N_PIPELINES) {
            cout << "The specified pipeline does not exist" << endl;
		    return -1;
        } else
            PIPELINE = PIPELINES[indexPipeline];

        // open input file
        ifstream file(argv[3]);
        if (!file) {
            cout << argv[3] << ": No such file or directory" << endl;
		    return -1;
        }

        // open output file
        ofstream out_file;
        out_file.open(argv[4], ios::binary | ios::out);
        if (!out_file) {
            cout << argv[4] << ": No such file or directory" << endl;
		    return -1;
        }

        // read all file
        string data((istreambuf_iterator<char>(file)),
            istreambuf_iterator<char>());
        file.close();

        // init string compressed/decompressed
        string output;

        // apply function
        switch(OPERATION) {

            case COMPRESS: {
        
                switch(PIPELINE) {

                    case HUFFMAN: {
                        cout << "Pipeline: Huffman" << endl;
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compress();
                        break;
                    }

                    case ARITHMETIC_CODE: {
                        cout << "Pipeline: Arithmetic Coding" << endl;
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encode(argv[3], argv[4]);
                        break;
                    }

                    case BWT_M2F_HUFFMAN: {
                        cout << "Pipeline: BWT -> M2F -> Huffman" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_encoded = bwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bwt_encoded = bwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compressData(output);
                        break;
                    }

                    case BWT_M2F_ARITHMETIC_CODE: {
                        cout << "Pipeline: BWT -> M2F -> Arithmetic Coding" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_encoded = bwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bwt_encoded = bwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encodeData(output, argv[4]);
                        break;
                    }

                    case BBWT_M2F_HUFFMAN: {
                        cout << "Pipeline: Bijective BWT -> M2F -> Huffman" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_encoded = bbwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_encoded = bbwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compressData(output);
                        break;
                    }

                    case BBWT_M2F_ARITHMETIC_CODE: {
                        cout << "Pipeline: Bijective BWT -> M2F -> Arithmetic Coding" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_encoded = bbwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_encoded = bbwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encodeData(output, argv[4]);
                        break;
                    }

                    case BWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: BWT -> M2F -> RLE -> Huffman" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_encoded = bwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bwt_encoded = bwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compressData(output);
                        break;
                    }

                    case BWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_encoded = bwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bwt_encoded = bwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encodeData(output, argv[4]);
                        break;
                    }

                    case BBWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: Bijective BWT -> M2F -> RLE -> Huffman" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_encoded = bbwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_encoded = bbwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compressData(output);
                        break;
                    }

                    case BBWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: Bijective BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_encoded = bbwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_encoded = bbwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encodeData(output, argv[4]);
                        break;
                    }

                    case RLE_BWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: RLE -> BWT -> M2F -> RLE -> Huffman" << endl;
                        data = RunLengthEncoding(data);
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_encoded = bwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bwt_encoded = bwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compressData(output);
                        break;
                    }

                    case RLE_BWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: RLE -> BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        data = RunLengthEncoding(data);
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_encoded = bwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bwt_encoded = bwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encodeData(output, argv[4]);
                        break;
                    }

                    case RLE_BBWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: RLE -> Bijective BWT -> M2F -> RLE -> Huffman" << endl;
                        data = RunLengthEncoding(data);
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_encoded = bbwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_encoded = bbwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        huffman huffman_encoder(argv[3], argv[4]);
                        huffman_encoder.compressData(output);
                        break;
                    }

                    case RLE_BBWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: RLE -> Bijective BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        data = RunLengthEncoding(data);
                        unsigned long size = data.size();
                        unsigned long nPerfectChunk = size / CHUNK_SIZE;
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_encoded = bbwtEncode(data.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_encoded = bbwtEncode(data.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_encoded;
                        }
                        MTF m2f;
                        output = m2f.encode(output);
                        output = rleEncode(output);
                        Encode arithmetic_encoder;
                        arithmetic_encoder.encodeData(output, argv[4]);
                        break;
                    }

                }            
            }
            break;

            case DECOMPRESS: {
                
                switch (PIPELINE) {                    
                    
                    case HUFFMAN: {
                        cout << "Pipeline: Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        huffman_decoder.decompress();
                        break;
                    }

                    case ARITHMETIC_CODE: {
                        cout << "Pipeline: Arithmetic Coding" << endl;
                        Decode arithmetic_decoder;
                        arithmetic_decoder.decode(argv[3], argv[4]);
                        break;
                    }

                    case BWT_M2F_HUFFMAN: {
                        cout << "Pipeline: BWT -> M2F -> Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        data = huffman_decoder.decompressData();
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE + 1);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(i * (CHUNK_SIZE + 1), (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        if ((nPerfectChunk * (CHUNK_SIZE + 1)) < size) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(nPerfectChunk * (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                    case BWT_M2F_ARITHMETIC_CODE: {
                        cout << "Pipeline: BWT -> M2F -> Arithmetic Coding" << endl;
                        Decode arithmetic_decoder; 
                        data = arithmetic_decoder.decodeData(argv[3]);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE + 1);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(i * (CHUNK_SIZE + 1), (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        if ((nPerfectChunk * (CHUNK_SIZE + 1)) < size) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(nPerfectChunk * (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                case BBWT_M2F_HUFFMAN: {
                        cout << "Pipeline: Bijective BWT -> M2F -> Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        data = huffman_decoder.decompressData();
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                case BBWT_M2F_ARITHMETIC_CODE: {
                        cout << "Pipeline: Bijective BWT -> M2F -> Arithmetic Coding" << endl;
                        Decode arithmetic_decoder; 
                        data = arithmetic_decoder.decodeData(argv[3]);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                    case BWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: BWT -> M2F -> RLE -> Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        data = huffman_decoder.decompressData();
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE + 1);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(i * (CHUNK_SIZE + 1), (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        if ((nPerfectChunk * (CHUNK_SIZE + 1)) < size) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(nPerfectChunk * (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                    case BWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        Decode arithmetic_decoder; 
                        data = arithmetic_decoder.decodeData(argv[3]);
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE + 1);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(i * (CHUNK_SIZE + 1), (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        if ((nPerfectChunk * (CHUNK_SIZE + 1)) < size) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(nPerfectChunk * (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                case BBWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: Bijective BWT -> M2F -> RLE -> Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        data = huffman_decoder.decompressData();
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                case BBWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: Bijective BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        Decode arithmetic_decoder; 
                        data = arithmetic_decoder.decodeData(argv[3]);
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        out_file << output;
                        break;
                    }

                case RLE_BWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: RLE -> BWT -> M2F -> RLE -> Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        data = huffman_decoder.decompressData();
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE + 1);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(i * (CHUNK_SIZE + 1), (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        if ((nPerfectChunk * (CHUNK_SIZE + 1)) < size) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(nPerfectChunk * (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        output = RunLengthDecoding(output);
                        out_file << output;
                        break;
                    }

                case RLE_BWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: RLE -> BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        Decode arithmetic_decoder; 
                        data = arithmetic_decoder.decodeData(argv[3]);
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE + 1);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(i * (CHUNK_SIZE + 1), (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        if ((nPerfectChunk * (CHUNK_SIZE + 1)) < size) {
                            string bwt_decoded = bwtDecode(m2f_decoded.substr(nPerfectChunk * (CHUNK_SIZE + 1)));
                            output += bwt_decoded;
                        }
                        output = RunLengthDecoding(output);
                        out_file << output;
                        break;
                    }

                case RLE_BBWT_M2F_RLE_HUFFMAN: {
                        cout << "Pipeline: RLE -> Bijective BWT -> M2F -> RLE -> Huffman" << endl;
                        huffman huffman_decoder(argv[3], argv[4]);
                        data = huffman_decoder.decompressData();
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        output = RunLengthDecoding(output);
                        out_file << output;
                        break;
                    }

                case RLE_BBWT_M2F_RLE_ARITHMETIC_CODE: {
                        cout << "Pipeline: RLE -> Bijective BWT -> M2F -> RLE -> Arithmetic Coding" << endl;
                        Decode arithmetic_decoder; 
                        data = arithmetic_decoder.decodeData(argv[3]);
                        data = rleDecode(data);
                        MTF m2f;
                        string m2f_decoded = m2f.decode(data);
                        unsigned long size = m2f_decoded.size();
                        unsigned long nPerfectChunk = size / (CHUNK_SIZE);
                        for(unsigned long i = 0; i < nPerfectChunk; i++) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(i * CHUNK_SIZE, CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        if ((nPerfectChunk * CHUNK_SIZE) < size) {
                            string bbwt_decoded = bbwtDecode(m2f_decoded.substr(nPerfectChunk * CHUNK_SIZE));
                            output += bbwt_decoded;
                        }
                        output = RunLengthDecoding(output);
                        out_file << output;
                        break;
                    }

                }
            }
        }

        // close output file
        out_file.close();

    } 

    else {
        cout << "Using: main <-c/-d> <pipeline> <input_of_file> <output_file>" << endl;
		return -1;
    }

}