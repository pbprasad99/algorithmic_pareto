# Mapping 1D Array to 2D Array

Consider a 1D array that represents a 2D array:

```
[ 00, 01, 02, 11, 12, 13 ]  # Row-major order
  0   1   2   3   4   5
```

This could represent the following 2D array:
```
[
  [00, 01, 02],
  [11, 12, 13]
]
```

## Row-Major Order

To convert a 1D array index back to 2D array coordinates in **row-major order**, use these formulas:

$$
\text{row_index} = \left\lfloor\frac{\text{index}}{\text{number_of_cols}}\right\rfloor
$$

$$
\text{col_index} = \text{index} \bmod \text{number_of_cols}
$$

**Explanation:**

- Integer division (⌊index/cols⌋) gives the row number because each row contains `number_of_cols` elements
- Remainder (modulo) gives the position within that row

For example, given index `4` with `number_of_cols = 3`:

- row_index = ⌊4/3⌋ = 1
- col_index = 4 mod 3 = 1
- Therefore, index 4 maps to position (1,1)

## Column-Major Order

For a 1D array in **column-major order**:
```
[ 00, 11, 01, 12, 02, 13 ]  # Column-major order
  0   1   2   3   4   5
```

The formulas are:

$$
\text{row_index} = \text{index} \bmod \text{number_of_rows}
$$

$$
\text{col_index} = \left\lfloor\frac{\text{index}}{\text{number_of_rows}}\right\rfloor
$$

**Explanation:**

- Remainder (modulo) gives position within the current column
- Integer division gives which column we're in

For example, given index `3` with `number_of_rows = 2`:

- row_index = 3 mod 2 = 1
- col_index = ⌊3/2⌋ = 1
- Therefore, index 3 maps to position (1,1)


## Practice

??? example "[Search in a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/){target="_blank"}"

    ```python 
             --8<-- "docs/Algorithms/Array_Linearization/74_Search_in_2D_Matrix.py"
    ```

??? example "[Reshape Matrix](https://leetcode.com/problems/reshape-the-matrix/){target="_blank"}"

    ```python 
             --8<-- "docs/Algorithms/Array_Linearization/566_Reshape_Matrix.py"
    ```