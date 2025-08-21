import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

from utils import load_dataset, has_no_repeating_characters

from itertools import product

if __name__ == "__main__":
    first_names, last_names = load_dataset()

    names = (f"{first} {last}" for first, last in product(first_names, last_names))
    non_repeating_names = (name for name in names if has_no_repeating_characters(name))

    with open("result.txt", "w") as f:
        for name in non_repeating_names:
            f.write(name + "\n")
