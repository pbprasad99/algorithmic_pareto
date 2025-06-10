"""
Generate n-bit binary numbers using backtracking.
Implementation Strategy: Stack-based Backtracking 
- Uses list as stack for building binary numbers
- For each position, we make TWO recursive calls because:
  1. First recursive call explores path after choosing '0'
  2. Second recursive call explores path after choosing '1'
- This creates a binary tree where each node represents a digit position
  and has exactly two children (one for '0' and one for '1')
"""
def generate(n) : 
    """
    Decision Tree Shows Two Branches at Each Level:
    Root
    ├── 0 (First recursive call)
    │   ├── 00
    │   └── 01
    └── 1 (Second recursive call)
        ├── 10
        └── 11

    Two Recursive Calls Pattern:
    1. First Call (with '0'): Explores all possibilities starting with '0'
    2. Second Call (with '1'): Explores all possibilities starting with '1'
    
    This ensures we generate ALL possible combinations systematically
    """

    path = [] #We will treat this as a stack in this implementation
    res = []
    
    #choose  0 or 1 at idx
    def backtrack(idx) : 
        if idx == n: 
            res.append("".join(path[:]))
            return 

        # First Recursive Branch: Try '0' at current position
        path.append('0')
        backtrack(idx+1)  # Explore all possibilities after choosing '0'
        path.pop()        # Backtrack by removing '0'

        # Second Recursive Branch: Try '1' at current position
        path.append('1')
        backtrack(idx+1)  # Explore all possibilities after choosing '1'
        path.pop()        # Backtrack by removing '1'

    backtrack(0)
    return res

print(generate(3))




