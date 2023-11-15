import sys
import random

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


# Inputs: Flow to record, registers to record in
# Returns: None
# Description: Hashes and records the geometric hash + 1 of all elements of a flow into the given registers
def record_flow(flow, registers):
    # Hashing and recording each element of flow
    for element in flow:
        # Finding the geometric hash (G) of a hashed value using current element
        g = geometric_hash(hash_function(element, 4, len(registers)))
        # Want G' = G + 1 for recording
        g_prime = g+1
                
        # Hashing element to a register using a different hash function
        hash_value = hash_function(element, 6, len(registers))
        # Updating register with new g_prime if it's larger
        registers[hash_value] = max(registers[hash_value], g_prime)
# record_flows()


# Inputs: Registers to estimate flow spread in
# Returns: Estimated flow spread
# Description: Estimate spread of a flow in the registers using the formula for HLL Sketch querying
def estimate_flow_spread(registers):
    estimated_flow_spread = 0

    # Constants
    m = len(registers)
    alpha = 0.7213/(1 + 1.079/m)

    # Calculating estimated flow using formula for HLL Sketch querying
    for register_value in registers:
        estimated_flow_spread += 1/(2 ** register_value)
    estimated_flow_spread = estimated_flow_spread ** -1
    estimated_flow_spread = estimated_flow_spread * (m ** 2) * alpha

    # Returning the estimated flow spread
    return estimated_flow_spread
# estimate_flow_spread()


# Inputs: Id of flow to hash, what size parts to split id into, number of registers
# Returns: Hash value result of element id
# Description: Folding hash function implementation based from https://www.herevego.com/hashing-python/
#   Split id into a number of parts based on given step size and then add them together
#   Hash function changes depending on step size
def hash_function(element_id, step_size, num_registers):
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
    return split_id_sum % num_registers
# hash_function()


# Inputs: Hashed element id
# Returns: Geometric hash of input
# Description: Calculates the geometric hash of the input value by calculating how many leading 0s are in the binary form of the number
#              Maximum number of bits is 8 for m = 256
def geometric_hash(id):
    # Obtaining binary form of input and removing prefix
    binary_form = bin(id)[2:]
    
    # Calculating how many leading 0s are present
    g = 8 - len(binary_form)
    
    #Returning geometric hash value
    return g
# geometric_hash()


main()