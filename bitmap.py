import sys
import random
import math

def main():

    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./bitmap.py number_bits_in_bitmap'")
        return
    
    # Setting input parameters
    num_bits_in_bitmap = int(sys.argv[1])

    # Creating Bitmap
    bitmap = [0] * num_bits_in_bitmap

    # Generating flows
    flows = []
    flow_spreads = [100, 1000, 10000, 100000, 1000000]
    for flow_spread in flow_spreads:
        flow = []
        for index in range(flow_spread):
            element_id = random.randrange(1000000000)
            flow.append(element_id)

        flows.append(flow)
    
    # Estimated flow spreads
    estimated_flow_spreads = []

    # Recording flows
    for flow in flows:
         record_flow(flow, bitmap)

         # Estimating spread of current flow after recording
         estimated_flow_spreads.append(estimate_flow_spread(bitmap))
        
        # Resetting bitmap
         for index in range(len(bitmap)):
            bitmap[index] = 0

    # Printing output
    for index in range(len(flows)):
        print("True flow spread: " + str(flow_spreads[index]) + "      Estimated flow spread: " + str(estimated_flow_spreads[index]))


# Inputs: Flow to record, bitmap to record flow in
# Returns: None
# Description: Hashes and records all elements of a flow into the given bitmap
def record_flow(flow, bitmap):
    # Hashing and recording each element of flow
    for element in flow:
        bitmap[hash_function(element, len(bitmap))] = 1
# record_flows()


# Inputs: Bitmap to estimate flow spread in
# Returns: Estimated flow spread
# Description: Estimate spread of a flow in a bitmap using formula -mln(v), where u = number of 0s in bitmap and v = u/(bitmap length)
def estimate_flow_spread(bitmap):
     # u = number of 0s in bitmap
     u = bitmap.count(0)
     # v = percentage of 0s in bitmap
     v = u/len(bitmap)
     # Potentially correcting v to estimate bounds to prevent error
     if v == 0:
         v = 1/len(bitmap)

     return -len(bitmap)*math.log2(v)
# estimate_flow_spread()


# Inputs: Id of element to hash, size of bitmap in bits
# Returns: Bitmap bit position where element encodes to
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split number into two (first four digits, and then rest of number)
#   Add two parts and then do num % num_table_entries
def hash_function(element_id, bitmap_size):
    # Error if id isn't more than four digits long; correcting here
    if element_id < 10000:
            element_id += 10000

    # Hashing into a bitmap position
    split_id_sum = int(str(element_id)[:4]) + int(str(element_id)[4:])
    return split_id_sum % bitmap_size
# hash_function()


main()
