# from
# https://brainwagon.org/2024/12/19/another-chapter-in-the-im-dimwitted-theme-from-advent-of-code-2024/
import re

# data was in the format of a big chunk of small patterns,
# followed by list of towels we need to construct.
input_path = "input/dec19.txt"

data = open(input_path).read()

# find the patterns, and build a regular expression

patterns, towels = data.split("\n\n")
patterns = patterns.split(", ")

# "any number of any of the patterns, consuming the entire string."
regex = "^(" + "|".join(patterns) + ")+$"

print(regex)

h = re.compile(regex)

c = 0
for design in towels.rstrip().split("\n"):
    if h.match(design):
        c += 1

print(c, "designs are possible")
