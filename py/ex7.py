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
import time



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
        # 4 -> Cprofile tells me it was called 100_000 times which would be here -> assuming theres no actual bug in the code so far the fix would be to use polars and
        #  vectorise this computaion but ill do a little bit of reserch first to find out if that the only thing i can do -> concurrency, paralelism, asyncio depending on functionality of code...
        valid_words = [w for w in words if is_valid_word(w, dictionary)]     
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
    time.sleep(15)
    print("resuming")
    dictionary = build_dictionary(size=50000)
    docs = generate_documents(n=500, words_per_doc=200)
    results = process_documents(docs, dictionary)             # 2