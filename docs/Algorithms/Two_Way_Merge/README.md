# Merging Sorted Containers

Before considering K-way merge, let us first look at the simpler version of the problem.

## The 2-Way merge problem.

### Merging two sorted arrays

Given 2 integer arrays, sorted in non decreasing order, merge them into a single sorted array. 

??? code 
    === "Two Way Merge on Arrays"
        ```python
        --8<--
        docs/Algorithms/Two_Way_Merge/two_way_merge.py
        --8<--
        ```
    === "Unit Tests for Two Merge on Arrays"
        ```python
        --8<--
        docs/Algorithms/Two_Way_Merge/test_two_way_merge.py
        --8<--
        ```

### Merging two sorted lists

The same thing for a linked list :

??? code 
    === "Two Way Merge on Lists"
        ```python
        --8<--
        docs/Algorithms/Two_Way_Merge/two_way_merge_list.py
        --8<-
        ```

So, how are we solving the problem of two way merging?

We have a write pointer p3 and we have two read pointers, p1 and p2.
In each iteration of the while loop, we pick the smaller read pointer to write to the write location and move both pointers (write pointer and one of the read pointers) ahead.

If either p1 or p2 have still not reached the end of their read containers, we just write the rest of that read container at the write pointer.

## Practice 

??? example "[Merge sorted arrays backwards](https://leetcode.com/problems/merge-sorted-array/){target="_blank"}"
    ```python
    --8<--
    docs/Algorithms/Two_Way_Merge/88_merge_sorted_arrays.py
    --8<-
    ```

??? example "[Merge Strings Alternately](https://leetcode.com/problems/merge-sorted-array/){target="_blank"}"
    ```python
    --8<--
    docs/Algorithms/Two_Way_Merge/1768_merge_strings_alternately.py
    --8<-
    ```

    
    