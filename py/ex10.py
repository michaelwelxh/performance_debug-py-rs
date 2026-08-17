
'''
Q10. Given this code, identify why a single slow synchronous call inside an async def blocks the entire event loop, 
and fix it using asyncio.to_thread or run_in_executor.
'''

import asyncio
import requests
import time


url = "http://localhost:8090/hello"  # go server



def process(data):
    return data.status_code

async def handler(request):
    print("before request")
    data = await asyncio.to_thread(requests.get, url)  # blocking call inside async function
    print("after request")
    return process(data)

async def og_handler(request):
    print("before request")
    data = requests.get(url)  # blocking call inside async function
    print("after request")

    return process(data)


# need to add other task to seen gains
async def other_task():
    for i in range(2):
        print("other task:", i)
        await asyncio.sleep(0.1)


async def main():
    request = None
    for i in range(2):
        await asyncio.gather(handler(None), other_task())

if __name__ == "__main__":
    start_ = time.perf_counter()
    asyncio.run(main())
    end_ = time.perf_counter()
    print(f"time: {end_-start_:.8f} seconds")

r'''

speed is similar but can see the handler be allowed to complete in the gap time 
instead of haveing to wait


async time 

before request
other task: 0
after request
other task: 1
before request
other task: 0
after request
other task: 1
time: 0.42015340 seconds

og time 

before request
after request
other task: 0
other task: 1
before request
after request
other task: 0
other task: 1
time: 0.46986450 seconds
'''