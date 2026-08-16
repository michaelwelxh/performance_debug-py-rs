'''

## Q9 asyncio internals (conceptual, no code to run)

No starter code needed this one's meant to be answered from understanding, then checked against real behavior if you want.

**Question:** Walk through, step by step, what actually happens when you call:

Answer in detail what happens between `print("before")` and `print("after")`:
- What does `await asyncio.sleep(1)` actually return/do under the hood?
    it tells the coroutine function to wait for one sencond allowing the evenet loops previously called code to complete more computation

- What does the event loop do with control while this coroutine is "waiting"?
    continues exevuting its avalible events but does not accept any more to be added
- What data structure is `foo`'s continuation stored in, and how does the loop know when to resume it?
    answer queue or heap?, and when the timer returns None or not None?
        a. enent timer is a heap 
        b. event loop uses 'ready' heap and i assume 'blocked' queue

        1. asyncio.sleep() does return None eventually but thats not what wakes it. just the exposed view of it
        ( 
        result = await asyncio.sleep(1)
            sleep() -> 
            create Future -> 
            schedule timer to complete Future after 1 sec -> 
            await Future  -> 
            Task suspends -> 
            timer fires -> 
            Future.set_result(None) -> 
            Future's callbacks run -> 
            Task gets scheduled -> 
            Task resumes coroutine -> 
            result = None
        )
- What's the difference between what happens here vs. what happens if you `await` a coroutine that does no I/O at all (e.g. `await asyncio.sleep(0)`)?
    sleep would eccentially just yeild its position in the queue to another task and be added to the end of the loop 
Once you've written your answer, try verifying it by reading `asyncio.sleep`'s and `BaseEventLoop._run_once`'s source, or by instrumenting with `asyncio` debug mode 
(`PYTHONASYNCIODEBUG=1`) and logging loop callbacks.
'''
import asyncio

async def foo():
    for i in range(5):
        print("FOO", i)
        await asyncio.sleep(0)
    print("FOO done")

async def bar():
    for i in range(5):
        print("BAR", i)
        await asyncio.sleep(0)              # after every call it essentially yeild control and is enqueued to the end of event queue - as seen in the output below
    print("BAR done")

async def main():
    await asyncio.gather(foo(), bar())

if __name__ == '__main__':
    asyncio.run(main())

'''
FOO 0
BAR 0

FOO 1
BAR 1

FOO 2
BAR 2
FOO 3
BAR 3
FOO 4
BAR 4
FOO done
BAR done
'''