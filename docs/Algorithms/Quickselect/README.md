# QuickSelect 

### Defining the problem.

Given an array, find the sorted value in non decreasing order at the kth smallest index when indices are counted from zero.

### The Algorithm

The core of the quickselect algorithm is the partitioning scheme. There are different ways of implementing quickselet based on whether the partitioning scheme puts the pivot in its sorted position or not. Here we will consider only the implementation which uses partition schemes which do, because this is simpler and more intuitive.

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
