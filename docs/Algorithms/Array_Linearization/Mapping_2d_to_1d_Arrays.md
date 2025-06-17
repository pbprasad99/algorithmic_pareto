# Mapping 2D Array to 1D Array

Consider a 2D array:

```
[
  [00, 01, 02],
  [11, 12, 13]
]
```

To convert this 2D array to a 1D array using **row-major order**, you list the elements row by row:

```
[ 00  ,01 , 02,   11,   12 ,  13 ]
  0     1   2      3     4    5 
```

## Row Major Order

For example, the element `12` is at position `(1, 2)` (row index 1, column index 2). Its corresponding index in the 1D array is `4`.

The general formula for mapping a 2D array element at position $(\text{row_index},\ \text{col_index})$ to a 1D array index is:

$$
\text{index} = \text{row_index} \times \text{number_of_cols} + \text{col_index}
$$

**Explanation:**

- $\text{row_index} \times \text{number_of_cols}$: Counts all elements in the rows before the current row.
- $\text{col_index}$: Gives the position within the current row.

So, to find the 1D index, count all elements in previous rows, then add the column index of the current element.

## Column Major Order

To convert a 2D array to a 1D array using **column-major order**, you list the elements column by column:

```
[ 00, 11,   01,  12,  02,  13]
  0   1     2    3    4    5
```

For example, the element `12` is at position `(1, 2)` (row index 1, column index 2). Its corresponding index in the 1D array is `3`.

The general formula for mapping a 2D array element at position $(\text{row_index},\ \text{col_index})$ to a 1D array index in column-major order is:


$$
\text{index} = \text{col_index} \times \text{number_of_rows} + \text{row_index}
$$

**Explanation:**

- $\text{col_index} \times \text{number_of_rows}$: Counts all elements in the columns before the current column.
- $\text{row_index}$: Gives the position within the current column.

So, to find the 1D index, count all elements in previous columns, then add the row index of the current element.

## Addition Resources

1. [Wikipedia - Row Major vs Column Major](https://en.wikipedia.org/wiki/Row-_and_column-major_order#:~:text=column%2Dmajor%20languages.-,Programming%20languages%20and%20libraries,Scilab%2C%20Yorick%2C%20and%20Rasdaman.){target="_blank"}
2. [Performance Analysis : Row Major vs Column Major](https://www.modular.com/blog/row-major-vs-column-major-matrices-a-performance-analysis-in-mojo-and-numpy#:~:text=Row%2Dmajor%20order%20vs.&text=Since%20it's%20faster%20to%20read,on%20column%2Dmajor%20order%20matrices.){target="_blank"}
3. [Why Use Parquet](https://www.upsolver.com/blog/apache-parquet-why-use#:~:text=As%20we%20mentioned%20above%2C%20Parquet,together%20in%20each%20row%20group:){target="_blank"}
4. [Reddit Discussion on Columnar DBs](https://www.reddit.com/r/dataengineering/comments/1ctzjxo/columnar_vs_relational_databases/#:~:text=These%20are%20things%20at%20completely%20different%20levels,will%20be%20very%20expensive\).%20Upvote%201%20Downvote.){target="_blank"}


