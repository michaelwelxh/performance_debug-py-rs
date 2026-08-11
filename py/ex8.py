"""
TASK:
  Two implementations of the same function below: build a big string from
  a list of pieces.

  1. Predict the asymptotic difference (Big-O) between concat_loop and
     concat_join before running anything. ---->  after some light searching join is a cPython method so should he highly optimised and potentially faster then the manual python 
     implementation but to answer the question both are likley O(N) and join is likely faster excluding the function call time -  theres also the consideration of my byte code being executed in the first version - but im unsure on this 
  2. Verify with cProfile or timeit yourself.
  3. Explain WHY the difference exists at the level of what CPython is doing
     with string immutability and memory allocation. not just "join is faster".
"""

import time


def concat_loop(pieces):
    result = ""
    for p in pieces:
        result += p
    
    return result


def concat_join(pieces):
    return "".join(pieces)


def generate_pieces(n):
    return [f"piece_{i}_" for i in range(n)]


if __name__ == "__main__":
    pieces = generate_pieces(100_000)

    start = time.perf_counter()
    concat_join(pieces)
    end = time.perf_counter()
    print(f"join time: {end-start:.8f} seconds")

    start_ = time.perf_counter()
    result = concat_loop(pieces)
    end_ = time.perf_counter()
    print(f"manual time: {end_-start_:.8f} seconds")




'''
time wrapper: 

    join time: 0.00125940 seconds
    manual time: 0.02063600 seconds

        -> correct in the original assumption but need to do some research on CPython 

'''
        
r'''

cprofile COMMANDS

        python -m cProfile -o profile.prof ex8.py
        python -m pstats profile.prof
        sort cumulative
        stats 20

        Tue Aug 11 14:40:57 2026    profile.prof

         14 function calls in 0.034 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.034    0.034 {built-in method builtins.exec}
        1    0.000    0.000    0.034    0.034 ex8.py:1(<module>)
        1    0.022    0.022    0.022    0.022 ex8.py:17(concat_loop)
        1    0.000    0.000    0.011    0.011 ex8.py:29(generate_pieces)
        1    0.011    0.011    0.011    0.011 ex8.py:30(<listcomp>)
        1    0.000    0.000    0.001    0.001 ex8.py:25(concat_join)
        1    0.001    0.001    0.001    0.001 {method 'join' of 'str' objects}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        4    0.000    0.000    0.000    0.000 {built-in method time.perf_counter}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}



        ### next with profile seperatly and do some research on CPython 
        


'''