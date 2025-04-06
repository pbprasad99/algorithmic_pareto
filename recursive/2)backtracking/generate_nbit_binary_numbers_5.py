
"""
Recursive Decomposition
"""
def generate(n) : 
    """
    Eg : For n = 3 , We have 3 spots each of which can be filled with 0 or 1. 
    
    -    -   -
    1/0
         1/0  
             1/0
    
    1 1 1
    1 1 0
    1 0 1
    1 0 0
    0 1 1
    0 1 0
    0 0 1
    0 0 0 
    """

    path = []  # We will treat this like a stack in this implementation
    res = []
    
    #choose  0 or 1 at idx
    def backtrack(idx) : 
        if idx == n: 
            res.append("".join(path[:]))
            return 
        for choice in ['0','1'] : 
            #Make a choice 
            path.append(choice)
            #Explore this choice
            backtrack(idx+1)
            #Undo this choice before making next choice. Undo of choice is explicit
            path.pop()

    backtrack(0)
    return res

print(generate(3))
        

        

