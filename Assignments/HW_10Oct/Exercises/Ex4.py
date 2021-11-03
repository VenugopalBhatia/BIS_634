## The merge sort is a divide and conquer alogrithm where we'd keep splitting the array in half recursively 
# up until the point where we just have single elements.
#  We'd have a function to merge sorted lists and since single element lists are sorted the merge operations will 
# then start returning sorted lists and we start popping out from the call stack  as the recursive function calls complete up until we have 
# one sorted array in the end which was our original array

# To parallelize this one method is to break the list up into chunks, 
# with each processor applying merge sort on each of the chunks and then we'd have to do
# one merge in the end for all the sorted lists from the processors.

# We could gauge performance improvements using time.perf_counter for regular versus parallelized merge sort 
# algorithms and see how the time required increases as n grows from 10, 100, 1000, 10000 and so on, a log log graph may 
# then be plotted to see improvements in the parallelized versus regular merge sort. For smaller data, the various overheads
# involved may cause it to be slower but as n grows the parallel version should give speedup. 
# 



# Here have written merge_npar and merge for working with np arrays and lists respectively. 
# Numpy arrays don't seem to be the best option here I think and sticking to plain old lists is probably better but wrote it anyway.
# Have called methods in a parallelized fashion, for 8 cores, it splits data into chunks of 8,
# sorts those and then 4 cores create 4 merged arrays, followed by 2 cores creating 2 merged arrays and a then final call to merge creates a merged array.
# Repeatedly closing and creating pools may be slowing it down, along with other tasks such as splitting data in chunks, etc. 
# Could you suggest a more efficient way of doing this?


import multiprocessing as mp
import numpy as np

def merge_nparr(arr1,arr2):
    mergedArr = []
    if((len(arr1) == 0)|(len(arr2) == 0)):
        return np.append(arr1,arr2)

    if(arr1[-1]<=arr2[0]):
        return np.append(arr1,arr2)
    elif(arr2[-1]<= arr1[0]):
         return np.append(arr2,arr1)

    i,j = 0,0
    while((i<len(arr1))&(j<len(arr2))):
        if(arr1[i]<arr2[j]):
            mergedArr = np.append(mergedArr,arr1[i]) #np append creates copies which isn't great but wrote this method for np arrays anyway
            i+=1
        elif(arr2[j]<=arr1[i]):
            mergedArr = np.append(mergedArr,arr2[j])
            j+=1
    
    if(i<len(arr1)):
        mergedArr = np.append(mergedArr,arr1[i:])
    if(j<len(arr2)):
        mergedArr = np.append(mergedArr,arr2[j:])
        
    return mergedArr

def merge(arr1,arr2):
    mergedArr = []
    if(arr1[-1]<=arr2[0]):
        return arr1 + arr2
    elif(arr2[-1]<= arr1[0]):
         return arr2 + arr1

    i,j = 0,0
    while((i<len(arr1))&(j<len(arr2))):
        if(arr1[i]<arr2[j]):
            mergedArr.append(arr1[i])
            i+=1
        elif(arr2[j]<=arr1[i]):
            mergedArr.append(arr2[j])
            j+=1
    
    if(i<len(arr1)):
        mergedArr.extend(arr1[i:])
    if(j<len(arr2)):
        mergedArr.extend(arr2[j:])
        
    return mergedArr


def mergeSort(arr):
    if(len(arr) <= 1):
        return arr
    k = (len(arr))//2
    left = mergeSort(arr[0:k])
    right = mergeSort(arr[k:])
    if(type(arr) == np.ndarray):
        return merge_nparr(left,right)
    else:
        return merge(left,right)
    

def mergeSort_parallelized(lst):
    num_cpus = mp.cpu_count()
    pool = mp.Pool(num_cpus)
    
    #print("unsorted list\n",lst)
    stepSize = len(lst)//num_cpus
    step = max(4,stepSize)


    #ll = [lst[i:(i+step)] for i in range(0,len(lst),step)]
    ll = np.array_split(lst,num_cpus)
    #print(ll)
    
    def mgsrt_cb(arr):
        #print(arr)
        sorted_arrays.append(arr)
    # for i in ll:
    #     pool.apply_async(Ex4.mergeSort,args = (i,),callback = mgsrt_cb)

    sorted_arr_objs = [pool.apply_async(mergeSort,args = (i,)) for i in ll]
    sorted_arrays = [arr_obj.get() for arr_obj in sorted_arr_objs]
    
    
    # pool.close()   #closing and then creating new pools doesn't seem ideal, something like queuing tasks could help here. Kindly guide as to how to optimize this
    # pool.join()
    #print(sorted_arrays)
    
    #pool = mp.Pool(num_cpus//2)
    merged_arr_objs = [pool.apply_async(merge_nparr,args = sorted_arrays[i:i+2]) for i in range(0,len(sorted_arrays)-1,2)]
    merged_arrays = [merged_arr_obj.get() for merged_arr_obj in merged_arr_objs]
    # merged_arrays = []
    # for i in range(0,7,2):
    #     if(type(sorted_arrays) == np.ndarray):
    #         pool.apply_async(Ex4.merge,args = sorted_arrays[i:i+2],callback=)
    # pool.close()
    # pool.join()

    #pool = mp.Pool(num_cpus//4)
    merged_arr_objs2 = [pool.apply_async(merge_nparr,args = merged_arrays[i:i+2]) for i in range(0,len(merged_arrays)-1,2)]
    merged_arrays2 = [merged_arr_obj2.get() for merged_arr_obj2 in merged_arr_objs2]
    pool.close()
    pool.join()
    arr_sorted = merge_nparr(merged_arrays2[0],merged_arrays2[1])
    return arr_sorted

    
    