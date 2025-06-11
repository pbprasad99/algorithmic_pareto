# In-Place Deduplication

## In-Place deduplication of Sorted Array

### Defining the Problem

The task is to partition a sorted array s.t the left partition contains only unique elements. The relative order of elements must be maintained. The function should return the length of the left partition.
([Leetcode Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/){target="_blank"})

??? example
    ```markdown
    Example 1:
    
    Input: nums = [1,1,2]
    Output: 2, nums = [1,2,_]
    Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
    It does not matter what you leave beyond the returned k (hence they are underscores).
    Example 2:
    
    Input: nums = [0,0,1,1,1,2,2,3,3,4]
    Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
    Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
    It does not matter what you leave beyond the returned k (hence they are underscores).
    ```
    
### Algorithm

!!! tip "Key Ideas"
    - [0,s] - Is the inclusive interval containing only non-duplicate elements
    - (s,f) - Is the exclusive interval containing duplicates from [0,s]
    
    Initialize s=0 and f=0.

    s+1 is the write position for the next unique element. f scouts ahead for the next unique element.
    
    The key insight is to compare f with s. Since the array is sorted, all elements between s and f that equal arr[s] are duplicates. 

    - s stays at the inclusive right boundary of the interval with no duplicates.
    
    - To maintain this invariant, f moves forward to find the next unique element which should be placed at s+1. 
    
    - This means if s and f are equal, we move only f ahead to find the next unique element.
    
    - Once a swap is made the interval with duplicates increases by 1 so s is incremented and Invariant 1 is maintained.
    
    Notice that f is incremented in both cases. But s is only incremented if a swap is made.
    
**Algorithm Steps:**

1. Initialize s=0, f=0 (both pointing to first element)
2. For each position f:
    
     - If nums[f] ≠ nums[s]:

        - Write nums[f] to position s+1
        - Increment s

3. Return s+1 as the length of valid partition


**Initially,**

- s,f = 0,0
- [0,0] - Has only 1 element. First Invariant is trivially True.
- (0,0) - Empty set. Second Invariant is trivially True.

**Maintenance**

In the loop we will maintain the invariants. Here is the dry run:
 

!!! info "DRY RUN"
    ```
        [ 1  1  1  2  2  3  4  5]
          sf                      # s and f are equal, only f moves forward  
          s  f                    # ----"----
          s     f                 # ----"----
          s        f              # ----"----
        [ 1  2  1  1  2  3  4  5] # s and f are not equal ; f is at next unique element; Swap s+1 with f and move both pointers forward
             s        f           # s and f are equal, only f moves forward
             s           f        # s and f are not equal ;f is at next unique element; Swap s+1 with f and move both pointers forward
        [ 1  3  1  1  2  2  4  5]
                s           f     # s and f are not equal ;f is at next unique element; Swap s+1 with f and move both pointers forward
        [ 1  3  4  1  2  2  1  5]
                   s           f  # s and f are not equal ;f is at next unique element; Swap s+1 with f and move both pointers forward 
        [ 1  3  4  5  2  2  1  1]
                      s           f  # Final state after loop ends     
        
        Notice that (s,f) always contains duplicates of elements from [0,s]
    ```

!!! code 
    ```python
    class Solution:
        def removeDuplicates(self, nums: List[int]) -> int:
            s =0
            for f in range(len(nums)) :
                if nums[s] != nums[f] :
                    nums[s+1] , nums[f] = nums[f],nums[s+1]
                    s+=1
            #[0,s] is the interval with no duplicates
            k = s+1 # k is the number of elements in the first interval
            return k 
    ```
### Complexity
- `O(n) time complexity`
- `O(1) Space Complexity`

## In-Place deduplication with Unique Elements appearing at most Twice

### Defining the Problem
Partition a sorted array s.t. the left partition contains at most two duplicates for each value. The relative order should be maintained. 

More formally, if there are k elements after removing the duplicates, then the first k elements of nums should hold the final result. It does not matter what you leave beyond the first k elements.


This is similar to the first problem with a relaxed constraint that allows one duplicate in the left partition.([Leetcode Link](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/){target="_blank"})

??? example

    ```
    Example 1:
    
    Input: nums = [1,1,1,2,2,3]
    Output: 5, nums = [1,1,2,2,3,_]
    Explanation: Your function should return k = 5, with the first five elements of nums being 1, 1, 2, 2 and 3 respectively.
    It does not matter what you leave beyond the returned k (hence they are underscores).
    Example 2:
    
    Input: nums = [0,0,1,1,1,1,2,3,3]
    Output: 7, nums = [0,0,1,1,2,3,3,_,_]
    Explanation: Your function should return k = 7, with the first seven elements of nums being 0, 0, 1, 1, 2, 3 and 3 respectively.
    It does not matter what you leave beyond the returned k (hence they are underscores).
    ```

### Algorithm
This problem is all about defining the invariant correctly. Let's dig into the solution.

