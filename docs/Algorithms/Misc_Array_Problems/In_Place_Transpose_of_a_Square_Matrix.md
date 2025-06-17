# In Place Transpose of a Square Matrix


A square matrix can be transposed in place by just swapping elements along the diagonals. The trick is to traverse only one side of the diagonal.

The code only iterates over the lower triangle ( lower half over the diagonal excluding the diagonal itself). When you iterate over columns, iterate over [o,curr_row).

*For upper triangle iterate over [curr_row+1,n)* 

```
[
  00  01   02  03
 *10  11   12  13
 *20 *21   22  23
 *30 *31  *32  33
]
```

???+ info "Transposing a square matrix"
    ```python
    
    --8<-- "docs/Algorithms/Misc_Array_Problems/transpose_square_matrix.py"
    ```

If the matrix is not square, then for an input array of m\*n, you will have to allocate a separate target array of dimensions n\*m and copy over each element to the target array : `src[r][c] = target[c][r]`