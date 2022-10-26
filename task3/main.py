from multiprocessing import Manager, Pool
import time


class QueueElement:
    def __init__(self, initial_value, current_value, steps):
        self.initial_value = initial_value
        self.current_value = current_value
        self.steps = steps


def collatz(number):
    if number % 2 == 0:
        return int(number / 2)
    else:
        return 3*number + 1


def collatz_worker(q, result, N):
    element = q.get(block=True)

    # avoid infinite loop for 1
    if element.initial_value == 1:
        result[int(element.initial_value)] = 0
        return

    if element.current_value <= N and result[int(element.current_value)] != -1:
        result[int(element.initial_value)] = element.steps + \
            result[int(element.current_value)]
        return

    next_value = collatz(element.current_value)

    if next_value == 1:
        result[int(element.initial_value)] = element.steps + 1
        return

    q.put(QueueElement(element.initial_value,
                       next_value, element.steps + 1))


def work_on_queue(q, result, N):
    while not q.empty():
        collatz_worker(q, result, N)


if __name__ == "__main__":
    N = 1000

    m = Manager()
    q = m.Queue()
    result = m.list([-1 for _ in range(N+1)])
    th_n = 4

    t0 = time.time()

    with Pool(th_n) as p:
        p.map(q.put, [QueueElement(i + 1, i + 1, 0) for i in range(N)])
        p.starmap(work_on_queue, [(q, result, N) for _ in range(th_n)])

    t1 = time.time()
    print("Execution time %i ms" % ((t1-t0) * 1000))
