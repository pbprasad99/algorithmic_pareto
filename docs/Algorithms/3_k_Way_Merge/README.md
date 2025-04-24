# Merging Sorted Containers

Before considering K-way merge, let us first look at the simpler version of the problem.

## The 2-Way merge problem.

### Merging two sorted arrays

Given 2 integer arrays, sorted in non decreasing order, merge them into a single sorted array. 


```python
--8<--
docs/Algorithms/3_k_Way_Merge/two_way_merge.py
--8<--
```

### Merging two sorted lists

The same thing for a linked list :

```python
--8<--
docs/Algorithms/3_k_Way_Merge/two_way_merge_list.py
--8<-
```


So, how are we solving the problem of two way merging?

We have a write pointer p3 and we have two read pointers, p1 and p2.
In each iteration of the while loop, we pick the smaller read pointer to write to the write location and move both pointers (write pointer and one of the read pointers) ahead.

If either p1 or p2 have still not reached the end of their read containers, we just write the rest of that read container at the write pointer.

## The k-way Merge problem

### Merging k sorted arrays

We can think of the k-way merge problem as a generalization of the 2-way merge problem. That is given, k sorted containers, return a merged sorted container.

In the 2-way merge problem , we had a binary choice when picking the next value to write to the merged container. 
Now we have a k-way choice among k or less elements at each step. We basically need a good way to pick the smallest value from among all posssible choices. This is what a heap does. Since we are considering containers sorted in a non decreasing order, a Min Heap is what we need to dynamically pick the smallest value at each step.

The crux of the algorithm is :

```
initialize a Min heap of all possible choices. 
While there is something in the heap : 
   Pop the heap top and write it to the merged container.
   Get the element next to popped element in the container to which it belongs (If it exists). Put it in the heap.
```

Thats it.

The code should actually simpler than handling the 2-way merge because there are no if else conditions to handle unequal lengthed arrays.
 

```python
--8<--
docs/Algorithms/3_k_Way_Merge/k_way_merge.py
--8<--
```

### Merging k sorted linked lists

The same thing for linked lists. 

```python
--8<--
docs/Algorithms/3_k_Way_Merge/k_way_merge_list.py
--8<--
```


## Important things to note

As we saw earlier, quicksort is just an application of array partitioning where we can think of a partition happening at the preorder position in the traversal of a binary tree. 

Similaraly, Merge sort is an application of 2-way merge where we can think of a merge happening in the post order position of a binary tree traversal.