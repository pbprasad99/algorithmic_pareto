
"""
Recursive Decomposition
"""
def generate(n) : 
    """
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

    path = [] #We will treat this as a stack in this implementation
    res = []
    
    #choose  0 or 1 at idx
    def backtrack(idx) : 
        if idx == n: 
            res.append("".join(path[:]))
            return 
        #Pick 0
        path.append('0')
        #Explore 0 
        backtrack(idx+1)
        #Undo 0 
        path.pop()
        #Pick 1
        path.append('1')
        #Explore 1
        backtrack(idx+1)
        #Undo 1
        path.pop()

    backtrack(0)
    return res

print(generate(3))
        

        

