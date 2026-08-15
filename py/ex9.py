'''

## Q9 asyncio internals (conceptual, no code to run)

No starter code needed this one's meant to be answered from understanding, then checked against real behavior if you want.

**Question:** Walk through, step by step, what actually happens when you call:

Answer in detail what happens between `print("before")` and `print("after")`:
- What does `await asyncio.sleep(1)` actually return/do under the hood?
- What does the event loop do with control while this coroutine is "waiting"?
- What data structure is `foo`'s continuation stored in, and how does the loop know when to resume it?
- What's the difference between what happens here vs. what happens if you `await` a coroutine that does no I/O at all (e.g. `await asyncio.sleep(0)`)?

Once you've written your answer, try verifying it by reading `asyncio.sleep`'s and `BaseEventLoop._run_once`'s source, or by instrumenting with `asyncio` debug mode (`PYTHONASYNCIODEBUG=1`) and logging loop callbacks.
'''
import asyncio

async def foo():
    print("before")
    await asyncio.sleep(1)
    print("after")

if __name__ == '__main__':
    asyncio.run(foo())