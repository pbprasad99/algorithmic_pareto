# Merge Sort

## Sorting an array

Merge Sort is just a binary recursive application of 2-way merge where the left and right recursive calls sort the left and right subarrays and we merge the two halves in the post order position.  

Thats it.

The actual sorting is a result of the merge function applied in a bottom up fashion from smallest subarray lengths.The actual sorting is a result of the merge function applied in a bottom up fashion from smallest subarray lengths.


As for the implementation details :

Instead of passing arrays to the merge method, pass pointers. Three pointers are sufficient : lo , mid and hi.
The subarrays to be merged are always adjacent: arr[lo...mid] and arr[mid+1...hi]

Base case is hit when lo = hi . A subarray of size one cannot be divided an further and is sorted by definition.

Merging cannot be done in place. So merge sort does require extra space. Instead of allocating extra temp space in each recursive call, just allocate extra space as external variable, equal to length of array. This temp space can be used to perform 2-way merge using the lo, mid and hi pointers passed to merge method. 


```python
"""
Merge Sort Solution for https://leetcode.com/problems/sort-an-array/description/
"""
class Solution:
    def merge(self, lo,mid,hi) :
        """
        Merge self.nums[lo:mid+1] and self.nums[mid+1,hi+1] into self.temp[lo:hi+1] 
        Write back self.temp[lo:hi+1] into self.nums[lo:hi+1]
        """
        print("merge " ,lo,mid,hi)
        for i in range(lo,hi+1) :
            self.temp[i] = self.nums[i]
        
        p1 = lo 
        p2 = mid+1
        p3 = lo 

        while p1 <= mid and p2 <= hi :
            if self.temp[p1] < self.temp[p2] :
                self.nums[p3] =  self.temp[p1]
                p1+=1
            else : 
                self.nums[p3] =  self.temp[p2]
                p2+=1
            p3+=1
        while p1 <= mid :
            self.nums[p3] = self.temp[p1]
            p1+=1
            p3+=1
    
        while p2 <= hi :
            self.nums[p3] = self.temp[p2]
            p2+=1
            p3+=1
        
    def sort(self, lo,hi) :
        """
        DRY RUN UNTIL FIRST BASE CASE IS HIT :

         0           2            5  
        [5,    1,    1,  2,  0  ,0]
        lo           m           hi
        lo     m     hi
        lomhi 
        ^BASE CASE HIT  
        """
        if lo >=  hi  :
            return
        # print(self.nums, self.temp)
        mid = (lo+hi)//2
        self.sort(lo,mid)
        self.sort(mid+1,hi)
        self.merge(lo,mid,hi)

    def sortArray(self, nums: List[int]) -> List[int]:
        #For writing intermediate merge results 
        self.temp = [0]*len(nums)
        #For accessing array which needs to be sorted
        self.nums = nums
        self.sort(0,len(nums)-1)
        return self.nums
```

## Sorting a linked list

Sorting a linked list is easier. We can actually break up the linked list in two halves in each recursive call. Sort the two halves and finally merge them. The base case is when the linked list is empty or only has a single element.

Pay attention to the difference in the recursive implementation for array and linked list.

For arrays, we pass pointers to the merge function to denote subarrays to be merged. For linked lists, we actually split the list and pass two separate lists.

```
"""
Solution for : https://leetcode.com/problems/sort-list/description/
Recursively  :
  Split the list in two halves .
  Sort first half
  Sort second half
  Merge the two SORTED halves.
"""
# Definition for singly-linked list.
 class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next

from typing import Optional

class Solution:
    def split_list(self, head: Optional[ListNode]) -> (Optional[ListNode],Optional[ListNode]) :
        """
        Splitting the list into two :
        dummy->1-> 2 ->3->None
            sf
               s   f
                   s      f  
        s.next -> second half  # s.next = None
        dummy.next --> first half
        """
        dummy = ListNode(0)
        dummy.next = head
        s,f = dummy,dummy 
        while f and f.next :
            f = f.next.next
            s = s.next
        #slow pointer stops at the PREVIOUS NODE of second half
        second_half = s.next
        s.next = None
        first_half = dummy.next
        # print("first half" , first_half)
        # print("second half", second_half)
        return first_half,second_half

    def merge(self,list1 : Optional[ListNode] , list2 : Optional[ListNode]) -> Optional[ListNode] : 
        p1, p2  = list1,list2
        # print("merging", p1, " and ", p2)
        dummy = ListNode(0)
        p3 = dummy

        while p1 and p2 :
            if p1.val < p2.val:
                p3.next = p1
                p1 = p1.next
            else: 
                p3.next = p2
                p2 = p2.next
            p3 = p3.next

        if p1 :
            p3.next = p1
        if p2 :
            p3.next = p2
        # print("merged" , dummy.next)
        return dummy.next 

    def _sort(self,head) :
        if not head or not head.next :
            return head
        #We first SPLIT the list halves
        first_half, second_half = self.split_list(head)
        #Then we SORT both halves
        #Sorting is not in place
        #So, you have to pass the sorted lists to merge
        sorted_first_half = self._sort(first_half)
        sorted_second_half = self._sort(second_half)
        #Merge the sorted halves
        return self.merge(sorted_first_half,sorted_second_half)


    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return self._sort(head)
```