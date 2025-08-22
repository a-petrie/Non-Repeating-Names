import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

from utils import load_dataset, has_no_repeating_characters

from itertools import product

def filter_non_ascii_names(names):
    return (name for name in names if has_no_repeating_characters(name))

def non_repeating(first_names, last_names):
    first_names = filter_non_ascii_names(first_names)
    last_names = filter_non_ascii_names(last_names)

    names = (f"{first} {last}" for first, last in product(first_names, last_names))
    return (name for name in names if has_no_repeating_characters(name))

if __name__ == "__main__":
    first_names, last_names = load_dataset()

    with open("result.txt", "w") as f:
        for name in non_repeating(first_names, last_names):
            f.write(name + "\n")
