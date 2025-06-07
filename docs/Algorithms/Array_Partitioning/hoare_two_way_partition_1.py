
from typing import List

#Given a list return partition index after partition on the pivot index value
def partition(nums: List[int],lo,hi) -> int :
    """
    Hoare partition with strong condition.
    Picks the first element as the pivot value.
    There is no guarantee that pivot will be in its right place in this implementation.
    All we get is that the first half has elements less than or equal to pivot.
    Pivot can be any value in the array. (Pivot Value can actually be any arbitrary value in this version).
    """
    pivot = nums[lo]
    left,right = lo+1 ,hi

    while left <= right :
        while left<= right and nums[left] <=  pivot :
            left+=1
        while left <=right and nums[right] > pivot :
            right-=1
        if left < right :
            nums[left],nums[right] = nums[right],nums[left]
    
    print(f"Pivot Value: {pivot} , Partitioned list : {nums}, Partition Index = {right}")
    return right

if __name__ == "__main__" :
    nums = [2,4,5,1,4,8,9]
    partition(nums, 0, len(nums)-1)
    nums = [2,2,2,2,2,2]
    partition(nums, 0, len(nums)-1)
        



