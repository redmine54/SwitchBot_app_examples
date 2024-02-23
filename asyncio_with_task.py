import asyncio
import time

async def say_after(delay, what):
    print(f"start>{what} at {time.strftime('%X')}")
    #await asyncio.sleep(delay)
    time.sleep(delay)
    print(f"stop>  {what} at {time.strftime('%X')}")
    return delay

async def main():
    print(f"start at {time.strftime('%X')}")

    time.sleep(1)
    task1=asyncio.create_task(say_after(8,"hello"))
    time.sleep(6)
    task2=asyncio.create_task(say_after(5,"world"))
    time.sleep(3)
    print(f"made task1,2 at {time.strftime('%X')}")

    time.sleep(4)
    print(f"await hello at {time.strftime('%X')}")
    result = await task1
    
    time.sleep(13)
    print(f"exit  hello result={result} at {time.strftime('%X')}")
    time.sleep(2)
    print(f"await world at {time.strftime('%X')}")
    result = await task2

    print(f"exit  world result={result} at {time.strftime('%X')}")

    print(f"stop  at {time.strftime('%X')}")

asyncio.run(main())
