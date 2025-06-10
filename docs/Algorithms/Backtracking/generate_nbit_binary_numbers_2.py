"""
Backtracking Implementation Using Pre-allocated Array Strategy
Key Features:
- Uses fixed-size array instead of growing/shrinking structure
- No push/pop operations needed
- Memory efficient as array size is known upfront
- Implicit undoing of choices through overwriting
"""
def generate(n) : 
    """
    Implementation Notes:
    1. Pre-allocated array of size 'n' with None values
    2. Each position directly overwritten with 0 or 1
    3. No need for explicit undo operations
    4. More efficient than stack-based approaches for known size problems
    
    Memory Layout (n=3):
    Initial: [None, None, None]
    During:  ['0'/'1', '0'/'1', '0'/'1']

    Time Complexity: O(2^n) - must generate all binary numbers
    Space Complexity: O(n) - fixed size array, no additional growth
    """
    
    # Pre-allocate array of size n - more efficient than growing/shrinking a list
    path = [None] * n
    res = []
    
    #choose  0 or 1 at idx
    def backtrack(idx) : 
        if idx == len(path): 
            res.append("".join(path[:]))
            return 
        # Direct assignment to index - no push/pop needed
        path[idx] = '0'
        backtrack(idx+1)
        # No explicit undo needed - next assignment overwrites
        
        path[idx] = '1'
        backtrack(idx+1)
        # No explicit undo needed at end - array will be reused

    backtrack(0)
    return res

print(generate(4))




