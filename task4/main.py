# mpiexec -n 4 python3 main.py
import math
import time
from mpi4py import MPI
import numpy as np

def is_in_circle(point):
    d = ((point[0])**2 + (point[1])**2)**0.5
    if d <= 1:
        return True
    else:
        return False

def pi_monte_carlo(array):
    in_circle = np.count_nonzero(((array.T[0])**2 + (array.T[1])**2)**0.5 <= 1)

    return (in_circle/len(array))*4


comm = MPI.COMM_WORLD
mpi_size = comm.Get_size()
mpi_rank = comm.Get_rank()

if __name__ == "__main__":
    data_to_scatter = None
    if mpi_rank == 0:
        print("🎬 main process started")

        n = 10_000_000
        chunk_length = math.ceil(n / mpi_size)
        arr = np.random.rand(n, 2)

        print("🎰 array generated")

        data_to_scatter = [arr[0: (i+1) * chunk_length]
                           for i in range(0, mpi_size)]

        print("📦 array divided into chunks")

    dots = comm.scatter(data_to_scatter, root=0)
    print("📦 received scattered data for process", mpi_rank)

    t0 = time.time()
    pi = pi_monte_carlo(dots)
    t1 = time.time()

    print("✅ finished calculating pi for process", mpi_rank)
    results = comm.gather({"time": (t1-t0) * 1000, "pi": pi}, root=0)

    if mpi_rank == 0:
        print("📦 results gathered")
        for result in results:
            print("⏰ time(ms): %i; pi: %.10f" %
                  (result["time"], result["pi"]))
