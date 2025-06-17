# Allocate, Copy and Transpose 2D Matrix

Avoid shallow copy bugs and stick to list comprehensions when copying and allocating 2D arrays.

## Allocating a 2D array

Allocate target Matrix of num_rows* num_cols intialized to 0 

!!! info "Allocate a 2D matrix" 
    >target = [ [0]*num_cols for _ in range(num_rows) ]

## Copying a 2D Matrix

!!! info "Create copy of 2D array"

    ```python
    class Solution:
      def get_copy(self,matrix: List[List[int]] ) -> List[List[int]]  : 
          num_rows, num_cols = len(matrix), len(matrix[0])
          # Using Nested List Comprehension.
          copy = [[matrix[r][c] for c in range(num_cols)] for r in range(num_rows)]
          return copy
    ```

## Transposing a 2D matrix

In a transposed matrix, the rows become columns and columns become rows. Which means :

`src[r][c] == target[c][r]` 

OR

`target[r][c] == src[c][r]`

!!! info "[Transpose of a matrix](https://leetcode.com/problems/transpose-matrix/){target="_blank"}"
    ```python
    """
    Solution for : https://leetcode.com/problems/transpose-matrix/
    You could alternately preallocate an n*m target matrix and copy over each element from src to target matrix using a nested loop over the original matrix.
    """
    class Solution:
        def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
            num_rows = len(matrix)
            num_cols = len(matrix[0])
            # Using Nested List Comprehension. Number of Columns equal number of rows.
            # Remember : target[r][c] = src[c][r]
            transpose = [[matrix[c][r] for c in range(num_rows)] for r in range(num_cols)]
            return transpose
    ```

