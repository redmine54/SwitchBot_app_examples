import threading
import time
import datetime

def task(t, thread_num):
    while True:
        print(" Thread {} t={} start {}".format(thread_num, t, datetime.datetime.now()))
        time.sleep(t)

if __name__=='__main__':
    thread1=threading.Thread(name="thread 1", target=task, args=(0.5,'A'))
    thread2=threading.Thread(name="thread 2", target=task, args=(2,'B'))
    thread1.start()
    thread2.start()
