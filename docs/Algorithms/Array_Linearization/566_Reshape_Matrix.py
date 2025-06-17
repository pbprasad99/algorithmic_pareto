"""
Solution for: https://leetcode.com/problems/reshape-the-matrix/

Allocate the target array.
Use 1D indexing to read and write values from the source matrix to the target matrix.
"""
class Solution:
    @staticmethod
    def read_val(linear_index, matrix) : 
        num_cols = len(matrix[0])
        return matrix[linear_index//num_cols][linear_index%num_cols]
    
    @staticmethod
    def write_val(linear_index, matrix,val) :
        """
        write val at linear index into matrix
        """
        num_cols = len(matrix[0])
        matrix[linear_index//num_cols][linear_index%num_cols] = val 

    def matrixReshape(self, mat: List[List[int]], r: int, c: int) -> List[List[int]]:

        #Quote :"If the reshape operation with given parameters is possible and legal, output the new reshaped matrix; Otherwise, output the original matrix."
        if not len(mat)*len(mat[0]) == r*c :
            return mat

        # Allocate target Matrix 
        target = [ [0]*c for _ in range(r) ]

        #read from source matrix and write into target matrix
        for i in range(len(mat) * len(mat[0])) :
            val = self.read_val(i,mat)
            self.write_val(i,target,val)
        
        return target