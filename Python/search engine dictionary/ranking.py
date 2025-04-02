import sys
import pickle
import copy

args = sys.argv
iterations = args[2]
dict_file = args[3]
out_file = args[4]

with open(dict_file, 'rb') as f:
    d = pickle.load(f)
LIST_OF_KEYS = d.keys()

def key_number_of_outgoing():
    outgoings_dict = {}.fromkeys(LIST_OF_KEYS, 0)
    for key in LIST_OF_KEYS:
        total = 0
        for key2 in LIST_OF_KEYS:
            num = d[key][key2].get(key2)
            total += num
        outgoings_dict[key] = total
    return outgoings_dict

outgoing_dict = key_number_of_outgoing()

def get_new_r(r):
    new_r = {}.fromkeys(LIST_OF_KEYS, 0)
    for key in LIST_OF_KEYS:
        for key2 in LIST_OF_KEYS:
            new_r[key2] = r[key] * (d[key][key2] / outgoing_dict[key])
    return new_r

def run_iterations():
    r = {}.fromkeys(LIST_OF_KEYS, 1)
    for num in range(iterations):
        temp_r = copy.deepcopy(temp_r)
        for key in LIST_OF_KEYS:
            new_r = get_new_r(r)
            r[key] = new_r[key]
    return r

with open(out_file, 'wb') as f:
    pickle.dump(run_iterations(), f)