## Q12 CPython bytecode: predict before you run

"""
TASK:
  For each function below, before running anything:
    1. Predict whether it's faster or slower than its sibling, and by roughly
       how much (same order of magnitude, 2x, 10x, etc).

    2. Use `dis.dis()` to look at the actual bytecode for each and explain
       the difference in terms of what instructions are being executed.

    3. Then time them for real and see if your prediction held.
"""

import time 

def sum_with_plus(n):
    total = 0
    for i in range(n):
        total = total + i
    return total


def sum_with_iadd(n):
    total = 0
    for i in range(n):
        total += i
    return total


def sum_builtin(n):
    return sum(range(n))


def lookup_attr_in_loop(obj, n):
    total = 0
    for _ in range(n):
        total += obj.value
    return total


def lookup_attr_cached(obj, n):
    val = obj.value
    total = 0
    for _ in range(n):
        total += val
    return total

if __name__ == "__main__":
    sum_with_plus(n)
    sum_with_iadd(n)
    sum_builtin(n)
    lookup_attr_in_loop(obj, n)
    lookup_attr_cached(obj, n)