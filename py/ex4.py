import numpy as np
import time

def normalize_og(arr):    
    t = time.perf_counter()
    result = np.zeros(len(arr))
    for i in range(len(arr)):
        result[i] = (arr[i] - np.mean(arr)) / np.std(arr)
    e = time.perf_counter()
    print(f"Code og took {e-t:.6f} seconds to complete.")
    return result

def pre_normalize(arr):
    t = time.perf_counter()
    m = np.mean(arr)
    s = np.std(arr)
    result = np.zeros(len(arr))
    for i in range(len(arr)):
        result[i] = (arr[i] - m) / s
    e = time.perf_counter()
    print(f"Precalculated code fix took {e-t:.6f} seconds to complete.")
    return result

def normalize_vectorized(arr):
    t = time.perf_counter()
    #arr = np.asarray(arr) #-> convert standard arry into a numpy array => handled in the input
    m = arr.mean()       # remeber to pre calculate even is vectorised -> cut the time in half
    s = arr.std()
    result = (arr - m) / s
    e = time.perf_counter()
    print(f"Vectorized took {e-t:.6f} seconds")
    return result

'''
Notes: 
1. precalculate values used in cpu bound opperation 
2. vectorise large loops -> use Numpy array and opperate over the whole data set in one batch

My code fix took 0.155247 seconds to complete.    (1)
Vectorized took 0.010227 seconds                  (2)
'''


arr = np.random.rand(1_000_000_0)
if __name__ == "__main__":
    # normalize_og(arr) - explodes in time over 10k itterations (10k: 0.02, 100k: 20s)
    pre_normalize(arr)
    normalize_vectorized(arr)

'''
Q4. NumPy vs loop — spot the antipattern

Task: this is O(n²) in wall time due to .mean()/.std() being recomputed every iteration, 
plus it's not vectorized. Fix it, then profile before/after with %timeit or time.perf_counter.

Steps: 
1. add the counter with 'import time', 'time.perf_counter()' and calculate the difference
2. precalculate the means and standard diviations

=> program now runs in 2n=n instead of n^2

3. use numpy arry array -> vectorised operation
'''