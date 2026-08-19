

## Q11 asyncio: the cancellation that doesn't cancel


"""
TASK:
  This is supposed to time out after 2 seconds and clean up a "connection".
  It doesn't behave the way you'd expect. Figure out why, fix it.

  Questions to answer before you fix anything:
    - What does asyncio.CancelledError actually do when raised inside a task?
        silently waits add to the end of the event quque 
        but the computaiotn is infinate and never releaves controls thus deadlocks never leting the error be noticed 

    - Why does the "cleanup" not happen where you'd expect?
        not sure -> there is no clean up as it never terminates

    - What's different between cancelling a task that's mid-await on I/O vs one that's running a tight CPU-bound loop?
        tight CPU-bound loop never will reach the await so the event loop never gets the cancel call 
        mid-await on I/O is suspoended so the event loop can inject canceledError into it thus the finaly block and clean up can run

    -> key point is running heavy CPU work on the event loop is not the correct design for a real system seperate threads for these two things is needed
"""

import asyncio

class Connection:
    def __init__(self):
        self.open = True

    async def close(self):
        await asyncio.sleep(0.1)
        self.open = False
        print("connection closed")


async def worker(conn):
    
    try:
        while True:
            print("working...")
            # simulate blocking CPU work, not I/O
            total = 0
            for i in range(10_000_000):
                total += i
                if total % 100_000 == 0:
                    await asyncio.sleep(0) # a real solution would actually be a process pool or not working on the event loop thread 
    finally:
        await conn.close()


async def main():
    conn = Connection()
    task = asyncio.create_task(worker(conn))
    await asyncio.sleep(2)
    task.cancel()
    await task


asyncio.run(main())
