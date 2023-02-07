import concurrent.futures
import time

def download_file(file_name):
    # Simulating a long running IO-bound task
    time.sleep(2)
    return f"{file_name} downloaded"

def main_chatgpt():
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # List of IO tasks to be executed concurrently
        files = ['file1.txt', 'file2.txt', 'file3.txt']

        # Submit the tasks to the executor and retrieve the results as they complete
        results = [executor.submit(download_file, file) for file in files]

        for f in concurrent.futures.as_completed(results):
            print(f.result())

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


def get_opm():
    for i in range(10):
        time.sleep(0.4)
        print(f'ReadOPM {i}')


def get_voa():
    for i in range(10):
        time.sleep(0.6)
        print(f'ReadVOA {i}')


@timer
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        func_list = [get_opm, get_voa]
        tasks = [executor.submit(f) for f in func_list]

        for t in concurrent.futures.as_completed(tasks):
            print(t.result())


if __name__ == '__main__':
    main()
