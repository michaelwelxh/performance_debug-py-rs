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

import dis
import time
#3 or 2 ->  load total aready there not sure which is faster  
def sum_with_plus(n):
    total = 0
    for i in range(n):
        total = total + i
    return total

# 2 or 3 - total is preloaded her once once 
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

class Obj:
    def __init__(self, value):
        self.value = value

if __name__ == "__main__":
    n = 10_000_000
    obj = Obj(0)

    print("sum_with_plus\n")
    start_ = time.perf_counter()
    dis.dis(sum_with_plus)
    end_ = time.perf_counter()
    print(f"time: {end_-start_:.8f} seconds")


    print("sum_with_iadd\n")
    start_ = time.perf_counter()
    dis.dis(sum_with_iadd)
    end_ = time.perf_counter()
    print(f"time: {end_-start_:.8f} seconds")

    print("sum_builtin\n")
    start_ = time.perf_counter()
    dis.dis(sum_builtin)
    end_ = time.perf_counter()
    print(f"time: {end_-start_:.8f} seconds")

    print("lookup_attr_in_loop\n")
    start_ = time.perf_counter()
    dis.dis(lookup_attr_in_loop)
    end_ = time.perf_counter()
    print(f"time: {end_-start_:.8f} seconds")


    print("lookup_attr_cached\n")
    start_ = time.perf_counter()
    dis.dis(lookup_attr_cached)
    end_ = time.perf_counter()
    print(f"time: {end_-start_:.8f} seconds")


## DIS DIS RESULT 

'''
sum_with_plus


line      offset inst                  arg 
 21           0 LOAD_CONST               1 (0)
              2 STORE_FAST               1 (total)

 22           4 LOAD_GLOBAL              0 (range)
              6 LOAD_FAST                0 (n)
              8 CALL_FUNCTION            1
             10 GET_ITER
        >>   12 FOR_ITER                 6 (to 26)
             14 STORE_FAST               2 (i)

 23          16 LOAD_FAST                1 (total)
             18 LOAD_FAST                2 (i)
             20 BINARY_ADD
             22 STORE_FAST               1 (total)
             24 JUMP_ABSOLUTE            6 (to 12)

 24     >>   26 LOAD_FAST                1 (total)
             28 RETURN_VALUE
sum_with_iadd

 28           0 LOAD_CONST               1 (0)
              2 STORE_FAST               1 (total)

 29           4 LOAD_GLOBAL              0 (range)
              6 LOAD_FAST                0 (n)
              8 CALL_FUNCTION            1
             10 GET_ITER
        >>   12 FOR_ITER                 6 (to 26)
             14 STORE_FAST               2 (i)

 30          16 LOAD_FAST                1 (total)
             18 LOAD_FAST                2 (i)
             20 INPLACE_ADD
             22 STORE_FAST               1 (total)
             24 JUMP_ABSOLUTE            6 (to 12)

 31     >>   26 LOAD_FAST                1 (total)
             28 RETURN_VALUE
sum_builtin                                     ---> clearly seems the fasested

 35           0 LOAD_GLOBAL              0 (sum)
              2 LOAD_GLOBAL              1 (range)
              4 LOAD_FAST                0 (n)
              6 CALL_FUNCTION            1
              8 CALL_FUNCTION            1
             10 RETURN_VALUE
lookup_attr_in_loop

 40           0 LOAD_CONST               1 (0)
              2 STORE_FAST               2 (total)

 41           4 LOAD_GLOBAL              0 (range)
              6 LOAD_FAST                1 (n)
              8 CALL_FUNCTION            1
             10 GET_ITER
        >>   12 FOR_ITER                 7 (to 28)
             14 STORE_FAST               3 (_)

 42          16 LOAD_FAST                2 (total)
             18 LOAD_FAST                0 (obj)
             20 LOAD_ATTR                1 (value)
             22 INPLACE_ADD
             24 STORE_FAST               2 (total)
             26 JUMP_ABSOLUTE            6 (to 12)

 43     >>   28 LOAD_FAST                2 (total)
             30 RETURN_VALUE
lookup_attr_cached

 47           0 LOAD_FAST                0 (obj)
              2 LOAD_ATTR                0 (value)
              4 STORE_FAST               2 (val)

 48           6 LOAD_CONST               1 (0)
              8 STORE_FAST               3 (total)

 49          10 LOAD_GLOBAL              1 (range)
             12 LOAD_FAST                1 (n)
             14 CALL_FUNCTION            1
             16 GET_ITER
        >>   18 FOR_ITER                 6 (to 32)
             20 STORE_FAST               4 (_)

 50          22 LOAD_FAST                3 (total)
             24 LOAD_FAST                2 (val)
             26 INPLACE_ADD
             28 STORE_FAST               3 (total)
             30 JUMP_ABSOLUTE            9 (to 18)

 51     >>   32 LOAD_FAST                3 (total)
             34 RETURN_VALUE
'''