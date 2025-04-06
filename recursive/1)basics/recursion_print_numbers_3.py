"""
Print Numbers from 1 to n  and then n to 1
""" 
def print_nums(n) :
    if n == 0 :
        return
    #preorder position
    print(n)
    #recursive call
    print_nums(n-1)
    #postorder position
    print(n)
    

print_nums(5)


