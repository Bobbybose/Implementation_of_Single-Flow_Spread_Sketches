# CS685 - Internet Data Streaming 
# Project 4 - Implementation of Single-Flow Spread Sketches
**Author:** Bobby Bose

## Description
- This is an implementation of a Bitmap, Probabilistic Bitmap, and a HyperLogLog (HLL)Sketch
- There are three Python scripts, one for each sketch
- An example output is given in three output (.out) files
- Hash function used in all code was based off of the folding method from https://www.herevego.com/hashing-python/

## Required Packages and Modules
- No external packages required 
- The only required modules are the sys, random, and math modules built into Python

## Bitmap
- To run, do 'python ./bitmap.py number_bits_in_bitmap'
- **Architecture Operation:**
    - Bitmap has a given number of bits
    - Each element is hashed to one bit in the bitmap
    - When querying, estimate flow spread using formula: n_f = -mln(v)
        - m = # bits in bitmap
        - v = fraction of bits in bitmap that are zeros
- **Program Flow**
    - Generate 5 flows with spreads 100, 1000, 10000, 100000, 1000000
    - Records each flow in bitmap and then queries for estimated flow spread
    - Bitmap resets after each record and query
- **Output:**
    - Line for each flow with true flow spread and estimated flow spread

## Probabilistic Bitmap
- To run, do 'python ./probabilistic_bitmap.py number_bits_in_bitmap sampling_probability'
- **Architecture Operation:**
    - Bitmap has a given number of bits
    - Each element is hashed to one bit in the bitmap based on a given sampling probability
        - If hashed value < maximum hash value * sampling probability, then hash to an entry using another hash
    - When querying, estimate flow spread using formula: n_f = -(m/p)ln(v)
        - m = # bits in bitmap
        - v = fraction of bits in bitmap that are zeros
        - p = sampling probability
- **Program Flow**
    - Generate 5 flows with spreads 100, 1000, 10000, 100000, 1000000
    - Records each flow in bitmap and then queries for estimated flow spread
    - Bitmap resets after each record and query
- **Output:**
    - Line for each flow with true flow spread and estimated flow spread

## HyperLogLog (HLL) Sketch
- To run, do 'python ./hyperLogLog.py num_registers'
- **Architecture Operation:**
    - Sketch is a given number of registers, each 5 bits
    - Each element is hashed, and then the geometric hash is taken of that value
    - Another hash is used to select a register for the element
    - If geometric hash is larger than what is already recorded, then replace with new value
    - When querying, estimate flow spread using formula: n_f = alpha * m^2 * sum(1/(2^B[i]) for 0 <= i <= m-1)^-1
        - m = number of registers
        - alpha = 0.7213/(1 + 1.079/m)
        - B = set of registers
- **Program Flow**
    - Generate 4 flows with spreads 1000, 10000, 100000, 1000000
    - Records each flow in HLL Sketch and then queries for estimated flow spread
    - Registers reset after each record and query
- **Output:**
    - Line for each flow with true flow spread and estimated flow spread