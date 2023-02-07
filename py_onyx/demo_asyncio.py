import asyncio
import time

async def download_file(file_name):
    # Simulating a long running IO-bound task
    await asyncio.sleep(2)
    return f"{file_name} downloaded"

async def main_chatgpt():
    start_time = time.time()

    # List of IO tasks to be executed concurrently
    files = ['file1.txt', 'file2.txt', 'file3.txt']

    # Schedule the tasks to run concurrently
    tasks = [asyncio.create_task(download_file(file)) for file in files]

    # Wait for all tasks to finish
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

    end_time = time.time()

    print(f"\nTotal time taken: {end_time - start_time:.2f} seconds")


def timer(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        rtn = func(*args, **kwargs)
        t1 = time.time()
        print(f'Finished in {t1 - t0} secs')

        return rtn
    return wrapper


async def get_opm():
    for i in range(10):
        await asyncio.sleep(0.4)
        print(f'ReadOPM {i}')
    return 'OPM reading done'


async def get_voa():
    for i in range(10):
        await asyncio.sleep(0.6)
        print(f'ReadVOA {i}')
    return 'VOA reading done'


@timer
async def main():
    task1 = asyncio.create_task(get_opm())
    task2 = asyncio.create_task(get_voa())

    rst1, rst2 = await asyncio.gather(task1, task2)

    print(rst1)
    print(rst2)


if __name__ == '__main__':
    asyncio.run(main())
