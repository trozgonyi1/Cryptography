import numpy as np
import lfsr

permutation = {1:54,2:57,3:35,4:36,5:6,6:55,7:40,8:10,9:14,10:3,11:30,12:28,13:18,14:63,15:64,16:38,17:39,18:8,19:1,20:49,21:16,22:26,23:48,24:37,25:51,26:34,27:22,28:42,29:12,30:4,31:41,32:60,33:52,34:13,35:31,36:9,37:25,38:29,39:2,40:33,41:17,42:46,43:11,44:32,45:23,46:56,47:20,48:50,49:24,50:47,51:53,52:5,53:27,54:62,55:44,56:61,57:7,58:45,59:43,60:15,61:58,62:59,63:19,64:21}

def inverse(num):
    f_x = np.array([1,0,0,0,1,1,1,0,1])
    _, remainder = np.polydiv(num, f_x)
    remainder = [i%2 for i in list(remainder)]
    if len(remainder) < 8:
        padding = 8 - len(remainder)
        padd = np.zeros(padding, dtype=int).tolist()
        for i in remainder:
            padd.append(int(i))

        remainder = padd
    return remainder

def s_box(input_vec):
    input_vec = [int(i) for i in input_vec]
    vec = np.uint32(input_vec)
    if np.sum(vec) == 0:
        return [0,0,0,0,0,0,0,0,0]

    return inverse(vec)

def apply_s_box(total_in):
    iterable = __unflatten(total_in)
    for ind, val in enumerate(iterable):
        iterable[ind] = s_box(val)
    iterable = __flatten(iterable)
    return iterable

def key_schedule(N):
    keys = []
    output, _, _ = lfsr.lfsr(8+64*6, [0,0,0,0,1,1,1,1], [1,0,1,0,1,1,1,0], 2, False)
    output = output[9:]
    for i in range(N + 1):
        keys.append(output[64*i: 64*(i+1)])
    
    return keys 

def key_addition(key, inpt):
    output = []
    for index, value in enumerate(inpt):
        output.append((key[index%len(key)] + value) % 2)
    return output

def pad_string(string):
    padding_needed = len(string) % 64
    for i in range(padding_needed):
        string.append(0)
    return string

def pi_p(input_string):
    new_string = []
    for i in range(len(input_string) // 64):
        for j in range(1, 65):
            new_string.append(input_string[permutation[j] - 1])

    return new_string

def encryption(x, sub, perm, keys):
    w_0 = x
    for r in range(len(keys)-1):
        pass

def __flatten(_2d_binary):
    flat = []
    for i in _2d_binary:
        if type(i) == int:
            for k in range(7):
                pass
        for j in i:
            flat.append(int(j))
    return flat

def __unflatten(flat):
    out = []
    counter = 0
    temp = []
    for i in flat:
        if counter == 8:
            out.append(temp)
            temp = []
            counter = 0 

        temp.append(i)
        counter += 1
    if len(temp) == 8:
        out.append(temp)
    while len(temp) < 8:
        temp.append(0)
    return out

if __name__ == '__main__':
    print('Input: "If you can dream it, you can do it". Thanks to #@Walt-Disney')
    string_input = [format(ord(i), '08b') for i in '"If you can dream it, you can do it". Thanks to #@Walt-Disney']
    string_input = [list(i) for i in string_input]
    for ind, val in enumerate(string_input):
        for ind2, val2 in enumerate(val):
            string_input[ind][ind2] = int(string_input[ind][ind2])
    
    keys = key_schedule(5)
    u_r = []
    string_input = __flatten(string_input)
    string_input = pad_string(string_input)
    for i in range(1, 5):
        print(''*5, "Applying key", i)
        u_r.append(key_addition(keys[i-1], string_input))
        print(''*5, 'applying s box')
        string_input = apply_s_box(u_r[-1])
        print(''*5, 'applying permutation')
        string_input = pi_p(string_input)

    print(''*5, 'Applying key 5')
    u_r.append(key_addition(keys[5 - 1], string_input))

    print(''*5, 'applying s box')
    string_input = apply_s_box(u_r[-1])
    
    print(''*5, 'Applying key 6')
    final = key_addition(keys[5], string_input)
    final_to_text = __unflatten(final)
    text = []
    for i in final_to_text:
        text.append(chr(int("".join(map(str, i)), 2)))

    final_encrypted = "".join(text)
    print("Final encrypted string: \n", final_encrypted)
    write = input("Would you like to write the final string to a file? (y/n): ")
    if write == 'y':
        with open('output.txt', 'w') as file:
            file.write(final_encrypted)
        
