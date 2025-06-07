"""
Solution for  https://leetcode.com/problems/merge-two-sorted-lists/description/
"""
from typing import Optional
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        p1, p2  = list1,list2
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
        else :
            p3.next = p2

        return dummy.next 
        