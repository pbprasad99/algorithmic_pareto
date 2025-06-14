
"""
Solution for https://leetcode.com/problems/merge-sorted-array/

A slightly different variation of the two-way merge problem. 
The challenge here is to merge one array into another array 
backwards into extra space allocated at the end of one of the arrays.

To accomplish this at each step we pick the greatest among the the two choices and put it at the end of the target array.

p3  -> write pointer
p1, p2 -> read pointers
nums1 -> target array



p3 will never overwrite p1 because :

Initially p3 - p1 = n,
If p2 is decremented, the gap p3 - p1 reduces by 1, because p3 is incremented and p1 remains the same.
If p1 is decremented, the gap p3 - p1 remains the same 
0<= p3-p1 <= n # The gap can at most become zero.
When,
p3 -p1 = 0 <-> p2  = -1
Which means all of nums2 has been written into nums1, the while loop will not execute.
Therefore p3 will never overwrite p1.


Dry Run these to see how it works out :

nums1 :[2,3,0]
nums2 :[4]

nums1 :[2,3,0]
nums2 : [-1]
"""
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1,p2,p3 = m-1, n-1, len(nums1) -1 
        while p2 >= 0 :
            if p1 >=0 and nums1[p1] > nums2[p2] : 
                nums1[p3] = nums1[p1]
                p1-=1
                p3-=1
            else :
                nums1[p3] = nums2[p2]
                p2-=1
                p3-=1
        
        return nums1