import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def extract_results(result):
    input_size = result["param"]

    stats = result["stats"]
    stats["algorithm"] = result["group"]
    stats["input_size"] = input_size
    return stats

def make_plot(results: pd.DataFrame, filename: str) -> None:
    sns.lineplot(x="input_size", y="mean", hue="algorithm", data=results)
    plt.ylabel("Execution time (ms)")
    plt.xlabel("Input Size")
    plt.title("Comparison of Algorithm Execution Times")
    #plt.savefig(filename)
    plt.show()

if __name__ == "__main__":

    with open("run5.json") as f:
        results = json.loads(f.read())

    stats = [extract_results(result) for result in results["benchmarks"]]

    results = pd.DataFrame(stats)

    both = results[results["algorithm"].str.contains("both")]
    last_name = results[results["algorithm"].str.contains("last name")]
    not_naive = results[~results["algorithm"].str.contains("naive")]

    make_plot(both, "varying both inputs")
    make_plot(last_name, "only varying last name")
    make_plot(not_naive, "without naive algorithm")

    both = not_naive[results["algorithm"].str.contains("both")]
    make_plot(both, "without naive algorithm")
