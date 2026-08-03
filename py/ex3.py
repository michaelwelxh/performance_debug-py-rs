import functools

class Processor:
    @staticmethod
    @functools.lru_cache(maxsize=10_000)
    def process(item_id, data):
        return expensive_computation(item_id, data)
    '''
    Why that's bad in a long-running service:

    Every Processor instance you ever create gets cached-in as part of some key, forever (unless evicted)
    Even if a Processor instance would normally get garbage collected, the cache holds a reference to self — so it never dies
    You end up with a growing cache of results tied to dead objects that never get cleaned up



    # Option B: separate the cache from the instance entirely
    @functools.lru_cache(maxsize=1000)
    def _process_cached(item_id, data):
        return expensive_computation(item_id, data)

    class Processor:
        def process(self, item_id, data):
            return _process_cached(item_id, data)

'''

'''
    Original code 
    import functools

    class Processor:
        @functools.lru_cache(maxsize=None)
        def process(self, item_id, data):
            return expensive_computation(data)


    '''