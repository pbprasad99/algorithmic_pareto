---
title: Properties Of Comparison Based Sorting Algorithms
---

# Quicksort  
Not Stable, Not adaptive. In-Place. O(NlogN) Average Case. 

Pivot Selection and partitioning schemes affect Complexity in a major way. 

Pivot Selection : Fixed at hi or lo (worst), random (Good enough in practicw), Median of three, etc. 

Partitoning  :  Two way partitioning ( Eg. Hoare Partitioning with weak condition) , Three way partitioning (Eg : Djikstra) , Dual Pivot partitioning.  

Quicksort is a highly reaearched algorithm and there are many variations and derivatives. It is more like a family of algorithms. 

Can degrade to O(n^2) in cases for duplicate keys and sorted inputs, depending on pivot selection and partitioning scheme.

Important thing to note, The most common partitioning scheme found on the internet (Lomuto parition) performs more swaps than Hoare partition with a weak condition. Also, it degrades to O(n^2) when all elements are the same ( Hoare partition with a strict condition will also degrade to O(n^2) for duplicate keys).   

Lomuto was popularized by Bentley in the book Programming Pearls because he found Hoare difficult and unintuitve. One advantage to note: because Lomuto uses two forward iterators, it can be used on singly linked lists.


# Mergesort
Quadratic. In-place. Stable. Not adaptive. Not In-place (Needs extra space)
Can be combined with Insertion sort for small subproblem sizes.


# Bubble Sort  
Stable. Can be made adaptive (just add a flag to tell if a swap has occurred. If not exit early). 

Invariant for inner loop

[ | ]
  j
```
def optimized_bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False  # Flag for no swaps in a pass
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True  # Swap occurred
        if not swapped:
            return  # Already sorted, no more passes needed
    return arr
```

# Insertion Sort

Quadratic. In-place. Stable. Adaptive.

```
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
```

This is quite similar to optimized bubble sort except that in bubble sort,the sort element (maximimum) is bubbled into unsorted section while in insertion sort, the sort element (minimum) is bubbled into the sorted section. 

Insertion sort is ONLINE. Each new element can be put in its sorted place as it is received.

Shell Sort is a faster variation of Insertion sort (named after D.L. Shell who invented it). It uses insertion sort on periodic subarrays.

Alse see : 
https://stackoverflow.com/questions/47712062/how-to-distinguish-online-and-offline-sorting-algorithms

https://cs.stackexchange.com/questions/55012/what-is-the-fastest-online-sorting-algorithm

# Selection Sort
Quadratic. In-Place. Not Stable. Not Adaptive. 

Only advantage over insertion sort : performs less swaps than insertion sort.


# Additional References 

https://www.toptal.com/developers/sorting-algorithms