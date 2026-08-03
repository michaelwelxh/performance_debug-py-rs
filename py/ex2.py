import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(1_000_000):
        with lock:             # counter += 1 is not atomic
            counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)  # expected 4,000,000, but it's not

'''
The GIL trap

Task: explain why this is wrong despite the GIL then fix it properly and 
explain when threading would actually help here vs when it wouldn't.
'''