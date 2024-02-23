import asyncio
import time

async def say_after(delay, what):
    print(f"start {what} at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"stop  {what} at {time.strftime('%X')}")

async def main():
    print(f"start at {time.strftime('%X')}")

    await  say_after(5,"hello")
    await  say_after(8,"world")


    print(f"stop  at {time.strftime('%X')}")

asyncio.run(main())
