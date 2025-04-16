

from typing import List
import random

def quickselect(arr: List[int],lo: int,hi: int,k : int) -> int :
    """
    Quickselect using Hoare partition with a weak condition and fixed pivot. 

    This is the implementation which you will find in textbooks using do..while style loops which in python becomes while True loops.
    I prefer avoiding white True loops. 
    It's still using Hoare partition with a weak condition. But the pivot selection is not random.
    Notice how the performance degrades to O(n^2) for sorted array because the pivot selection is not random.
    Compare this with next version which uses a random pivot.
    """
    v = arr[lo]
    i = lo
    j = hi+1
    while True:
        while True:
            i += 1
            if not (i < hi and arr[i] < v):
                break
        while True:
            j -= 1
            if not (j > lo and arr[j] > v):
                break
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]
    arr[lo], arr[j] = arr[j], arr[lo]
    
    print(f"Pivot Value: {v}  ,Partitioned list : {arr}, Partition Index = {j} , le = {lo}, hi = {hi}, k = {1}")
    if k -1  == j :
        print(f"Returning index {j}")
        return nums[j]
    elif k -1 > j : 
        return quickselect(nums,j+1,hi,k)
    else :
        return quickselect(nums,lo,j-1,k)

if __name__ == "__main__" :
    # nums = [5,2,1,1,1,1,1,1,1,1,1,5,5,-3,1,1,1,1,1,1,1,1,1,1,1-2,-5]               # O(nlogn)
    nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # O(nlogn)
    # nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]  #degrades to O(n^2)
    # nums = [24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]  #O(nlogn)
    print( 
           f"kth_largest = { quickselect(nums, 0, len(nums)-1 ,23) }" 
          )

    # nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # O(nlogn)
    # print( 
    #        f"kth_largest = { quickselect(nums, 0, len(nums)-1 ,1) }" 
    #       )
        



