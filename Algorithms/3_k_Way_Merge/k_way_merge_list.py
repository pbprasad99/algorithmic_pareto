from heapq import heapify,heappush,heappop
#Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        pq=[]
        for idx, head in enumerate(lists) : 
            if not head : continue
            #Put idx between the value and the node object  to avoid comparing objects in case of a tie 
            #Which will lead to this error :'<' not supported between instances of 'ListNode' and 'ListNode'
            heappush(pq,(head.val,idx, head)) 

        #Allocate Write container and write pointer
        dummy = ListNode(0)
        write_ptr = dummy

        while pq :
            #Pick the lowest valued node from available choices.
            _,idx,curr_node = heappop(pq)
            
            #write to write container and move write pointer ahead
            write_ptr.next = curr_node
            write_ptr = write_ptr.next

            #For curr_node, put its next node in the heap  
            nxt_node = curr_node.next 
            if nxt_node : heappush(pq,(nxt_node.val, idx, nxt_node ))
        return dummy.next