# Diagonal and Antidiagonal traversal of Square Matrix

The important thing to note here is that the diagonal and antidiagonal overlap only in cases when the square matrix has an odd number of rows/columns and the overlapping cell will always have the same row and column index.

Another thing to not is that the number of elements in the diagonal and antidiagonal of an n*n matrix is the same as number of rows/columns.


As for the diagonal traversal it is easy:

```
Iterate n times :
   start from [0,0] and keep adding one to both r and c.
```

For the antidiagonal, if you start from the bottom left,  the column index remains the same as that of the diagonal and the row index is n-1 - row_index of diagonal.

So, we can iterate over the same antidiagonal:

```
Iterate n times :
   start from [n-1,0] and keep adding one to c and subtracting 1 from r.
```

Of course, we only need a single loop to iterate over both. Just take care of the overlapping cell in case you are doing arithmetic on the elements.


## Practice

???+ example "[Matrix Diagonal Sum](https://leetcode.com/problems/matrix-diagonal-sum/){target="_blank"}"
     ```python
     """
     Solution for : https://leetcode.com/problems/matrix-diagonal-sum/
 
     Eyeball this and you will get the pattern :
 
     00 01 02
     10 11 12
     20 21 22
     """
     class Solution:
         def diagonalSum(self, mat: List[List[int]]) -> int:
             total = 0
             n = len(mat) 
             for i in range(len(mat)) :
                 total+=mat[i][i] 
                 # Do not count if this is an overlapping cell
                 if (n-1) - i == i : continue
                 #Traverse Anti Diagonal from bottom left to top right
                 total+=mat[(n-1)-i][i]
             return total 
     ```







