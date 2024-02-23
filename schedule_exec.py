import schedule
import time
import datetime

def job1():
    print("job1:",datetime.datetime.now())

def job2():
    print("job2:",datetime.datetime.now())

def job3():
    print("job3:",datetime.datetime.now())

if __name__=="__main__":
    schedule.every(2).seconds.do(job1)
    schedule.every(1).minutes.do(job2)
    schedule.every().minute.at(":23").do(job3)

    print("start:",datetime.datetime.now())

    while True:
        schedule.run_pending()
        time.sleep(1)
