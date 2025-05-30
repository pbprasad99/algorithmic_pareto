# Hoare Partition

## Defining the problem
Let us consider the simplest version of the problem.

Given an array of integers, rearrange the elements such that the left part contains elements less than or equal to a pivot value and the right part contains values greater than the pivot value.


## Hoare partition with strict condition

Consider this example array and a pivot value of 4   :

[ 1 , 9, 3, 5, 7, 4, 8  ]

If this array were already partitioned s.t. the left partition has only elements less than or equal to the pivot.
These would hold true :
```
Any element in left partition <= pivot
Any element in right partition > pivot
```
If we take left and right pointers  while verifying that arr[left] <= pivot and arr[right] > pivot, left and right pointers would move past each other before evaluating to False for the first time. Left pointer would end up at the BEGINNING of the right partition and the right pointer would end up at the END of the left partition.

```
[ 1,   3,     4,   5,   7,   8,   9 ]
  L/T  L/T   L/T *L/F*                            # L = Left pointer, T = arr[left]<= pivot is True , F = Its False
            *R/F* R/T   R/T     R/T    R/T        # R = right pointer, T = arr[right] > pivot is True, F = Its False   
```
  
If left evaluates to True while its less than right, it would mean that this element is in the wrong partition. This also implies that there must be an element in the right partition which belongs to the left partition. 

``` 
[  1 ,   9,   3,   5,   7,   4,   8  ]         
  L/T **L/F**                                    # L = Left pointer, T = arr[left]<= pivot is True, F = Its False
                          **R/F**   R/T          # R = right pointer, T = arr[right] > pivot is True, F = Its False                
```

We can simply swap these and keep moving until left and right pass each other.

**So, the algorithm would be:**

```
Invariant 1) [0,right] only contains elements less than or equal to pivot
Invariant 2) (right, len(arr) -1] only contains elements greater than pivot


While left <= right :
      while left<=right and > (Invaraint 1) is True :
           left +=1
      while left<=right and (Invariant 2) is True :
           right -=1
      if left < right :
          swap left and right
return right
```



##  Hoare partition with weak condition
The problem with the partition scheme with a strict condition (where we always put pivot values  in one of the partitions) is that it produces unbalanced partitions when used in quickselect or quicksort.

Consider if the above partition scheme were used in quickselect for finding the smallest element in an array of size n). 

What happens when all elements are duplicates :

```
    [1,1,1,1,1,1]
     l         r   Iter 1 : 5  comparisons
     l       r     Iter 2 : 4  comparisons
     l     r       Iter 3 : 3  comparisons
     l   r         Iter 4 : 2  comparisons
     l r           Iter 5 : 1  comparisons
     lr            Iter 6 : 0  comparisons
```
Number of comparisons = SUM([1.....n]) = n(n+1)/2 = (n*2 + n ) /2
Therefore, Complexity is O(n^2)  in this case.

To mitigate this, we could slightly modify the definition of our partitions :

```
Any element in left partition <= pivot
Any element in right partition >= pivot
```

Invariant 1) [low,right] only contains elements less than OR EQUAL to pivot
Invariant 2) (right, high] only contains elements greater OR EQUAL to pivot

That is, pivot values are allowed to be in either partition.

Our problem now becomes : 

Given an array of integers, rearrange the elements such that the left part contains elements less than or equal to a pivot value and the right part contains values greater than or equal to the pivot value.

The implementation is tricky when handling values equal to pivot. 

We also stop scanning when left or right are equal to pivot in both partitions. 
We swap and move the left and right pointers.
After any swap, both partitions will increase by 1. Pivot values might end up in any partition. 
This will also be the case when, left and right are both pointing to pivot value i.e. both partitions increase by 1 and there is a redundant swap between two pivot values.

```
While left <= right :
      while  left<=right and left < pivot :
           left +=1
      while left<=right and right > pivot:
           right -=1
      if left <= right :
          swap left and right
          left-=1
          right-=1
return right
```

Let us see the behavior of quickselect with this scheme for the same case :

```            
    [1,1,1,1,1,1]
     l         r   Iter 1 : 5  comparisons
     l   r         Iter 2 : 3  comparisons; This iteration returns r=0 and ends the loop
     rl            Iter 2 END 
```

The complexity is reduced to nLOG(n) now.

## Important things to Note:

***This algorithm does not necessarily place the pivot in its sorted position.***
Or rather, the problem is not asking us to do this,

This array is partitioned by 4 but 4 is not in its sorted position.

```
[ 1,   4,    3,  |5,   7,   8,   9 ]
```

We can put the pivot in its sorted position by swapping it with the right pointer after running the algorithm.  A good way to handle this is :
1) Ensure that  the pivot at the lowest index  .
2) Run the partitioning algorithm on the rest of the array.
3) Swap right with low.

But again, this will not group multiple instances of pivot together if pivot is duplicated. That is another problem called three way partitioning.

**This algorithm is not stable. The relative order of elements will not be preserved.**
Naive partitioning using extra space is the only algorithm which preserves relative order of elements.

Additional References :
https://algs4.cs.princeton.edu/23quicksort/