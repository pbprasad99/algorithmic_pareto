
from typing import List

#Given a list return partition index after partition on the pivot index value
def partition(nums: List[int],pivot_index: int) -> int :
    """
    Here we modififed the code slightly to:
    Fix pivot value at index zero.
    Partition by the pivot value.
    Finally place the pivot  at the end of the left partition.
    This implementation puts pivot in the sorted position as well after partitioning.
    """
    n = len(nums)
    if pivot_index >= len(nums) : 
        raise ValueError("Pivot Index is out  of bounds!")
    
    print(f"Input List : {nums}")

    #Always keep pivot at index zero
    nums[0],nums[pivot_index] =  nums[pivot_index],nums[0]
    pivot_val = nums[0]

    left,right = 0 ,len(nums) -1

    while left < right :

        while left<= n-1 and nums[left] <= pivot_val :
            left+=1
        
        while right >=  0  and nums[right] > pivot_val :
            right-=1

        if left < right :
            #swap
            nums[left],nums[right] = nums[right],nums[left]

    #Put pivot Value in sorted  position
    nums[0] , nums[right] =  nums[right] ,nums[0]
    print(f"Pivot Value: {pivot_val}  ,Partitioned list : {nums}, Partition Index = {right}")
    return right

#nums = [2,4,5,1,8,9]
#nums = [2,4,5,1,4,8,9]
#nums= [3,2,1]
nums= [1,2,3]
partition(nums, 0)

        



