"""
Print Numbers from 1 to n .
"""

def print_nums(n) :
    if n == 0 :
        return
    print_nums(n-1)
    print(n)

print_nums(5)


"""
Print Numbers from n to 1 .
"""

def print_nums(n) :
    #base cases
    if n == 0 :
        return

    print(n)
    print_nums(n-1)


print_nums(5)
    

