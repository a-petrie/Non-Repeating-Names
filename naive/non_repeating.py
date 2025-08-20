from itertools import product

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def read_name_dataset(dataset_file: str) -> [str]:
    with open(dataset_file) as f:
        names = [name.strip() for name in f.readlines()]
    return [name for name in names if is_ascii(name)]

def has_no_repeating_characters(name: str) -> bool:
    return len(name) == len(set(name))

if __name__ == "__main__":

    first_names = read_name_dataset("../first_names.all.txt")
    last_names = read_name_dataset("../last_names.all.txt")

    print(len(first_names) * len(last_names))

    non_repeating_names = []

    for first, last in product(first_names, last_names):
        name = f"{first} {last}"
        if has_no_repeating_characters(name):
            print(f"{name} has no repeating characters")
            non_repeating_names.append(name)        

    with open("result.txt", "w") as f:
        f.writelines(non_repeating_names)
