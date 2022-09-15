import threading
import time

def sleep(duration):
    time.sleep(duration)

if __name__ == "__main__":
    t0 = time.time()

    # Creating threads with delay in 1, 2 and 3 seconds
    th1 = threading.Thread(target=sleep, args=(1,))
    th2 = threading.Thread(target=sleep, args=(2,))
    th3 = threading.Thread(target=sleep, args=(3,))
    th1.start()
    th2.start()
    th3.start()

    # Waiting for each thread finish
    th1.join()
    th2.join()
    th3.join()

    # Expected execution time is ~3 seconds as the longest delay
    t1 = time.time()
    print("Execution time %i ms" % ((t1-t0) * 1000))
