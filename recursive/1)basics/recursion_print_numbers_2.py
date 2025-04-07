"""
Print Numbers from 1 to n .
"""

def print_nums_1_to_n(n) :
    if n == 0 :
        return
    print_nums_1_to_n(n-1)
    print(n)

#print  1 to n
print_nums_1_to_n(5)


"""
Print Numbers from n to 1 .
"""

def print_nums_n_to_1(n) :
    #base cases
    if n == 0 :
        return

    print(n)
    print_nums_n_to_1(n-1)


print_nums_n_to_1(5)
    

