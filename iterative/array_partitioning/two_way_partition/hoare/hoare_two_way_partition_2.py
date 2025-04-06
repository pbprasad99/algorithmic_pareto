
from typing import List

#Given a list return partition index after partition on the pivot index value
def partition(nums: List[int],pivot_index) -> int :
    """
    Here we modififed the code slightly to :
    Fix pivot value at index zero.
    Partition by the pivot value on the rest of the array.
    Finally put the pivot value at the end of the left half of the array.
    Therefore, this implementation puts pivot in the sorted position as well after partitioning.
    """
    print(f"Input List : {nums}")
    n = len(nums)
    
    #We can ignore this for the purpose of understanding the algorithm.
    #Pivot index Boundary check should be here
    #Edge cases for lists of length 2 or less. 
    # if n < 1  :
    #     return None
    # if n < 2 :
    #     return 0 
    # if n == 2 :
    #    if nums[1] > nums[0] : 
    #        nums[0], nums[1] = nums[1],nums[0]
    #        return 1
    #    return 0 
          
    
    #Always keep pivot at index zero
    nums[0],nums[pivot_index] =  nums[pivot_index],nums[0]
    pivot_val = nums[0]

    left,right = 1 ,len(nums) -1

    while left < right :

        while left< n-1 and nums[left] <= pivot_val :
            left+=1
        
        while right >  0  and nums[right] > pivot_val :
            right-=1
        if left < right :
            #swap
            nums[left],nums[right] = nums[right],nums[left]

    #Put pivot Value in its right place
    nums[0] , nums[right] =  nums[right] ,nums[0]
    print(f"Pivot Value: {pivot_val}  ,Partitioned list : {nums}, Partition Index = {right}")
    return right

#nums = [2,4,5,1,8,9]
nums = [2,4,5,1,4,8,9]
partition(nums, 4)

        



