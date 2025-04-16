"""
Print Numbers from i to 5.
"""

def print_nums(i) :
    if i > 5 :
        return
    
    #preorder position
    print(i)
    #recursive call
    print_nums(i+1)

"""
Print Numbers from i to 5 in reverse order
"""

def print_nums_backwards(i) :
    if i > 5 :
        return

    #recursive call
    print_nums_backwards(i+1)
    #postorder position
    print(i)


print_nums(1)
print_nums_backwards(1)






    

