import asyncio

async def fetch_data(id):
    await asyncio.sleep(1)
    return id * 2
'''
async def main():
    results = []
    for id in range(10):
        result = ->await fetch_data(id)
        results.append(result)
    print(results)

    Calling fetch_data(id) just creates a coroutine object — it doesn't run it. 
    So results ends up full of coroutine objects, and because nothing ever 
    awaits them, none of them actually execute concurrently (or at all, until 
    Python complains about it via a RuntimeWarning: coroutine was never awaited).

    Even if you fixed that naively with await fetch_data(id) inside the loop, you'd 
    get correct results but it'd run sequentially — 10 seconds total instead of ~1 
    — because each await blocks until that one coroutine finishes before starting 
    the next.
'''
async def main():
    results = await asyncio.gather(*(fetch_data(id) for id in range(10)))
    print(results)

asyncio.run(main())