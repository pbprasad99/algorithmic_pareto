# Properties of Comparison-Based Sorting Algorithms

---

## Quicksort

- **Stability:** Not stable  
- **Adaptivity:** Not adaptive  
- **In-Place:** Yes  
- **Time Complexity:** O(N log N) average case  
- **Worst Case:** O(N²) (e.g., sorted input, duplicate keys, poor pivot selection)  

**Notes:**
- Pivot selection and partitioning schemes significantly affect complexity.

**Pivot Selection:**  

  - Fixed at high or low index (worst case)
  - Random (good enough in practice)
  - Median-of-three, etc.

**Partitioning:**  

  - Two-way (e.g., Hoare partitioning with weak condition)
  - Three-way (e.g., Dijkstra)
  - Dual-pivot partitioning

Quicksort is a highly researched algorithm with many variations and derivatives—it's more like a family of algorithms.

**Important:** 
 
- The most common partitioning scheme found online (Lomuto partition) performs more swaps than Hoare partition with a weak condition.
- Lomuto degrades to O(N²) when all elements are the same.
- Hoare partition with a strict condition also degrades to O(N²) for duplicate keys.
- Lomuto was popularized by Bentley in "Programming Pearls" because he found Hoare unintuitive.  
  - **Advantage:** Lomuto uses two forward iterators, so it can be used on singly linked lists.

---

## Mergesort

- **Stability:** Stable  
- **Adaptivity:** Not adaptive  
- **In-Place:** No (needs extra space)  
- **Time Complexity:** O(N log N) worst case  

Can be combined with insertion sort for small subproblem sizes.

---

## Bubble Sort

- **Stability:** Stable  
- **Adaptivity:** Can be made adaptive (add a flag to check if a swap occurred; if not, exit early)  
- **In-Place:** Yes  
- **Time Complexity:** O(N²)  

**Optimized Bubble Sort Example:**

```python
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

---

## Insertion Sort

- **Stability:** Stable  
- **Adaptivity:** Adaptive  
- **In-Place:** Yes  
- **Time Complexity:** O(N²)  

**Example:**

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
```

- Similar to optimized bubble sort, except:
  - In bubble sort, the maximum element is bubbled into the unsorted section.
  - In insertion sort, the minimum element is inserted into the sorted section.
- **Online:** Each new element can be put in its sorted place as it is received.
- **Shell Sort:** A faster variation of insertion sort (named after D.L. Shell), using insertion sort on periodic subarrays.

**See also:**  
- [Stack Overflow: Online vs Offline Sorting Algorithms](https://stackoverflow.com/questions/47712062/how-to-distinguish-online-and-offline-sorting-algorithms)  
- [CS StackExchange: Fastest Online Sorting Algorithm](https://cs.stackexchange.com/questions/55012/what-is-the-fastest-online-sorting-algorithm)

---

## Selection Sort

- **Stability:** Not stable  
- **Adaptivity:** Not adaptive  
- **In-Place:** Yes  
- **Time Complexity:** O(N²)  

**Note:**  
- Only advantage over insertion sort: performs fewer swaps.

---

## Additional Resources

1. <a href="https://www.toptal.com/developers/sorting-algorithms" target="_blank" rel="noopener noreferrer">Toptal: Sorting Algorithms</a>
2. <a href="https://www.youtube.com/playlist?list=PL9xmBV_5YoZOZSbGAXAPIq1BeUf4j20pl" target="_blank" rel="noopener noreferrer">YouTube: Sorting Algorithms Playlist</a>
