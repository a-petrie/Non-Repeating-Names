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

non_repeating_names = []

for first, last in product(first_names, last_names):
    name = f"{first} {last}"
    if has_no_repeating_characters(name):
        print(f"{name} has no repeating characters")
        non_repeating_names.append(name)        
```

This naive solution is clearly suboptimal, it has time complexity `O(M*N)` where `M` and `N` are the number of first and last names respectivelt. For our dataset this is 15,789,424,232 name combinations that we need to check.

I left this running, and it took a grand total of <<some time>> to run on my machine.

### A Small Improvement

Now, we can make some observations about our problem to improve our algorithm. We care about names that don't have repeated characters. It's a fairly trivial observation that if either a first or a last name contains a repeated character, then any combination of names involving that first or last name will also contain a repeated character.

Therefore, we can reduce the number of pairs we need to check if we pre-filter our first and last names that contain repeated characters:

```
first_names = [name for name in first_names if has_no_repeating_characters(name)]
last_names = [name for name in last_names if has_no_repeating_characters(name)]

non_repeating_names = []

for first, last in product(first_names, last_names):
    name = f"{first} {last}"
    if has_no_repeating_characters(name):
        print(f"{name} has no repeating characters")
        non_repeating_names.append(name)        
```

This takes us down to only 54,834 first names and 3,6041 last names. So now our time complexity is `O(M'*N')` where `M' < M` and `N < N'`. For our names dataset, this cuts us down to 1,976,272,194 name combinations to check. So we've shaved off two orders of magnitude!

Indeed, on my machine this took <<SOME TIME>> to run to completion. Of course, this isn't a rigourous performance benchmark, but it does at least serve as a finger-in-the-wind point of comparison.

### The Quest For Linear Time

We've managed to cut down our runtime by a factor of <<SOME FACTOR>>, but can we do better? Both the algoritms thus far have had quadratic time complexity. Would it be possible to construct an algorithm in linear time? After all, we're checking lots of name combinations that possibly don't need to be checked. I've done enough hackerrank problems to know that some sort of lookup table should be able to come to the rescue here.
