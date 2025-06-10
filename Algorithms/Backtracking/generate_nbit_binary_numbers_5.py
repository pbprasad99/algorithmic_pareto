"""
Backtracking with Dynamic Stack & For-loop Choices
Key Features:
- Combines dynamic stack operations (like version 3) with for-loop choice iteration (like version 4)
- Explicit undo operations through pop() (unlike version 2 & 4's implicit overwrites)
- More verbose but clearer state management
- Shows complete choice-explore-undo cycle explicitly
"""
def generate(n) : 
    """
    Implementation Characteristics:
    1. Dynamic Growth: path grows/shrinks as we make/undo choices
    2. Explicit State Management:
       - Choice: path.append(choice)
       - Explore: backtrack(idx+1)
       - Undo: path.pop()
    3. Uses for-loop for choices (more flexible than dual recursion)
    4. Memory Usage: O(n) but with dynamic resizing overhead
    
    Choice-Explore-Undo Pattern:
    For each position:
        For each choice (0,1):
            1. Make choice (append)
            2. Explore further (recurse)
            3. Undo choice (pop)
    """

    path = []  # We will treat this like a stack in this implementation
    res = []
    
    #choose  0 or 1 at idx
    def backtrack(idx) : 
        if idx == n: 
            res.append("".join(path[:]))
            return 
        for choice in ['0','1'] : 
            # State Change: Add choice to current path
            path.append(choice)
            # Explore: Recurse with this choice in place
            backtrack(idx+1)
            # State Restoration: Remove choice before next iteration
            path.pop()  # Explicit undo - different from array overwrite versions

    backtrack(0)
    return res

print(generate(3))




