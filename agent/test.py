import threading
import time


def task(arg):
    time.sleep(2)
    print(arg)

for i in range(100):
    t = threading.Thread(target=task,args=(i,))
    print(i)
    t.start()

print("end")