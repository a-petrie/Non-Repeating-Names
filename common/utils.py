def read_name_dataset(dataset_file: str) -> [str]:
    with open(dataset_file) as f:
        names = [name.strip() for name in f.readlines()]
    return [name for name in names if is_ascii(name)]

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def has_no_repeating_characters(name: str) -> bool:
    return len(name) == len(set(name))
