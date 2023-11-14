import sys
import random
import math

def main():

    # Checking that the correct number of arguments was passed in
    if len(sys.argv) != 2:
        print("Invalid number of arguments")
        print("Program should be run in form 'python ./hyperLogLog.py num_registers'")
        return
    
    # Setting input parameter
    num_registers = int(sys.argv[1])

    # Creating registers
    registers = [0] * num_registers

    # Generating flows
    flows = []
    flow_spreads = [1000, 10000, 100000, 1000000]
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
        record_flow(flow, registers)

        # Estimating spread of current flow after recording
        estimated_flow_spreads.append(estimate_flow_spread(registers))
        
        # Resetting registers
        for index in range(len(registers)):
            registers[index] = 0

    # Printing output
    for index in range(len(flows)):
        print("True flow spread: " + str(flow_spreads[index]) + "      Estimated flow spread: " + str(estimated_flow_spreads[index]))


# Inputs: Flow to record, bitmap to record flow in
# Returns: None
# Description: Hashes and records all elements of a flow into the given bitmap
def record_flow(flow, registers):
    # Hashing and recording each element of flow
    for element in flow:
        hash_value = hash_function(element, len(registers))
        g = geometric_hash(hash_value)
        g_prime = g+1

        if registers[hash_value] < g_prime:
            registers[hash_value] = g_prime

        #print(hash_value)
        #print(g_prime)
# record_flows()


# Inputs: Bitmap to estimate flow spread in
# Returns: Estimated flow spread
# Description: Estimate spread of a flow in a bitmap using formula -mln(v), where u = number of 0s in bitmap and v = u/(bitmap length)
def estimate_flow_spread(registers):
    
    estimated_flow_spread = 0
    
    m = len(registers)
    alpha = 0.7213/(1+1.079/m)

    for index in range(m):
        estimated_flow_spread += 1/(2**registers[index])

    estimated_flow_spread = estimated_flow_spread ** -1
    estimated_flow_spread = estimated_flow_spread * (m ** 2) * alpha

    return estimated_flow_spread
# estimate_flow_spread()

# Inputs: Id of element to hash, size of bitmap in bits
# Returns: Bitmap bit position where element encodes to
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split number into two (first four digits, and then rest of number)
#   Add two parts and then do num % num_table_entries
def hash_function(element_id, register_size):
    # Error if id isn't more than four digits long; correcting here
    if element_id < 10000:
            element_id += 10000

    # Hashing into a bitmap position
    split_id_sum = int(str(element_id)[:4]) + int(str(element_id)[4:])
    return split_id_sum % register_size
# hash_function()


def geometric_hash(id):
    g = 0
    binary_form = bin(id)[2:]
    #print(binary_form)

    g += 8 - len(binary_form)

    return g

main()