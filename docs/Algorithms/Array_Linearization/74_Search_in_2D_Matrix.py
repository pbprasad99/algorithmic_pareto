"""
Solution for :  https://leetcode.com/problems/search-a-2d-matrix/description/


If you look at the examples, the data in the 2d matrix is sorted in row-major order.

You can use a 1D index to binary search (bisect left) over the range of the entire array.

The range of the 1D index will be :
lo =0 , hi = num_rows*num_cols

To get the value at any 1D index :
matrix[1d_index//num_cols][1d_index%num_cols]
"""
class Solution:
    @staticmethod
    def get_val_at_sn(sn: int, matrix : List[List[int]]) -> int :
        """Given a 1D index into 2D Matrix, Return the corresponding Value."""
        num_rows,num_cols = len(matrix), len(matrix[0])

        return matrix[sn//num_cols][sn%num_cols ]

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        00 - 0 01 -1 02 -2
        10 - 3 11 -4 12 -5
        21 - 6  22 -7 23 -8 

        3 - 3 
        r = 1 , c = 0

        r = sn // num_cols , c = sn % num_columns
        """

        num_rows,num_cols = len(matrix), len(matrix[0])
        lo,hi = 0 , num_rows*num_cols

        while lo < hi :
            mid = (lo + hi) // 2
            val = self.get_val_at_sn(mid,matrix)
            if val < target :
                lo = mid + 1
            else :
                hi = mid
        
        if lo ==  num_rows*num_cols :
            return False
        
        if self.get_val_at_sn(lo,matrix) == target :
            return True
        
        return False
