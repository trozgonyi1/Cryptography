import numpy as np
import sys

def lfsr(iterations, coefficients, initial_state, modulus, debug):
    output = np.array(initial_state)
    state_vectors = set()
    periodic = -1
    repeated = tuple()
    if debug:
        print(initial_state)

    if len(coefficients) != len(initial_state):
        print("Invalid initial state")
        return (None, None, None)

    for i in range(iterations - len(initial_state)):
        next_out = next_term(coefficients, tuple(output[-(len(initial_state)+1)::]), modulus)
        next_out = next_out%modulus
        output = np.append(output, np.array(next_out))
        if tuple(output[-(len(initial_state)+1)::]) in state_vectors and periodic < 0:
            periodic = i
            repeated = tuple(output[-(len(initial_state)+1)::])
        state_vectors.add(tuple(output[-(len(initial_state)+1)::]))
        if debug:
            print("Current State Vector: ", output[-(len(initial_state)+1)::])
    if debug:
        print("-" * 30)
    if periodic != -1 and debug:
        print("The first state vector to be repeated is ", repeated)
        print("This linear recurrence relation is periodic with least period", periodic)

    return (output, state_vectors, periodic)

def next_term(coefficients, state, modulus):
    output = 0
    state_len = len(state)
    for ind, val in enumerate(coefficients):
        output += val*state[state_len - ind - 1]
    return (output) % modulus

def matrix_lfsr(interation):
    A = np.array([[0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1], [3,-1,0,1,0]])


if __name__ == '__main__':
    n = len(sys.argv)
    num_iterations = 30
    coef = []
    take_coef = False
    initial_vector = []
    take_vec = False
    mod = 5

    for ind, val in enumerate(sys.argv):
        if val == '-n':
            num_iterations = int(sys.argv[ind + 1])
            take_coef = False
            take_vec = False
        if val == '-c':
            take_coef = True
            take_vec = False
            continue
        if val == '-i':
            take_vec = True
            take_coef = False
            continue
        if val == '-m':
            take_coef = False
            take_vec = False
            mod = int(sys.argv[ind + 1])
            continue
        
        if take_coef:
            coef.append(int(val))
        if take_vec:
            initial_vector.append(int(val))

    if len(coef) == 0 or len(initial_vector) == 0 or len(coef) != len(initial_vector):
        print("USAGE: -n \{iterations\} -c \{coefficients\} -i \{initial vector\}")

    output, state_vectors, periodic = lfsr(num_iterations, coef, initial_vector, mod)
