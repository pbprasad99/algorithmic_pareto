
from typing import List

#Given a list return partition index after partition on the pivot index value
def partition(nums: List[int],pivot_index) -> int :
    """
    There is no guarantee that pivot will be in its right place in this implementation.
    All we get is that the first half has elements less than or equal to pivot.
    Pivot can be any value in the array. (Pivot Value can actually be any arbitrary value in this version).
    """
    n = len(nums) 
    pivot_val =  nums[pivot_index]
    #Pivot Value can actually be any arbitrary value in this version
    #pivot_val = 100
    left,right = 0 ,len(nums) -1

    while left < right :
        while left< n-1 and nums[left] <= pivot_val :
            left+=1
        #Right will end up at -1 if pivot value is less than any value in array
        #if right > 0 is the boundary check , then the result won't be correct for this case.
        #Therefore raise an error in case right goes beyond 0. 
        #Because, negative index for list slicing will give a valid result and that again would be incorrect 
        while right >=  0  and nums[right] > pivot_val :
            right-=1
        if left < right :
            #print(left,right)
            nums[left],nums[right] = nums[right],nums[left]
    
    print(f"Pivot Value: {pivot_val} , Partitioned list : {nums}, Partition Index = {right}")

    # if right < 0  :
    #     raise ValueError("Pivot less than any value in array")

    return right
nums = [2,4,5,1,8,9]
nums = [2,4,5,1,4,8,9]
partition(nums, 4)

        



