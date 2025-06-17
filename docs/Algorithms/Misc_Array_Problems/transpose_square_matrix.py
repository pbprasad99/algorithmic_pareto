def transpose(matrix) :
    """
    Transpose an n*n matrix
    """
    n = len(matrix)
    try :
        assert n == len(matrix[0])
    except AssertionError :
        print("Not a square matrix")
        raise

    for r in range(n) :
        #for c in range(r+1, n) : # Iterate over the upper triangle
        for c in range(r) : # Iterate over the lower triangle
            print(f"Swapping ({r},{c}) with ({c},{r})")
            matrix[r][c], matrix[c][r] = matrix[c][r],matrix[r][c]
    
    return matrix

if __name__ == "__main__" :
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print("Original Matrix:")
    for row in matrix:
        print(row)
    
    transposed_matrix = transpose(matrix)
    print("\nTransposed Matrix:")
    for row in transposed_matrix:
        print(row)