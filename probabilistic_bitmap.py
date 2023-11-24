import sys
import random
import math

def main():

    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 3:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./probabilistic_bitmap.py number_bits_in_bitmap sampling_probability'")
        return
    
    # Setting input parameters
    num_bits_in_bitmap = int(sys.argv[1])
    sampling_probability = float(sys.argv[2])

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
         record_flow(flow, bitmap, sampling_probability)

         # Estimating spread of current flow after recording
         estimated_flow_spreads.append(estimate_flow_spread(bitmap, sampling_probability))
        
        # Resetting bitmap
         for index in range(len(bitmap)):
            bitmap[index] = 0

    # Printing output
    for index in range(len(flows)):
        print("True flow spread: " + str(flow_spreads[index]) + "      Estimated flow spread: " + str(estimated_flow_spreads[index]))


# Inputs: Flow to record, bitmap to record flow in
# Returns: None
# Description: Hashes and records all elements of a flow into the given bitmap
def record_flow(flow, bitmap, sampling_probability):
    # Hashing and recording each element of flow
    for element in flow:
        # If the hash value falls under the set probability, hash to an entry
        if hash_function(element, 4, len(bitmap)) < len(bitmap)*sampling_probability:
             bitmap[hash_function(element, 6, len(bitmap))] = 1
# record_flows()


# Inputs: Bitmap to estimate flow spread in
# Returns: Estimated flow spread
# Description: Estimate spread of a flow in a bitmap using formula -mln(v), where u = number of 0s in bitmap and v = u/(bitmap length)
def estimate_flow_spread(bitmap, sampling_probability):
    # u = number of 0s in bitmap
    u = bitmap.count(0)
    # v = percentage of 0s in bitmap
    v = u/len(bitmap)
    # Potentially correcting v to estimate bounds to prevent error
    if v == 0:
        v = 1/len(bitmap)

    return -(len(bitmap)/sampling_probability)*math.log(v)
# estimate_flow_spread()


# Inputs: Id of flow to hash, what size parts to split id into, bitmap size
# Returns: Index in bitmap where element should be recorded to
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split id into a number of parts based on given step size and then add them together
#   Hash function changes depending on step size
def hash_function(element_id, step_size, bitmap_size):
    # If id is too short than error will occur; fixing here
    if element_id < 10**(step_size):
        element_id += 10**(step_size)

    # Pointer to current position of number
    int_pos = 0
    # Total sum of the split id
    split_id_sum = 0
    # Creating parts until there's no number left
    while int_pos < len(str(element_id)):
        # Making sure index isn't out of bounds
        if int_pos + step_size < len(str(element_id)):
            split_id_part = str(element_id)[int_pos:int_pos + step_size]
        else:
            split_id_part = str(element_id)[int_pos:]
        
        # Incrementing number position pointer
        int_pos = int_pos + step_size
        split_id_sum += int(split_id_part)

    # Returning hashed position
    return split_id_sum % bitmap_size
# hash_function()


main()
