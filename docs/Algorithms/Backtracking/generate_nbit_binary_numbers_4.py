"""
Generate n-bit binary numbers using backtracking with for-loop iteration.
Implementation Strategy: For-loop Based Choice Selection
- Uses pre-allocated array like version 2
- Iterates over choices using for-loop instead of explicit recursive calls
- More generalizable pattern that can handle multiple choices beyond just binary
- Common pattern in backtracking problems where we iterate over available choices
"""
def generate(n) : 
    """
    Key Differences from Other Versions:
    1. Uses for-loop to iterate over choices ['0','1']
    2. Single recursive call instead of multiple explicit ones
    3. More extensible - easy to add more choices if needed
    4. Common pattern seen in other backtracking problems like:
       - Generating permutations (choices are remaining numbers)
       - N-Queens (choices are valid positions)
       - Sudoku (choices are valid digits)

    Memory Layout:
    - Pre-allocated array: [None] * n
    - Choices handled by for-loop: for choice in ['0','1']
    - Implicit undo through overwriting
    """

    path = [None] * n
    res = []
    
    #choose  0 or 1 at idx
    def backtrack(idx) : 
        if idx == len(path): 
            res.append("".join(path[:]))
            return 
        for choice in ['0','1'] : 
            path[idx] = choice
            backtrack(idx+1)
            #Here we dont care if path[idx] overwritten,
            #Undo of choice is implicit

    backtrack(0)
    return res

print(generate(3))




