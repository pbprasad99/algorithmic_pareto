
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
    if n == 0 : 
        return [""]

    l = [ "1" + _ for _ in  generate(n-1) ] 
    r = [ "0" + _ for _ in  generate(n-1) ]

    return l + r  

print(generate(3))