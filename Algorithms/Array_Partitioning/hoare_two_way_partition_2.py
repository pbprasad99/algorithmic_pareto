
from typing import List
import random

# Given a list return partition index after partition on the pivot index value
def partition(nums: List[int],lo,hi) -> int :
    """
    Hoare partition with strong condition.
    Here we modififed the code slightly to:
    Fix pivot value at index zero.
    Partition by the pivot value.
    Finally place the pivot  at the end of the left partition.
    This implementation puts pivot in the sorted position as well after partitioning.
    This version is  not entropy optimal . That is, it does not lead to balanced partitions when there are a lot of duplicates. 

    Why? Consider,  if this partition scheme is used in quickselect for finding the smallest element in an array of size n). 
    What happens when all elements are duplicates (disregarding random pivot selection):
    [1,1,1,1,1,1]
     l         r   Iter 1 : 6  comparisons
     l       r     Iter 2 : 5  comparisons
     l     r       Iter 3 : 4  comparisons
     l   r         Iter 4 : 3  comparisons
     l r           Iter 5 : 2  comparisons
     lr            Iter 6 : 1  comparisons

    Number of comparisons = SUM([1.....n]) = n(n+1)/2 = (n*2 + n ) /2
    Therefore, Complexity is O(n^2) 
    """

    print(f"Input List : {nums}")
    left, right = lo,hi
    
    # RANDOM PIVOT SELECTION
    # Always keep pivot at index lo
    # pivot_index = random.randint(lo,hi)
    # nums[lo],nums[pivot_index] =  nums[pivot_index],nums[lo]

    #PARTITIONING
    left+=1
    pivot_val = nums[lo]

    while left <= right :

        while left <= right and nums[left] <= pivot_val :
            left+=1
        
        while left <= right and nums[right] > pivot_val :
            right-=1

        if left < right :
            #swap
            nums[left],nums[right] = nums[right],nums[left]

    #Put pivot Value in sorted  position
    nums[lo] , nums[right] =  nums[right] ,nums[lo]
    print(f"Pivot Value: {pivot_val}  ,Partitioned list : {nums}, Partition Index = {right}")
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