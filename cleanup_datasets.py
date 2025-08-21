import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'common')))

from utils import load_dataset

FIRST_NAMES = "first_names.all.txt"
LAST_NAMES = "last_names.all.txt"
DISALLOWED_FIXES = ["-", ",", "/"]

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def cleanup(names):
    names = [name for name in names if is_ascii(name)]
    return names

def read_name_dataset(dataset_file: str) -> [str]:
    with open(dataset_file) as f:
        return [name.strip() for name in f.readlines()]

if __name__ == "__main__":

    first_names = read_name_dataset(FIRST_NAMES)
    first_names = cleanup(first_names) 
    
    with open(FIRST_NAMES, "w") as f:
        f.write("\n".join(first_names))

    last_names = read_name_dataset(LAST_NAMES)
    last_names = cleanup(last_names)
    with open(LAST_NAMES, "w") as f:
        f.write("\n".join(last_names))
