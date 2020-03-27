#!/usr/bin/env python3

# nintendi.py:
# Description: Generated a mutated version of "Nintendo".
# Usage: Run it.
# Requires: Python (tested on 3.8)
# dev notes: lmfao

import random

vowels = "aeiouy"
def randvowel(): return random.choice(vowels)

print("n{}nt{}nd{}".format(randvowel(), randvowel(), randvowel()))
