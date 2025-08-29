import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'naive')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prefilter')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'linear_time')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'further_optimisations')))

# @Citation: ChatGPT
import pytest
import gc

from naive import non_repeating as naive_non_repeating
from prefilter import non_repeating as prefilter_non_repeating
from linear_time import non_repeating as linear_time_non_repeating
from optimised import non_repeating as optimised_non_repeating

from utils import load_dataset

BENCHMARKS = [
    #("naive", naive_non_repeating),
    ("prefilter", prefilter_non_repeating),
    ("linear_time", linear_time_non_repeating),
    ("optimised", optimised_non_repeating),
]

DATA_MODES = [
    ("first_only", lambda sample_size: (load_dataset(sample_size=sample_size)[0], load_dataset()[1][-1000:])),
    ("both", lambda sample_size: load_dataset(sample_size=sample_size)),
]

SAMPLE_SIZES = [2000, 4000, 8000, 16000, 32000, 64000]

@pytest.mark.parametrize("algo_name,algo_func", BENCHMARKS)
@pytest.mark.parametrize("data_mode_name,data_loader", DATA_MODES)
@pytest.mark.parametrize("sample_size", SAMPLE_SIZES)
def test_benchmarks(benchmark, algo_name, algo_func, data_mode_name, data_loader, sample_size):
    first_names, last_names = data_loader(sample_size)
    benchmark.group = f"{algo_name} {data_mode_name}"
    benchmark(lambda: list(algo_func(first_names, last_names)))
