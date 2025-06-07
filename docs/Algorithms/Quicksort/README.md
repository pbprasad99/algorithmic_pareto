
# QuickSort

## Defining the problem.

Given an array, sort it in non decreasing order.

## The Algorithm

Once you understand partitioning, quickselect and quicksort are just recursive applications of it. In quickselect, we make a single recursive call, while in quicksort, we make two recursive calls to eventually put all elements in their sorted position. Quick Sort can be visualized as a preorder traversal of a binary tree, where in the preorder position, you call the partitioning function and recursively call quicksort on both partitions. The base case is when lo >= hi.


Assume, you have a partitioning scheme which returns some partition index / pivot index s.t. the value at the pivot index is in its sorted position.

The algorithm is :


```
def quicksort(arr,lo,hi, k ) :
    if lo >= hi  :
       return 
    p = partition(arr,lo,hi)
    quicksort(arr,lo,p-1,k)
    quicksort(arr,p+1,hi,k)
```

## Additional References :

https://algs4.cs.princeton.edu/23quicksort/