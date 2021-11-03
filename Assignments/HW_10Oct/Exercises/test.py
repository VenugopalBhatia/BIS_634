from Exercises import Ex4
from time import perf_counter
import numpy as np
import importlib
importlib.reload(Ex4)

def run_test(n_arr):
    time_taken = {'parallel':{},'regular':{}}

    for i in n_arr:
        lst = np.random.randint(1,1000000000,size = i)
        lst2 = lst.copy()
        lst2.sort()

        t_parallel_start = perf_counter()
        l_parallel = Ex4.mergeSort_parallelized(lst)
        t_parallel_stop = perf_counter()
        time_taken['parallel'][str(i)] = t_parallel_stop - t_parallel_start
        if(not np.array_equal(l_parallel,lst2)):
            print("sorting issue")
            return (lst2,l_parallel)

        t_regular_start = perf_counter()
        l_regular = Ex4.mergeSort(lst)
        t_regular_stop = perf_counter()
        time_taken['regular'][str(i)] = t_regular_stop - t_regular_start

        if(not np.array_equal(l_regular,lst2)):
            print("sorting issue")
            return (lst2,l_regular)
        
    return time_taken