!!! tip "Key Ideas"
    - [0,s] - Is the inclusive interval containing no more than two duplicate
    - (s,f) - Is the exclusive interval containing duplicates from [0,s]
    
    Initialize s=1 and f=2.

    s+1 is the write position for the next valid element. f scouts for the next valid element which can be placed at s+1.
    
    The key insight is to look two positions back to identify when we've seen more than two of the same element. Since the array is sorted, we can identify duplicates by comparing with the element at position s-1. We know that if arr[f] == arr[s-1] -> arr[f] == arr[s] as well.

    If it's same as s-1, we've seen this element more than twice, therefore only f moves forward and s stays where it is.

    If it is different, then it is the next element which belongs at position s+1. Swap s+1 with f and move both s and f forward.



**Algorithm Steps:**

1. Handle edge case of array with length ≤ 1
2. Initialize s=1, accepting first two elements by default
3. For each position f starting from 2:
   - If nums[f] ≠ nums[s-1]:
     - Write nums[f] to position s+1
     - Increment s
4. Return s+1 as the length of valid partition

!!! warning
     #s,f= 1,1 # Cannot Initialize like this. f has to be s+1 initially for swapping to work correctly. If f=s, you will end up putting s ahead of f initially if f !=s-1, since we are swapping s+1 with f. Besides if (s,f) is an exclusive interval, f should be initialized to s+1.

**Initially,**

   - s,f = 1,2
   - [0,1] - Has only two elements. First Invariant is Trivially True.
   - (1,2) - Empty set. Second Invariant is Trivially True.

**Maintenance**

In the loop we will maintain the invariants. Here is the dry run: 

!!! info "DRY RUN"
    ```
    [1,1,1,2,2,3] # everything before s including s is good
       s f        # (s,f) empty,  f = s-1 . Only f moves ahead, After f moves ahead : (s,f) will contain the excess 1. 1 is a duplicate wrt to elements in [0,1]. This works because array is sorted. We know that if arr[f] == arr[s-1] -> arr[f] == arr[s] as well..
       s   f      # If we move f ahead now, it will contain 2 which is not a duplicate,swap s+1 with f and move both ahead to maintain both invariants 
    [1,1,2,1,2,3] # swapped s+1 with f and s+=1, f+=1
         s   f    # f!=s-1 : swap s+1 with f
    [1,1,2,2,1,3] #swapped s+1 with f and s+=1,f+=1
           s   f  # f!=s-1  : swap f with s+1 
    [1,1,2,2,3,1] #swapped s+1 with f and s+=1,f+=1
             s   f
    ```

!!! code 
    ```python
    class Solution:
        def removeDuplicates(self, nums: List[int]) -> int:
            #Edge case - nums has only one element
            if len(nums) == 1 :
                return 1
            
            #Initialization: s=1 and f=2
            s=1
            for f  in range(2,len(nums)) :
                #Maintenance
                if nums[f] != nums[s-1] :
                    nums[s+1],nums[f] = nums[f],nums[s+1]
                    s+=1
            return s+1
    ```
### Complexity
- `O(n) time complexity`
- `O(1) Space Complexity`

## Comparison with Lomuto's Partition

The deduplication algorithm looks awfully similar to [Lomuto](Lomuto.md){target="_blank"}, but there are subtle and crucial differences.While both algorithms use two-pointer techniques, their invariants reveal fascinating differences in how they handle elements:

### Interval Types and Their Significance

A key distinction lies in how these algorithms define their intervals:

**Lomuto's Partition**: Uses half-open intervals

  - `[lo,s)` ≤ pivot: Excludes s
  - `[s,f)` > pivot: Excludes f
  - This makes sense because s acts as a boundary between two partitions
  - Next valid element (≤ pivot) is written at position s

**Deduplication**: Uses closed interval for primary invariant

  - `[0,s]`: Includes s
  - This is necessary because s marks the last valid unique element
  - The next unique element will be placed at s+1

Deduplication needs s to be part of the valid region since it represents the last confirmed unique element

### Deduplication as a Lomuto Variant

The deduplication algorithm can be viewed as a specialized variant of Lomuto's partition where:

1. **Pivot Selection**: Instead of a fixed pivot, we use a "moving pivot" (nums[s]) that changes as we progress

2. **Partition Criteria**: Rather than comparing with a fixed value:

     - Lomuto: Elements ≤ pivot go left
     - Deduplication: Elements ≠ current value go to next position

3. **Pointer Movement**: 

     - Both use s as a boundary of the "accepted" elements
     - Both increment f to scan through remaining elements
     - Both swap when their condition is met

The key insight is that deduplication adapts Lomuto's two-pointer partitioning strategy but:

- Uses equality comparison instead of less-than
- Updates its "pivot" value after each partition
- Requires input to be sorted 

This connection explains why both algorithms share similar pointer movement patterns despite serving different purposes.
