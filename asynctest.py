import asyncio


async def derp():
    print("Hello ...")
    await asyncio.sleep(5)
    print("... World!")


async def deep():
    print("Meow ...")
    await asyncio.sleep(3)
    print("... Woof!")


async def main():
    print("hello")
    task1 = asyncio.create_task(deep())
    task2 = asyncio.create_task(derp())
    print("goodbye!")

    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
