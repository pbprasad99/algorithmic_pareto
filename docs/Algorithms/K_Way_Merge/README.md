#  The k-way Merge problem

## Merging k sorted arrays

We can think of the k-way merge problem as a generalization of the 2-way merge problem. That is given, k sorted containers, return a merged sorted container.

In the 2-way merge problem , we had a binary choice when picking the next value to write to the merged container. 
Now we have a k-way choice among k or less elements at each step. We basically need a good way to pick the smallest value from among all possible choices. This is what a heap does. Since we are considering containers sorted in a non decreasing order, a Min Heap is what we need to dynamically pick the smallest value at each step.

The crux of the algorithm is :
!!! info "Algorithm"
    ```
    initialize a Min heap of all possible choices. 
    While there is something in the heap : 
       Pop the heap top and write it to the merged container.
       Get the element next to popped element in the container to which it belongs (If it exists). Put it in the heap.
    ```

Thats it.

The code should actually simpler than handling the 2-way merge because there are no if else conditions to handle unequal lengthed arrays.
 
??? code
    === "K Way Merge on Arrays"
    ```python
    --8<--
    docs/Algorithms/K_Way_Merge/k_way_merge.py
    --8<--
    ```

## Merging k sorted linked lists

The same thing for linked lists. 

??? code
    === "K Way Merge on Arrays"
        ```python
        --8<--
        docs/Algorithms/K_Way_Merge/k_way_merge_list.py
        --8<--
        ```

## Practice

??? example "[Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/){target="_blank"}"
    ```
    """
    Solution for https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/
    
    This can be solved using k-way merge. Instead of putting the next smaller value in a resultant merged array, 
    simply put it in a max heap of size k.
    
    Example :
    [
    [1,5,9],
           *
    [10,11,13],
        *
    [12,13,15]
     *
    ]
    
    say , k = 4
    Can we use A Max heap to maintain the k largest numbers?
    [10,9,5,1]
    
    When size becomes greater than k pop from the max heap:
    
    >[11,10,9,5,1]
    >size is greater than 5 
    >pop from max heap
    [10,9,5,1]
    
    Memory required is : max heap of size k to  keep track of k smallest numbers
    A min heap of size len(matrix) (equal to the number of rows in matrix) to pick the next smallest number
    
    Algorithm :
    
    1) Initialize a min heap to pick next smallest number from all rows of matrix
    2) While min heap is not empty:
        -  Pop from min heap and put in a max heap of size k
        -  Put element next to popped element into min heap  
    3) Return the top of max heap.
    
    """
    from heapq import heapify, heappush , heappop
    class Solution:
        def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
            pq = []
            for row in matrix : 
                e = (row[0], 0, row)  # tuple of Curr_Value, curr_index, row reference
                pq.append(e)
            heapify(pq)
            
            max_hp = []
            while pq :
                #pick next smallest number
                val, idx, row = pq.pop()
                #Simulate max heap by negating values
                heappush(max_hp,-val)
                if len(max_hp) > k :
                    heappop(max_hp)
                if idx < len(row) -1 :
                    heappush(pq,(row[idx+1],idx+1,row))
            # Retun top of max heap
            return -heappop(max_hp) 
    ```
    