

from typing import List
import random


def hoare_partition(arr, lo, hi):
    """
    Entropy Optimal Hoare partition.
    Produces balanced partitions when there are large number of duplicates.
    [lo,right] contains elements less than or equal to pivot.
    (right,hi]  contains elements greater than or equal to pivot.
    Invariants for the while loop :
    [lo] has pivot  
    [lo, left)  <= pivot    #Has values <= pivot
    (right, hi] >= pivot
    [pivot|--- <=pivot-----|-----Undetermined-------|--->=pivot----]
                            left               right
    After execution of while loop : 
    [pivot|----<=pivot------|----->=pivot------]
    lo                  right                  hi
    [lo,right] <= pivot
    After Putting pivot in sorted position : 
    [----<=pivot----|pivot|----->=pivot------]
    lo               right                  hi
    Finally, return right.
    """
    #PIVOT SELECTION
    #Pick a random pivot index and always keep pivot at index lo
    #NB:  random.randint(0,0) is 0.
    pivot_index = random.randint(lo,hi)
    arr[lo],arr[pivot_index] =  arr[pivot_index],arr[lo]
    #read pivot value
    pivot = arr[lo]
    
    #PARTITIONING
    #partition [lo+1,hi] ; 
    #NB : when lo == hi , while loop will not be executed
    left,right = lo+1, hi
    while left<=right:
        #Move left ahead if arr[left] is strictly less than pivot value
        while left <= right and arr[left] < pivot :
            left+=1
        #Move right to the left if it is strictly higher than pivot
        while left <= right  and arr[right] > pivot :
            right-=1
        #Swap left and right and move pointers
        #If both values are equal to pivot this will do a swap,move pointers and effectively leave pivot values where they are. 
        if left <=  right :
            arr[left], arr[right] = arr[right], arr[left]
            right-=1
            left+=1
    #Put pivot in sorted position
    arr[lo], arr[right] = arr[right], arr[lo]
    return right

def quickselect(arr: List[int],lo: int,hi: int,k : int) -> int :
    """
    Quicselect using Hoare partition with weak condition and random pivot.
    Return vlaue at Kth SMALLEST Index,
    Returns the non decreasingly sorted value at kth Index with indices starting from lo. [lo ,hi] is inclusive.
    This uses Hoare's partition scheme with a weak condition and which also puts pivot in its sorted position.
    """ 
    pivot_index = hoare_partition(arr,lo,hi)
    print(f"Pivot Value: {arr[pivot_index]}  ,Partitioned list : {arr}, Partition Index = {pivot_index} , le = {lo}, hi = {hi}, k = {k}")
    if k == pivot_index :
        return arr[k]
    if k < pivot_index :
        return quickselect(arr,lo, pivot_index-1,k)
    elif k > pivot_index :  
         return quickselect(arr,pivot_index+1,hi,k)

        

if __name__ == "__main__" :
    # nums = [5,2,1,1,1,1,1,1,1,1,1,5,5,-3,1,1,1,1,1,1,1,1,1,1,1-2,-5]                 # O(nlogn)
    # nums = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # Close to O(nlogn)
    nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]  #STill close to O(nlogn) . WIthout random pivot degrades to O(n^2)
    # nums = [24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]  #O(nlogn)
    print( 
           f"kth_largest = { quickselect(nums, 0, len(nums)-1 ,23) }" 
          )