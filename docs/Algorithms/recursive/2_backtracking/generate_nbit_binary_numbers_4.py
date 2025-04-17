
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
        

        

