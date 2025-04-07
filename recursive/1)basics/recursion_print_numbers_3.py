"""
Print Numbers n to 1 and then 1 to n
""" 
def print_nums(n) :
    if n == 0 :
        print("Base Case Hit.")
        return
    #preorder position
    print(f"Preorder : {n}")
    #recursive call
    print_nums(n-1)
    #postorder position
    print(f"Postorder : {n}")
    

print_nums(5)


