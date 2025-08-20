import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

from utils import read_name_dataset, is_ascii, has_no_repeating_characters

from itertools import product

if __name__ == "__main__":

    first_names = read_name_dataset("../first_names.all.txt")
    last_names = read_name_dataset("../last_names.all.txt")

    first_names = [name for name in first_names if has_no_repeating_characters(name)]
    last_names = [name for name in last_names if has_no_repeating_characters(name)]

    non_repeating_names = []
    
    for first, last in product(first_names, last_names):
        name = f"{first} {last}"
        if has_no_repeating_characters(name):
            print(f"{name} has no repeating characters")
            non_repeating_names.append(name)        

    with open("result.txt", "w") as f:
        f.writelines(non_repeating_names)
