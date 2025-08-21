# Name Analysis

## Background

When I was at university, I had a friend - and that friend had a very peculiar property. His name contained no repeating characters. I won't include his full name here to maintain his privacy, but his name was a stonking 12 letters long. That's quite a lot not to have any repeating characters.

Now, I have another friend. This friend is a mathematician. I was telling him this story, and we got to pondering other possible names that didn't have any repeating characters. What is the longest name without a repeating character? How many people have names without repeating characters? The following investigation is dedicated to these two friends.

## The Names

In order to investigate names without repeating characters, first we'll need a list of names. An initial guess was whether or not we could use the UK electoral register, though after a quick look this does not seem to be readily available online - online via public libraries. Historical records are also available, though cost a princely sum of £92. The search for names continued. I came across a few other name datasets, but these seemed to only contain first names.

Eventually, I did stumble across [this dataset](https://github.com/Debdut/names.io) which contains lists of first and last names. It contains 164,432 first names and 98,394 last names. These will be the datasets used to carry out the investigation. Note that the datasets are included directly in this repo.

Taking a look at the dataset, many of the names contain non-ascii characters. For an initial investigation we won't consider non-ascii names. This takes us down to 160,553 first names and 98,344 last names. Note that there was also some strange HTML at the end of the last names file, but this was after we got into non-ascii names so this shouldn't concern us.

## The Algorithm

### Naive Baseline

First off, let's just take the naive approach: we consider all pairs of names and check each one to see if it has repeating characters.

```
def has_no_repeating_characters(string: str) -> bool:
    return len(name) == len(set(name))

names = (f"{first} {last}" for first, last in product(first_names, last_names))
non_repeating_names = (name for name in names if has_no_repeating_characters(name))

with open("result.txt", "w") as f:
    for name in non_repeating_names:
        f.write(name + "\n")
```

Before diving in to the initial results, I'd like to make a few notes on the implementation. Firstly, we're using python's generator expressions to capture the actual computation. This is massively preferable to a list comprehension as the results are always lazily evaluated, meaning that our program is actually `O(1)` in terms of memory usage as opposed to `O(M*N)` were to try and store everything in a list. Additionally, we're writing straight to the output file - previously I had a print statement to print out names without non-repeating characters, however as a general principle we can assume that disk IO will be faster that printing to stdout. Of course, for true performance benchmarks we should ultimately try and remove this IO overhead entirely from any performance measurements to capture the algorithm in isolation.

So how bad is it? This naive solution is clearly suboptimal, it has time complexity `O(M*N)` where `M` and `N` are the number of first and last names respectivelt. For our dataset this is 15,789,424,232 name combinations that we need to check.

I left this running, and it took a grand total of 1hr 49m 20s to run on my machine and reported a total of 149,490,149 names with no repeating characters. In fact, the resulting `result.txt` was 1.7GB in size.

### A Small Improvement

Now, we can make some observations about our problem to improve our algorithm. We care about names that don't have repeated characters. It's a fairly trivial observation that if either a first or a last name contains a repeated character, then any combination of names involving that first or last name will also contain a repeated character.

Therefore, we can reduce the number of pairs we need to check if we pre-filter our first and last names that contain repeated characters:

```
# pre-filter out names with repeating characters
first_names = [name for name in first_names if has_no_repeating_characters(name)]
last_names = [name for name in last_names if has_no_repeating_characters(name)]

names = (f"{first} {last}" for first, last in product(first_names, last_names))
non_repeating_names = (name for name in names if has_no_repeating_characters(name))

with open("result.txt", "w") as f:
    for name in non_repeating_names:
        f.write(name + "\n")
```

This takes us down to only 54,834 first names and 3,6041 last names. So now our time complexity is `O(M'*N')` where `M' < M` and `N' < N`. For our names dataset, this cuts us down to 1,976,272,194 name combinations to check. So we've shaved off two orders of magnitude!

Indeed, on my machine this took a comparatively minuscule 14m 42s to run to completion. Of course, this isn't a rigourous performance benchmark, but it does at least serve as a finger-in-the-wind point of comparison.

### The Quest For Linear Time

We've managed to cut down our runtime by a factor of <<SOME FACTOR>>, but can we do better? Both the algoritms thus far have had quadratic time complexity. Would it be possible to construct an algorithm in linear time? After all, we're checking lots of name combinations that possibly don't need to be checked. I've done enough hackerrank problems to know that some sort of lookup table should be able to come to the rescue here.

The thrust of this algorithm lies in whether or not we can compute some data structure that, given a first name, can return all of the second names that do not contain any of the characters from the first name. 

For clarity, let's quickly look at a worked example the intended behaviour of such a lookup:

```
# add some names to the lookup
>> lookup.add("jim")
>> lookup.add("pat")
>> lookup.add("dan")

# now we can ask for the names that don't have characters from "steve" in it
>> lookup.get("steve")
["jim", "dan"] # "pat" and "steve" both have the letter 't'
```

So, in pseudo-code this algorithm would look something like:

```
# compute lookup table
for last_name in last_names:
    lookup.add(last_name)
    
non_repeating_names = []

# now all non-repeating names
for first_name in first_names:
    valid_last_names = lookup.get(name)
    non_repeating_names = [first_name + " " last_name for last_name in valid_last_names]
```

The above should be linear time (`O(M+N)`) given that:

a) The lookup can be constructed in linear time
b) Querying the lookup can be done in constant time

