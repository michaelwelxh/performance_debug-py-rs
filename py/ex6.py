"""
TASK:
  This script processes a list of "log records" and builds a summary report.
  It's slow.

  1. Profile it with cProfile yourself (command line or programmatic).
  2. Identify the ACTUAL bottleneck. It's probably not what you'd guess just
     from reading top to bottom.
  3. Fix it. Confirm at least a 10x speedup.
  4. Output must stay the same shape (same return values).
"""

import random
import time 
import pandas as pd



def generate_records(n=20000):
    s = time.perf_counter() 
    random.seed(42)
    records = []
    for i in range(n):
        records.append({
            "id": i,
            "user": f"user_{random.randint(0, 500)}",
            "message": " ".join(random.choice(
                ["error", "warning", "info", "timeout", "retry", "success"]
            ) for _ in range(20)),
            "level": random.choice(["ERROR", "WARN", "INFO"]),
        })
    e = time.perf_counter()
    print(f"generation took {e-s:.6f} seconds to complete.")  

    return records


def pandas_build_report(records):
    """Builds a summary: per-user message log as a single string, plus level counts."""
    s = time.perf_counter() 
    report = ""
    level_counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    user_logs = {}

    # next ill vectirise the computation in both these loops should get the time down considerable all the fixes in implemened loop for all user logs and was still 'vectorised pandas build took 0.456082 seconds to complete'
    for r in records:
        report += f"[{r['level']}] {r['user']}: {r['message']}\n"
        level_counts[r["level"]] += 1

        if r["user"] not in user_logs:
            user_logs[r["user"]] = ""
        user_logs[r["user"]] += r["message"] + " "

    user_word_counts = {}
    for user, text in user_logs.items():
        words = text.split()
        wordser = pd.Series(words)
        counts = wordser.value_counts().to_dict()
        user_word_counts[user] = counts
    e = time.perf_counter() 
    print(f"vectorised pandas build took {e-s:.6f} seconds to complete.")  

    return report, level_counts, user_word_counts

def og_build_report(records):
    """Builds a summary: per-user message log as a single string, plus level counts."""
    s = time.perf_counter() 
    report = ""
    level_counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    user_logs = {}

    for r in records:
        report += f"[{r['level']}] {r['user']}: {r['message']}\n"
        level_counts[r["level"]] += 1

        if r["user"] not in user_logs:
            user_logs[r["user"]] = ""
        user_logs[r["user"]] += r["message"] + " "

    user_word_counts = {}
    for user, text in user_logs.items():
        words = text.split()
        counts = {}
        for w in words:
            counts[w] = words.count(w)        # <- HERE IS THE CULPRITE 
        user_word_counts[user] = counts
    e = time.perf_counter() 
    print(f"original build took {e-s:.6f} seconds to complete.")  

    return report, level_counts, user_word_counts

if __name__ == "__main__":
    records = generate_records(n=20000)
    
    report, level_counts, user_word_counts = pandas_build_report(records)
    # report, level_counts, user_word_counts = og_build_report(records)


# solution 
    # 1.vectorise the count computation (first try pandas then try polars)




''''

HOW TO USE CPROFIELE


Command line (easiest)

        python -m cProfile ex6.py

    Or save the results:

        python -m cProfile -o profile.prof ex6.py

    Then inspect them:

        python -m pstats profile.prof

Programmatically

    Wrap the code you want to measure.

        import cProfile

        def main():
            # your code
            ...

        cProfile.run("main()")

    Or:

        import cProfile

        profiler = cProfile.Profile()

        profiler.enable()

        # Code to profile
        main()

        profiler.disable()
        profiler.print_stats(sort="cumtime")

        
    MORE CPROFILE USEFUL COMMANDS 


    Useful commands inside pstats:

        sort cumulative
        stats 20

    cumulative → total time including child function calls.
    stats 20 → top 20 slowest functions.




    Sorts by time spent only in that function (tottime).
        % sort time
        % stats 20
    

    Shows who called a function.
        % callers function_name
   

    Shows which functions it called.
        % callees function_name
   

    Lists all available commands.
        % help
   

    Exits.
        % quit
'''

#used a raw string here to fix ---- as the doc string contains windows paths
r'''
results 

-> FIRST RUN 


        python -m cProfile ex6.py
        python -m cProfile -o profile.prof ex6.py
        python -m pstats profile.prof
            % sort cumulative
            % stats 20

        OUTPUT
            Thu Aug  6 07:12:44 2026    profile.prof

                    3262053 function calls (3262026 primitive calls) in 4.534 seconds

            Ordered by: cumulative time
            List reduced from 127 to 20 due to restriction <20>

            ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                3/1    0.000    0.000    4.534    4.534 {built-in method builtins.exec}
                    1    0.001    0.001    4.534    4.534 ex6.py:1(<module>)
                    1    0.373    0.373    3.897    3.897 ex6.py:37(build_report)
            400000    3.507    0.000    3.507    0.000 {method 'count' of 'list' objects}
                    1    0.034    0.034    0.633    0.633 ex6.py:18(generate_records)
                20044    0.062    0.000    0.538    0.000 {method 'join' of 'str' objects}
            420000    0.108    0.000    0.476    0.000 ex6.py:26(<genexpr>)
            420000    0.135    0.000    0.387    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:375(choice)
            440000    0.181    0.000    0.241    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:239(_randbelow_with_getrandbits)
                20000    0.007    0.000    0.040    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:366(randint)
            580289    0.035    0.000    0.035    0.000 {method 'getrandbits' of '_random.Random' objects}
                20000    0.018    0.000    0.033    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:292(randrange)
            440000    0.025    0.000    0.025    0.000 {method 'bit_length' of 'int' objects}
            420090    0.022    0.000    0.022    0.000 {built-in method builtins.len}
                501    0.016    0.000    0.016    0.000 {method 'split' of 'str' objects}
                60000    0.004    0.000    0.004    0.000 {built-in method _operator.index}
                6/1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap>:1022(_find_and_load)
                6/1    0.000    0.000    0.004    0.004 <frozen importlib._bootstrap>:987(_find_and_load_unlocked)
                6/1    0.000    0.000    0.003    0.003 <frozen importlib._bootstrap>:664(_load_unlocked)
                2/1    0.000    0.000    0.003    0.003 <frozen importlib._bootstrap_external>:877(exec_module)
                
                WE CAN SEE '400000    3.507    0.000    3.507    0.000 {method 'count' of 'list' objects}' IS THE BULK OF THE TIME.
'''