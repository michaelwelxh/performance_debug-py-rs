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

#every add is a function call so likely not fast  -> x.__add__(sep).__add__(y).__add__(sep).__add__(z) -> 

import time 

#3 -> slower then sum_with_iadd as it need to load total twice 
def sum_with_plus(n):
    total = 0
    for i in range(n):
        total = total + i
    return total

# 2
def sum_with_iadd(n):    
    total = 0
    for i in range(n):
        total += i
    return total

# 1 function calls here vs N+1 in the above two and no aditional space needed
def sum_builtin(n):
    return sum(range(n))


#4 .value called n times, add called n times and range called onese so slowest so far  
def lookup_attr_in_loop(obj, n):
    total = 0
    for _ in range(n):
        total += obj.value
    return total

# obj.value is additional cost , add called n times  with 1 range call so slower then 2 and 3 unless im missing something
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