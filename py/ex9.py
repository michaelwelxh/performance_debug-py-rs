'''

## Q9 asyncio internals (conceptual, no code to run)

No starter code needed this one's meant to be answered from understanding, then checked against real behavior if you want.

**Question:** Walk through, step by step, what actually happens when you call:

Answer in detail what happens between `print("before")` and `print("after")`:
- What does `await asyncio.sleep(1)` actually return/do under the hood?
    it tells the coroutine function to wait for one sencond allowing the evenet loops previously called code to complete more computation
        to the event loop yeild in complete asyncio.Future object, signalling that the coroutine is blocked.
        to the code return None once time completed

        registrationa and suspension 
            check the threads event loop to get runnning instance
            initalise black future object
            calcs wake time stamp with loop.time() then pushes call back function  _set_result..... with time stap on to time heap 
            yeild control.....

        event loop napping 

        waking up 

- What does the event loop do with control while this coroutine is "waiting"?
- What data structure is `foo`'s continuation stored in, and how does the loop know when to resume it?
- What's the difference between what happens here vs. what happens if you `await` a coroutine that does no I/O at all (e.g. `await asyncio.sleep(0)`)?

Once you've written your answer, try verifying it by reading `asyncio.sleep`'s and `BaseEventLoop._run_once`'s source, or by instrumenting with `asyncio` debug mode 
(`PYTHONASYNCIODEBUG=1`) and logging loop callbacks.
'''
import asyncio

async def foo():
    print("before")
    await asyncio.sleep(1)
    print("after")

if __name__ == '__main__':
    asyncio.run(foo())