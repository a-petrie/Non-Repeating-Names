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
    for i, name in enumerate(names):
        if "/" in name:
            split = names.split("/")
            names[i] = split[0]
            names.append(split[1])
        for fix in DISALLOWED_FIXES:
            names[i] = name.removeprefix(fix).removesuffix(fix)
    return sorted(list(set(names)))

def read_name_dataset(dataset_file: str) -> [str]:
    with open(dataset_file) as f:
        return [name.strip() for name in f.readlines()]

def clean_dataset(dataset: str) -> None:
    names = read_name_dataset(dataset)
    names = cleanup(names) 
    with open(dataset, "w") as f:
        f.write("\n".join(names))

if __name__ == "__main__":
    clean_dataset(FIRST_NAMES)
    clean_dataset(LAST_NAMES)
