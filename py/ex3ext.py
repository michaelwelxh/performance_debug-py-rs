"""
Demonstrates the functools.lru_cache-on-self memory leak.

Watch the object counts printed for BROKEN vs FIXED versions.
"""

import functools
import gc
import time


def expensive_computation(item_id, data):
    # Stand-in for "real work" - just something deterministic
    time.sleep(0.001)
    return sum(data) + item_id


# ---------------------------------------------------------------------------
# BROKEN: lru_cache on an instance method caches (self, item_id, data)
# ---------------------------------------------------------------------------
class ProcessorBroken:
    def __init__(self, name):
        self.name = name

    @functools.lru_cache(maxsize=None)
    def process(self, item_id, data):
        return expensive_computation(item_id, data)


# ---------------------------------------------------------------------------
# FIXED (Option B): cache lives outside the instance, keyed only on real inputs
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=1000)
def _process_cached(item_id, data):
    return expensive_computation(item_id, data)


class ProcessorFixed:
    def __init__(self, name):
        self.name = name

    def process(self, item_id, data):
        return _process_cached(item_id, data)


def count_processor_instances(cls):
    gc.collect()
    return sum(1 for obj in gc.get_objects() if isinstance(obj, cls))


def run_broken(n=2000):
    print("\n--- BROKEN VERSION ---")
    for i in range(n):
        p = ProcessorBroken(f"proc-{i}")
        p.process(i, (1, 2, 3))
        # p goes out of scope here on each loop iteration should be
        # garbage collected... but the cache is holding a reference to it.

    alive = count_processor_instances(ProcessorBroken)
    cache_info = ProcessorBroken.process.cache_info()
    print(f"Processor instances still alive after loop: {alive}")
    print(f"Cache info: {cache_info}")
    print("-> Every instance is still alive because lru_cache holds `self`.")


def run_fixed(n=2000):
    print("\n--- FIXED VERSION ---")
    for i in range(n):
        p = ProcessorFixed(f"proc-{i}")
        p.process(i, (1, 2, 3))

    alive = count_processor_instances(ProcessorFixed)
    cache_info = _process_cached.cache_info()
    print(f"Processor instances still alive after loop: {alive}")
    print(f"Cache info: {cache_info}")
    print("-> Instances get garbage collected normally; cache only holds inputs.")


if __name__ == "__main__":
    run_broken()
    run_fixed()