# Median of two sorted arrays

This is one of those problems which I like to call an "Algorithm in itself". Although categorized under Binary Search, its not just a straightforward application of it.

!!! info "Description"
    
    [Leetcode Link](https://leetcode.com/problems/median-of-two-sorted-arrays/description/){target="_blank"}      
    
    ```
    Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
    
    The overall run time complexity should be O(log (m+n)).
    
     
    
    Example 1:
    
    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.00000
    Explanation: merged array = [1,2,3] and median is 2.
    Example 2:
    
    Input: nums1 = [1,2], nums2 = [3,4]
    Output: 2.50000
    Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
     
    
    Constraints:
    
    nums1.length == m
    nums2.length == n
    0 <= m <= 1000
    0 <= n <= 1000
    1 <= m + n <= 2000
    -106 <= nums1[i], nums2[i] <= 106
    ```

Let us figure out how binary search can be applied to solve this problem..

## What is the data?

nums1 = [1,2], nums2 = [3,4]

Two sorted arrays.

## What is being asked?

To find the median in logarithmic time.

## Thoughts

**What is a median**

Consider :
```
[1 2 |3 4]  #right partition is inclusive 
``` 
If we partition an even lengthed sorted array such that the left and right partitions are of equal size.

The median is ( max(left partition) + min(right partition)  ) / 2

If the array is odd lengthed :
```
[1 2 3 4 5]
     *
```
We can consider the middle element to belong to both partitions. In which case
```
[1 2 3 4 5]
     *
```  

The middle element IS the median i.e. index len(arr)//2


Provided A and B are both sorted, We can always find partitions on A and B such that elements to the left of both partitions are less than elements to their right and both partitions combined divide the combined arrays in half. It will be clear what is meant from the examples below (Consider left out of bounds position to be -inf and right out of bounds position to be +inf). 

!!! example "Example 1 : Valid Partitions"
    ```
    Example 1: 
    B [ 1, 2, |6, 7]  # right pertition is inclusive
    A  [  5, |10  ]
    
    1,2,5  < 6,7,10
    ```
!!! example "Example 2 : Valid Partitions"
    ```
    Example 2 :
    B [ |5, 6, 7, 8, 9 ] # consider left out of bounds position to be -inf and right out of bounds position to be +inf
    
    A [ 1, 2, 3, 4| ]
    
    1,2,3,4 < 5,6,7,8,9
    ```

Note that if you pick a partition on array A, there is only one corresponding partition on array B because we are looking for the set of partitions which divide the combined arrays in two halves.

We can tell a set of partitions COULD BE a valid by verifying that the last element of the left partition of one array is less than or equal to the first element of the other arrays right partition. We can check the inverse to confirm that the partitions are in fact not valid. 

We can in fact use binary search to find the correct partitions. All we need is to know which way should we move one of the partitions. We will go into this in more detail. 

The idea is if we find the correct partitions, we can calculate the median by looking at the elements clustered around both partitions. Let's see how..

**The first question is how should we define the partitions?**

partition_a + partition_b = (m+n+1) //2 OR partition_a + partition_b = (m+n) // 2 

let len(A) =m and len(B) = n 

FOR ODD LENGTHED ARRAY :

```
B  [1]   ; #IFF partition_b = (m+n +1 )//2 - partition_a  = 2//2 -0 = 1 But *IFF partition_b =  (m+n)//2 - partition_a =  1//2 -0 = 0-0 = 0 
   *0 #1  
A  [ ]   ; partition_a = (0+ 0)//2 =0 
    0
```

*If we say that **partition_x + partition_y = (m+n)//2 then median is in the right partition** in case of odd lengthed array.*

*If we say that **partition_x + partition_y = (m+n+1)//2 then median is in the left partition** in case of odd lenghted array.*

***It makes no difference for arrays where m+n is even.***
```
B [1 2]   ; #IFF partition_b = (m+n+1)//2 - partition_a  = 5//2 - 1 = 2- 1 = 1 and *IFF partition_b = (m+n)//2 - partition_a = 4//2 -1 = 1
    #*1
A [1 2]   ; partition_a = (0 + 2) // 2 = 1
```

Lets pick one convention : 

partition_a + partition_b = (m+n) //2

**Now for the binary search:**

It makes sense to binary search on the smaller array. Lets call this array A and the partition on it,  partition_a.

!!! info "Binary Search Logic" 
    In each iteration of the binary search, we consider mid as partition_a.
    For each partition_a we determine partition_b (as per our definition) and ask ***is left_b > partition_a*** where left_b is the last element in the left partition of array B. 
    
    - If this is TRUE, then partition_a cannot be the pivot. Now the question is where do we move partition_a: to the left or to the right?
    We know that left_b is too big right now, so it needs to be made SMALLER i.e. Moved left. For doing this, by definition of our partitions, we NEED TO MOVE partition_a to the right i.e. partition_a need to be made larger. This is like increasing our lower bound.
    - If this is FALSE, it means that the current set of partitions COULD BE VALID. Therefore, we set hi = mid. That is, decrease our upper bound.

!!! info "Dry Run"   
    ```
    INIT:         
    B [ 1  3  4  5   6  ]
    A  [ 2  6  7   8   ] 
         lo          hi
    
    ITER 1:
    A [1  3  4  5  6  ]
             *            #left_b is 3.
    B  [ 2 6  7  8 ]  
         lo   *            #3 > 7 is F; this could be the right partition_a ; hi = mid
             F/hi
    
    ITER 2 :
    A [1  3  4  5  6  ]
                *
    B  [ 2  6 7  8 ]
       lo   *           #4> 6 is F  ; this could be partition_a hi = mid            
           F/hi
    
    ITER 3 :
    A [1  3  4  5  6  ]
                   *
    B  [ 2    6  7  8 ]
         *              #5>2 T; This cannot be the right partition_a ;
         T/lo hi        #lo = mid+1  ; Now lo == hi; lo and hi have converged and  loop exits in next iteration
    
    ITER 5 :
    B [2   6   7   8]  # lo = hi = 1 and while loop exits
           *
           F/lo,hi
    
    ```
!!! tip "tl;dr" 
    Binary search will converge on the first false value.
    ```
       [1    3    4     |5    6  ]
         [2     |6    7    8]
          T     F    F    F
    ```

In our binary search we need a function move_right which simply returns left_b > right_a

**Thats it. Once , we have the right partition, calculate median:**

- If (m+n) is odd : return min(right_a, right_b)

- If (m+n) is even : return (max(left_a, left_b) + min(right_a, right_b)) /2 

## Code

???+ code
     ```python
     
     class Solution:
         def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
             # A is always the smaller array
             A, B = nums1, nums2 
             if len(A) > len(B) :
                 A , B = B, A
     
             #measure their lengths    
             m,n = len(A), len(B)
     
             def find_partition_b(partition_a) : 
                 return (m+n)//2 - partition_a
     
             def get_left(partition,array) :
                 return float('-inf') if (partition-1 )<0 else array[partition-1]
             
             def get_right(partition,array) :
                 return float('inf') if (partition)>= len(array) else array[partition]
             
             def move_right(partition_a) : 
                 partition_b = find_partition_b(partition_a)
                 left_b = get_left(partition_b,B)
                 right_a = get_right(partition_a,A)
                 return left_b > right_a
             
             #binary search to find the correct partition_a
             lo, hi  = 0 , len(A)
             while lo < hi :
                 partition_a = (lo +hi) // 2
                 if move_right(partition_a) :
                     lo = partition_a+1
                 else :
                     hi = partition_a
             
             #lo and hi have converged on the correct partition_a 
             partition_a,partition_b   = lo, find_partition_b(lo)
             right_a = get_right(partition_a,A)
             right_b = get_right(partition_b,B)
     
             #combined array length is odd
             if (m+n) % 2 == 1 :
                 return min(right_a,right_b)
     
             #combined array length is even    
             left_a = get_left(partition_a,A)
             left_b = get_left(partition_b,B)
             return ( max(left_a,left_b) + min(right_a,right_b) ) / 2        
     ```