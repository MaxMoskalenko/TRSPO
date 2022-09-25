import random
import threading

LOOPS_IN_THREAD_INTERVAL = (10_000, 20_000)
RANDOM_NUMBER_INTERVAL = (0, 9)
THREADS_NUMBER_INTERVAL = (10, 20)


class DataClass:
    # Classes are the same, so no need to duplicate it twice
    def __init__(self):
        self.__data = 0

    def set(self, value):
        self.__data = value

    def get(self):
        return self.__data


def thread_function(obj1, obj2, thread_index):
    print("Thread %i is started" % thread_index)

    k = random.randint(*LOOPS_IN_THREAD_INTERVAL)

    for _ in range(k):
        new_obj1_data = random.randint(*RANDOM_NUMBER_INTERVAL) + obj1.get()
        obj1.set(new_obj1_data)

        new_obj2_data = random.randint(*RANDOM_NUMBER_INTERVAL) + obj2.get()
        obj2.set(new_obj2_data)

    print("Thread %i is finished" % thread_index)


if __name__ == "__main__":
    obj1 = DataClass()
    obj2 = DataClass()

    n = random.randint(*THREADS_NUMBER_INTERVAL)
    thread_pool = []

    # First half and the second half of threads have the same function, so
    # it's no difference between them
    for i in range(n):
        new_th = threading.Thread(
            target=thread_function, args=(obj1, obj2, i,)
        )
        thread_pool.append(new_th)

    for th in thread_pool:
        th.start()

    for th in thread_pool:
        th.join()

    print("All threads finished their work")
    print("Results:\n\tobj1: %i\n\tobj2: %i" % (obj1.get(), obj2.get()))
