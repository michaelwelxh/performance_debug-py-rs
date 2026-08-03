import pandas as pd
import time
import numpy as np
import polars as pl


def og(df, total): 

    s = time.perf_counter()            

    total = 0
    for i in range(len(df)):
        total += df.iloc[i]['a'] 

    e = time.perf_counter()
    print(f"Og code fix took {e-s:.6f} seconds to complete.")

def vec(df, total):
    s = time.perf_counter()            

    total += df['a'].sum()

    e = time.perf_counter()
    print(f"Vec(raw pandas) code fix took {e-s:.6f} seconds to complete.")    


def vecval(df, total):
    s = time.perf_counter()            

    total += df['a'].values.sum()     # np c loop since values coanverts from pandas series to numpyarray

    e = time.perf_counter()
    print(f"Vecval(pandas-value -> numpy c loop) code fix took {e-s:.6f} seconds to complete.")    

def vecnp(df, total):
    # pandas method, handles NaN by default (skipna=True)
    # numpy directly, no NaN handling by default -> hence using np actually cuts out the pandas NaN overhead
    s = time.perf_counter()            

    total += np.sum(df['a'].values)     # np c loop 

    e = time.perf_counter()
    print(f"Vecnp(numpy) code fix took {e-s:.6f} seconds to complete.")  

def pol(df, total):

    p = pl.from_pandas(df)

    s = time.perf_counter()            

    total += p['a'].sum()


    e = time.perf_counter()
    print(f"Pol(polars) code fix took {e-s:.6f} seconds to complete.")  

 
total = 0
df = pd.DataFrame({'a': range(1_000_000)})
if __name__ == "__main__":
    #og(df, total)
    vec(df, total)
    vecval(df, total)
    vecnp(df, total)
    pol(df, total)



'''The polars/pandas gotcha
Task: rewrite for at least 100x speedup using vectorized ops.
 Bonus: rewrite in Polars and compare.


Og code fix took 14.722803 seconds to complete.
Vec code fix took 0.001071 seconds to complete.
Vecval code fix took 0.000836 seconds to complete.
Vecnp code fix took 0.000637 seconds to complete.
Vecnp code fix took 0.000531 seconds to complete.


the original code uses integer location at index i in column a 
-> i want to simply use the vectorised df and sum all 





Notes 

1. using np actually cuts out the pandas NaN overhead and uses a C loop instantly -> actually more complex
| Operation        | C loop         | Checks for `NaN`?   | Result with `NaN` |
| ---------------- | -------------- | ------------------- | ----------------- |
| `arr.sum()`      | ✓              | No                  | `NaN`             |
| `np.sum(arr)`    | ✓              | No                  | `NaN`             |
| `np.nansum(arr)` | ✓              | Yes                 | Ignores `NaN`     |
| `df["a"].sum()`  | ✓ (eventually) | Yes (`skipna=True`) | Ignores `NaN`     |


2. dtype matters
If df['a'] were object dtype instead of int64, .sum() would fall back to a slow 
Python-level loop even though it's "vectorized" syntax. Always check df.dtypes 
— vectorized syntax isn't vectorized execution if the underlying array isn't a proper numeric dtype.
-> convert to pd arary

3. warming up the paths (did have misconfigured virtual env at the time so would have to check)

Vec(raw pandas) code fix took 0.002680 seconds to complete.
Vecval(pandas-value -> numpy c loop) code fix took 0.000581 seconds to complete.
Vecnp(numpy) code fix took 0.000726 seconds to complete.
Pol(polars) code fix took 0.001931 seconds to complete.

Vec(raw pandas) code fix took 0.000888 seconds to complete.
Vecval(pandas-value -> numpy c loop) code fix took 0.000542 seconds to complete.
Vecnp(numpy) code fix took 0.000515 seconds to complete.
Pol(polars) code fix took 0.000404 seconds to complete.

- pandas and polars require waarm up.
'''