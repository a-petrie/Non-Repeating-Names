import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

from utils import load_dataset, has_no_repeating_characters

def set_to_string(charset) -> str:
    return str(''.join(sorted(c for c in charset)))

class Lookup:

    def __init__(self, names: [str]):
        self.table = dict()

        chars = set(''.join(names))
        for char in chars:
            self.table[char] = set()

        for name in names:
            chars_not_present = chars - set(name)
            for char in chars_not_present:
                self.table[char].add(name)
        self.all_names = set(names)

    def does_not_contain_characters(self, name: str):
        name = set(name)
        name_str = set_to_string(name)
        if name_str in self.table:
            valid = self.get(name_str)
            return valid
        else:
            prefix, last_char = name_str[:-1], name_str[-1:]
            first = self.does_not_contain_characters(prefix)
            rest = self.get(last_char)
            self.table[prefix] = first
            return set.intersection(first, rest)


    def get(self, char: str):
        if char not in self.table:
            return self.all_names
        return self.table[char]


def non_repeating(first_names, last_names):
    first_names = [n for n in first_names if has_no_repeating_characters(n)]
    last_names = [n for n in last_names if has_no_repeating_characters(n)]

    lookup = Lookup(last_names)

    for name in first_names:
        valid_last_names = lookup.does_not_contain_characters(name)
        for last_name in valid_last_names:
            yield f"{name} {last_name}"


if __name__ == "__main__":
    first_names, last_names = load_dataset()

    with open("result.txt", "w") as f:
        for name in non_repeating(first_names, last_names):
            f.write(name + "\n")
