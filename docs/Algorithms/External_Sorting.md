# External Sorting

---

## Problem Definition

Given limited RAM, how do you sort a file that is too large to fit into memory?

---

## Solution

Suppose you have an **X GB** file and only **2 GB** of RAM, where **X > 2**.

**Steps:**

1. **Divide the file** into chunks of size equal to available RAM (e.g., X // 2 GB chunks if RAM is 2 GB).
2. **For each chunk:**
    - Read the chunk into memory.
    - Sort it.
    - Write it back to disk as a "part file".
3. **Merge the sorted part files:**
    - This is now a *k-way merge* problem.
    - You can either:
        - Run a single k-way merge, or
        - Use multiple passes of two-way merges to ultimately merge all part files into a single sorted file.

---

## Additional References

1. <a href="https://en.wikipedia.org/wiki/External_sorting" target="_blank" rel="noopener noreferrer">Wikipedia: External Sorting</a>