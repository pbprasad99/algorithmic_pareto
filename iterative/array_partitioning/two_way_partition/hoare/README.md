# Defining the problem

Given an array of integers, rearrange the elements such that the left part contains elements less than or equal to a pivot value and the right part contains values greater than the pivot value.


# Deriving the algorithm

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
Invariant 1) [0,Left) only contains elements less than or equal to pivot
Invariant 2) (right, len(arr) -1] only contains elements greater than pivot
```

While left <= right :
      while  (Invaraint 1) is True :
           left +=1
      while (Invariant 2) is True :
           right -=1
      if left < right :
          swap left and right

# Important things to Note:

***This algorithm does not neceassrily place the pivot in its sorted position.***
Or rather, the problem is not asking us to do this,

This array is partitioned by 4 but 4 is not in its sorted position.

```
[ 1,   4,    3,  |5,   7,   8,   9 ]
```

We can put the pivot in its sorted position by swapping it with the right pointer after running the algorithm.  A good way to handle this is :
1) Place the pivot in the index 0 .
2) Run the partitioning algorithm on [1,n-1]
3) Swap right with 0.

But again, this will not group multiple instances of pivot together if pivot is duplicated. That is another problem called three way partitioning.

**This algorithm is not stable. The relative order of elements will not be preserved.**
Naive partitioning using extra space is the only algorithm which preserves relative order of elements.