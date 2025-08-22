from random import sample

FIRST_NAMES = "first_names.all.txt"
LAST_NAMES = "last_names.all.txt"

def read_name_dataset(dataset_file: str) -> [str]:
    with open(dataset_file) as f:
        return [name.strip() for name in f.readlines()]

def load_dataset(sample_size=None) -> ([str], [str]):
    first_names = read_name_dataset(f"../{FIRST_NAMES}")
    last_names =read_name_dataset(f"../{LAST_NAMES}")

    if sample_size is None:
        return first_names, last_names
    return (
        sample(first_names, sample_size),
        sample(last_names, sample_size)
    )

def has_no_repeating_characters(name: str) -> bool:
    return len(name) == len(set(name))
