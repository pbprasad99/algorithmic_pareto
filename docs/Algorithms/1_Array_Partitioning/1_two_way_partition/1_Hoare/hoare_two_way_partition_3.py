from typing import List
import random


def partition(arr, lo, hi):
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
    print(f"Pivot Value: {pivot}  ,Partitioned list : {arr}, Partition Index = {right}")
    return right

if __name__ == "__main__" : 
    # nums= [1,2,3]
    # partition(nums, 0, len(nums)-1)
    # nums = [2,2,2,2]
    # partition(nums, 0, len(nums)-1)
    # nums = [2,4,5,1,4,8,9]
    # partition(nums, 0, len(nums)-1)
    # nums= [3,2]
    # partition(nums, 0, len(nums)-1)
    # nums= [3]
    # partition(nums, 0, len(nums)-1)
    nums = [5,2,1,1,1,1,1,1,1,1,1,5,5,-3,-2,-5]
    partition(nums, 0, len(nums)-1)