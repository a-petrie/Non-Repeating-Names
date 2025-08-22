import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

from utils import load_dataset, is_ascii, has_no_repeating_characters


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
        valid_names = self.get(name.pop())
        for names_without_char in self.__get_all_for_name(name):
            valid_names = set.intersection(valid_names, names_without_char)
        return valid_names

    def __get_all_for_name(self, name: set):
        return (self.get(char) for char in name)

    def get(self, char: str):
        try:
            return self.table[char]
        except KeyError:
            return self.all_names


def non_repeating(first_names, last_names):
    first_names = [n for n in first_names if has_no_repeating_characters(n)]
    last_names = [n for n in last_names if has_no_repeating_characters(n)]

    lookup = Lookup(last_names)

    for name in first_names:
        valid_last_names = lookup.does_not_contain_characters(name)
        for full_name in (f"{name} {last_name}" for last_name in valid_last_names):
            yield full_name

if __name__ == "__main__":
    first_names, last_names = load_dataset()

    with open("result.txt", "w") as f:
        for name in non_repeating(first_names, last_names):
            f.write(name + "\n")
