def swap(arr_,i,j):
    if(i == j):
        return
    else:
        # arr_[i] = arr_[i] + arr_[j]
        # arr_[j] = arr_[i] - arr_[j]
        # arr_[i] = arr_[i] - arr_[j]
        arr_[i],arr_[j] = arr_[j],arr_[i]
    return
# Write method to partition
def partition(arr_,st_idx,end_idx):
    # step 1: get the first value in the right place
    val_1 = arr_[st_idx]
    idx_2_ = 0 
    for i in range(st_idx+1,end_idx + 1):
        if(arr_[i]<= val_1):
            idx_2_+=1
    #print(idx_2_)
    idx_2 = st_idx + idx_2_
    swap(arr_,st_idx,idx_2)
    # step 2: set an index i at zeroth position and index j at last position of array, if arr_[i] > arr[val2_idx],pause i and if arr_[j] < arr[val2_idx], stop j, then swap and keep doing this, stop when i >= j

    idx_1  = st_idx
    
    idx_3 = end_idx

    #print(idx_1,idx_2,idx_3)

    while(idx_1<idx_3):

        if((arr_[idx_1]<= arr_[idx_2]) & (idx_1<idx_2)):
            idx_1+=1
        
        if((arr_[idx_2]<=arr_[idx_3]) & (idx_3>idx_2)):
            idx_3-=1

        swap(arr_,idx_1,idx_3)
        
        
    return idx_2

# Write method for quicksort

def quicksort(arr_,st_idx,end_idx):
    
    if((len(arr_)<=1)|(st_idx>=end_idx)):
        return
    
    idx_partition = partition(arr_,st_idx,end_idx)

    quicksort(arr_,st_idx,idx_partition-1)
   
    quicksort(arr_,idx_partition+1,end_idx)
    

arr_ = [12,4,3,11,1,9,8,7]
quicksort(arr_,0,7)
print(arr_)