For now, I'll take these as a given. But I've outline the case for the above two statements being true in Appendix A.

So the actual implementation looks something like:

```
def non_repeating(first_names, last_names):
    for name in first_names:
        valid_last_names = lookup.does_not_contain_characters(name)
        for full_name in (f"{name} {last_name}" for last_name in valid_last_names):
            yield full_name

if __name__ == "__main__":
    first_names, last_names = load_dataset()

    first_names = [n for n in first_names if is_ascii(n)]
    last_names = [n for n in last_names if is_ascii(n)]

    first_names = [n for n in first_names if has_no_repeating_characters(n)]
    last_names = [n for n in last_names if has_no_repeating_characters(n)]

    lookup = Lookup(last_names)

    with open("results.txt", "w") as f:
        for name in non_repeating(first_names, last_names):
            f.write(name + "\n")
```

Now with these improvements, the total runtime has now reduced to a staggeringly low 3minutes and 10seconds on my most recent run!

A fun corollary of this algorithm is that if you don't pre-filter the first and last names, the algorithm will actually return all names who first and last names contain disjoint sets of characters. I realised this after wondering why my supposedly linear time algorithm was taking so long to run, only to realise I'd forgotten to do the pre-filtering!

## Benchmarks

So far, all of our performance measurements have been very rough and ready. Let's have an actual showdown of our algorithms! To do this we'll firstly need to refactor our code to separate it from any IO. Secondly, given that these algorithms take so long to finish execution, we want to be able to run them on smaller sets of input data so that the benchmarks run in a reasonable amount of time.

## Appendix A: Proving Time Complexities of Lookup Table

Perhaps it'll be easiest to get a feel for the time complexities for the lookup table are true by looking at the actual implementation.

```
class Lookup:

    table = dict()

    def __init__(self, names: [str]):
        self.chars = set(''.join(names))
        for char in self.chars:
            self.table[char] = set()

        for name in names:
            chars_not_present = self.chars - set(name)
            for char in chars_not_present:
                self.table[char].add(name)
            
    def does_not_contain_characters(self, name: str):
        name = set(name)
        valid_names = self.table[name.pop()]
        for names_without_char in (self.table[char] for char in name):
            valid_names = set.intersection(valid_names, names_without_char)
        return valid_names
```

### Proof of Linear Time Construction

So for a) we can take a look at `__init__` which takes a list of names. First of all, we construct empty sets for each of the different characters in our input (we can call this our alphabet). This will be come constant. Since we're only considering ASCII names, our alphabet is the standard 26 letters of the english alphabet, but the characters `-` (as in Jean-Pierre) and `'` (as in O'Neil). Let's denote the size of our alphabet with `A`.

So the initialisation of the empty sets in the table is `O(A)`. Now the main body of the population logic has us:

1) Taking a set difference between our alphabet and the characters in each last name to get the characters that _aren't_ in that name.
2) For each of those characters, adding the name to the corresponding set in our lookup

According to [TODO: reference], the best-case time complexity of the set difference is `O(A)`, and worst case is `O(A*A)`. And for the name to the lookup, the number of iterations will have an upper bound of `A-1` (ie `name` is a single character), though the average case will be a lot better. Let's call this value B.

This gives an overall worst-case time complexity for constructing the lookup of `O(A+N*A*A*B)`. Both `A` and `B` are constant size the size of our alphabet is bound, the `N` term dominates so have a time complexity of `O(N)`.

### Proof of Constant Time Lookup

For the implementation of the lookup, we calculate the intersection of all of the sets of names that don't contain each successive character of the input name.

So for example, if we were looking up "steve" then this would be `~S ∩ ~T ∩ ~E ∩ ~V` where `~S` denotes the set of names that don't contain the letter "s" etc. The time complexity of `set.intersect(A,B)` is `O(min(|A|,|B|))`. It remains to prove an upper bound for this. Actually, it is proportional to the size of the input.

Hunch: upper bound isn't great makes lookup quadratic but average/best case is much better.


## References

- [Time complexity of Python set difference](https://stackoverflow.com/questions/48044353/what-is-the-run-time-of-the-set-difference-function-in-python)
- [Time complexity of Python set.intersection](https://stackoverflow.com/questions/8102478/intersection-complexity)
