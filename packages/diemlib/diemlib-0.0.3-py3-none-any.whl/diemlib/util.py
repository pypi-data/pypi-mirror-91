#!/usr/bin/env python
# -*- coding: utf-8 -*-

# diemlib/main.py

"""
   These are some utilities
"""

import random
import string

# some other utilities


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for i in range(length))
    print("Random string is:", result_str)