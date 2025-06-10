
"""
Recursive Decomposition- There is no need to maintain a path in this implementation. Therefore, no backtracking is required.
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
    # Recursively generate the binary numbers for n-1 bits
    # generate(n-1) returns a list of binary numbers of length n-1
    # We will take each of these binary numbers and prepend '1' and '0' to each of them
    l = [ "1" + _ for _ in  generate(n-1) ] 
    r = [ "0" + _ for _ in  generate(n-1) ]
    
    print(f"n = {n} , l = {l} , r = {r}")
    #Concatenate the two lists
    return l + r  

print(generate(3))