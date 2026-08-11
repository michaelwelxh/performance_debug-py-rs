"""
TASK:
  This script does some "data processing" that calls into a couple of helper
  functions, one of which quietly does something expensive.

  1. Run this script in the background and attach py-spy to it:
       py-spy record -o profile.svg --pid <PID>
     or
       py-spy dump --pid <PID>
     (You'll need to add a sleep/loop so it runs long enough to attach to,
     or run it as a long-lived process. that's part of the exercise: figure
     out how to make it profileable.)
  2. Determine whether time is going into your code or into a library call
     underneath, and where exactly.
  3. Fix the actual cause of the slowness.
"""

import re
import os
import polars as pl


def clean_text(text):
    # looks fine at a glance
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text


def is_valid_word(word, dictionary):                               # 1
    # dictionary is a list, not a set -> on purpose                                                                     ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    return word in dictionary                                      # (all centered on this ) ran cprofile to confirm ->  100000  19.932    0.000   19.932    0.000 ex7.py:31(is_valid_word)


def process_documents(documents, dictionary):                     # 3 
    results = []
    for doc in documents:
        cleaned = clean_text(doc)
        words = cleaned.split()
        # convert dict to a set 
        dictionary = set(dictionary)
        # vectorise the computation and integreate is_valid_word (valid_words = [w for w in words if is_valid_word(w, dictionary)])
        valid_words = (pl.DataFrame({"word": words}).filter(pl.col("word").is_in(dictionary)).get_column("word").to_list())     
        results.append(valid_words)
    return results


def build_dictionary(size):
    return [f"word{i}" for i in range(size)]


def generate_documents(n, words_per_doc):
    import random
    random.seed(1)
    docs = []
    for _ in range(n):
        words = [f"word{random.randint(0, 60000)}" for _ in range(words_per_doc)]
        docs.append(" ".join(words))
    return docs

if __name__ == "__main__":
    print("Waiting 15 seconds for py-spy to attach...")
    print(f"My PID is: {os.getpid()}") 
    # time.sleep(10) # commment out when using cProfile
    print("resuming")
    dictionary = build_dictionary(size=50000)
    docs = generate_documents(n=500, words_per_doc=200)
    results = process_documents(docs, dictionary)             # 2




r'''

COMMANDS
        py-spy record -o profile.svg --pid <ID>

        python -m cProfile -o profile.prof ex7.py
        python -m pstats profile.prof
        sort cumulative
        stats 20

        

BEFOR

         916749 function calls (916721 primitive calls) in 35.188 seconds

   Ordered by: cumulative time
   List reduced from 172 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      3/1    0.000    0.000   35.188   35.188 {built-in method builtins.exec}
        1    0.000    0.000   35.188   35.188 ex7.py:1(<module>)
        1    0.005    0.005   19.999   19.999 ex7.py:36(process_documents)
      500    0.040    0.000   19.971    0.040 ex7.py:41(<listcomp>)
   100000   19.932    0.000   19.932    0.000 ex7.py:31(is_valid_word)
        1   14.996   14.996   14.996   14.996 {built-in method time.sleep}
        1    0.001    0.001    0.187    0.187 ex7.py:50(generate_documents)
      500    0.031    0.000    0.182    0.000 ex7.py:55(<listcomp>)
   100000    0.023    0.000    0.152    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:366(randint)
   100000    0.067    0.000    0.128    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:292(randrange)
   100000    0.035    0.000    0.047    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\random.py:239(_randbelow_with_getrandbits)
      500    0.002    0.000    0.014    0.000 ex7.py:24(clean_text)
   300000    0.014    0.000    0.014    0.000 {built-in method _operator.index}
      500    0.001    0.000    0.011    0.000 C:\Users\micha_1chy2aa\AppData\Local\Programs\Python\Python310\lib\re.py:202(sub)
      500    0.008    0.000    0.008    0.000 {method 'split' of 'str' objects}
   109331    0.007    0.000    0.007    0.000 {method 'getrandbits' of '_random.Random' objects}
      500    0.007    0.000    0.007    0.000 {method 'sub' of 're.Pattern' objects}
   100000    0.005    0.000    0.005    0.000 {method 'bit_length' of 'int' objects}
        1    0.000    0.000    0.005    0.005 ex7.py:46(build_dictionary)
        1    0.005    0.005    0.005    0.005 ex7.py:47(<listcomp>)





AFTER 

        1159693 function calls (1155128 primitive calls) in 5.079 seconds

   Ordered by: cumulative time
   List reduced from 1433 to 20 due to restriction <20>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    275/1    0.005    0.000    5.079    5.079 {built-in method builtins.exec}
        1    0.001    0.001    5.079    5.079 ex7.py:1(<module>)
        1    0.835    0.835    4.615    4.615 ex7.py:36(process_documents)
      500    0.336    0.001    2.540    0.005 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\expr\expr.py:6419(is_in)
1500/1000    0.007    0.000    2.218    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\series\series.py:266(__init__)
1500/1000    0.020    0.000    2.212    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\_utils\construction\series.py:76(sequence_to_pyseries)
     1000    0.002    0.000    2.201    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\_utils\parse\expr.py:22(parse_into_expression)
      500    0.006    0.000    2.198    0.004 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\functions\lit.py:31(lit)
      500    1.607    0.003    2.173    0.004 {built-in method new_from_any_values}
      500    0.010    0.000    1.117    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\dataframe\frame.py:5391(filter)
      500    0.002    0.000    1.068    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\_utils\deprecation.py:84(wrapper)
      500    0.005    0.000    1.065    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\lazyframe\opt_flags.py:345(wrapper)
      500    0.004    0.000    1.058    0.002 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\lazyframe\frame.py:2411(collect)
      500    1.047    0.002    1.047    0.002 {method 'collect' of 'builtins.PyLazyFrame' objects}
     1000    0.001    0.000    0.553    0.001 C:\Users\micha_1chy2aa\quant-study\debug\.venv\lib\site-packages\polars\_utils\construction\series.py:345(_construct_series_with_fallbacks)
     1000    0.553    0.001    0.553    0.001 {built-in method new_str}
    246/2    0.001    0.000    0.250    0.125 <frozen importlib._bootstrap>:1022(_find_and_load)
    246/2    0.001    0.000    0.250    0.125 <frozen importlib._bootstrap>:987(_find_and_load_unlocked)
    236/2    0.001    0.000    0.249    0.124 <frozen importlib._bootstrap>:664(_load_unlocked)
    217/2    0.001    0.000    0.248    0.124 <frozen importlib._bootstrap_external>:877(exec_module)

    

    RESULT: 20 seconds(excluding the sleep) ----> reduced to 5 seconds
    FUTHER WORK could likely get below 1s by vectorising the other loops 
    but reduce clean_text and build_dictionary to just a coulple lines which 
    is not something i want to do right now
'''