Q1. The silent asyncio bug

```python
import asyncio

async def fetch_data(id):
    await asyncio.sleep(1)
    return id * 2

async def main():
    results = []
    for id in range(10):
        result = fetch_data(id)
        results.append(result)
    print(results)

asyncio.run(main())
```
Task: this prints coroutine objects, not results, and takes way longer than it should. Fix it to run concurrently and return actual values.

Q2. The GIL trap

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # expected 4,000,000, but it's not
```
Task: explain why this is wrong despite the GIL (hint: it's not what people assume), then fix it properly and explain when threading would actually help here vs when it wouldn't.

Q3. Memory leak in a "cache"

```python
import functools

class Processor:
    @functools.lru_cache(maxsize=None)
    def process(self, item_id, data):
        return expensive_computation(data)
```
Task: this leaks memory in long-running services. Why? Fix it. (Hint: self is part of the cache key.)

Q4. NumPy vs loop. spot the antipattern

```python
import numpy as np

def normalize(arr):
    result = np.zeros(len(arr))
    for i in range(len(arr)):
        result[i] = (arr[i] - arr.mean()) / arr.std()
    return result
```
Task: this is O(n²) in wall time due to .mean()/.std() being recomputed every iteration, plus it's not vectorized. Fix it, then profile before/after with %timeit or time.perf_counter.

Q5. The polars/pandas gotcha

```python
import pandas as pd

df = pd.DataFrame({'a': range(1_000_000)})
total = 0
for i in range(len(df)):
    total += df.iloc[i]['a']

```

Task: rewrite for at least 100x speedup using vectorized ops. Bonus: rewrite in Polars and compare.

## Q6 Find the real bottleneck with cProfile

```python
"""
TASK:
  This script processes a list of "log records" and builds a summary report.
  It's slow.

  1. Profile it with cProfile yourself (command line or programmatic your choice).
  2. Identify the ACTUAL bottleneck. It's probably not what you'd guess just
     from reading top to bottom.
  3. Fix it. Confirm at least a 10x speedup.
  4. Output must stay the same shape (same return values).
"""

import random


def generate_records(n=20000):
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
    return records


def build_report(records):
    """Builds a summary: per-user message log as a single string, plus level counts."""
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
            counts[w] = words.count(w)
        user_word_counts[user] = counts

    return report, level_counts, user_word_counts
```

---

## Q7 py-spy: find where CPU time is really going

```python
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


def clean_text(text):
    # looks fine at a glance
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text


def is_valid_word(word, dictionary):
    # dictionary is a list, not a set -- on purpose
    return word in dictionary


def process_documents(documents, dictionary):
    results = []
    for doc in documents:
        cleaned = clean_text(doc)
        words = cleaned.split()
        valid_words = [w for w in words if is_valid_word(w, dictionary)]
        results.append(valid_words)
    return results


def build_dictionary(size=50000):
    return [f"word{i}" for i in range(size)]


def generate_documents(n=500, words_per_doc=200):
    import random
    random.seed(1)
    docs = []
    for _ in range(n):
        words = [f"word{random.randint(0, 60000)}" for _ in range(words_per_doc)]
        docs.append(" ".join(words))
    return docs
```

---

## Q8 String concatenation vs `''.join()`

```python
"""
TASK:
  Two implementations of the same function below: build a big string from
  a list of pieces.

  1. Predict the asymptotic difference (Big-O) between concat_loop and
     concat_join before running anything.
  2. Verify with cProfile or timeit yourself.
  3. Explain WHY the difference exists at the level of what CPython is doing
     with string immutability and memory allocation. not just "join is faster".
"""

def concat_loop(pieces):
    result = ""
    for p in pieces:
        result += p
    return result


def concat_join(pieces):
    return "".join(pieces)


def generate_pieces(n=100000):
    return [f"piece_{i}_" for i in range(n)]
```

---

## Q9 asyncio internals (conceptual, no code to run)

No starter code needed this one's meant to be answered from understanding, then checked against real behavior if you want.

**Question:** Walk through, step by step, what actually happens when you call:

```python
async def foo():
    print("before")
    await asyncio.sleep(1)
    print("after")

asyncio.run(foo())
```

Answer in detail what happens between `print("before")` and `print("after")`:
- What does `await asyncio.sleep(1)` actually return/do under the hood?
- What does the event loop do with control while this coroutine is "waiting"?
- What data structure is `foo`'s continuation stored in, and how does the loop know when to resume it?
- What's the difference between what happens here vs. what happens if you `await` a coroutine that does no I/O at all (e.g. `await asyncio.sleep(0)`)?

Once you've written your answer, try verifying it by reading `asyncio.sleep`'s and `BaseEventLoop._run_once`'s source, or by instrumenting with `asyncio` debug mode (`PYTHONASYNCIODEBUG=1`) and logging loop callbacks.