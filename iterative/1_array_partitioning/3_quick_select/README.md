
# QuickSelect 

## Defining the problem.

Given an array, find the sorted value in non decreasing order at the kth smallest index when indices are counted from zero.


## The Algorithm

The core of the quickselect algorithm is the partitioning scheme. There are different ways of implementing quickselet based on whether the partitioning scheme puts the pivot in its sorted position or not. Here we will consider only the implementation which uses partition schemes which do, becuase this is simpler and more intuitive.

Assume, you have a partitioning scheme which returns some partition index / pivot index s.t. the value at the pivot index is in its sorted position. The quickeselect algorithm makes one recursive call based on the relative position of k to the pivot index. The base case is when the pivot index is k.

The algorithm is :

```

def quickselect(arr,lo,hi, k ) :
    p = partition(arr,lo,hi)
    if p == k :
       return arr[k]
    elif  k< p :
       return quickselect(arr,lo,p-1,k)
    else :
       return quickselect(arr,p+1,hi,k)

```


## Additional References :

https://en.wikipedia.org/wiki/Selection_algorithm

# QuickSort

## Defining the problem.
GIven an array, sort it in non decreasing order.

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