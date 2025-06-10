# Basic Recursion

Recursion can be tricky to understand, especially when it comes to the order of operations. Here, we'll try to understand what happens when you "do" something before the recursive call (preorder position) or after the recursive call (postorder position). 

Debug this in your IDE and see what is happening on the stack and how function calls are stacked and unwound.


## Understanding Recursive Positions

1. **Preorder Position**: Operations performed before the recursive call
2. **Postorder Position**: Operations performed after the recursive call
3. **Base Case**: Condition to stop recursion

## Implementation Approaches

!!! approach "Print i to 5 forwards and backwards"
    Input is the starting point .Use preorder position to print in ascending order and postorder position to print in reverse order. Base Case is when i exceeds 5.
    ```python 
    --8<--
    docs/Algorithms/Basic_Recursion/recursion_print_numbers_1.py
    --8<--
    ```
    In preorder position, numbers are printed along with stack build up. In postorder, stack builds up before any print statement is executed and numbers are printed as the stack unwinds.
    
!!! approach "Print numbers forward and backward in the range 1 to n." 
    n is the input parameter to the function. Base case is when n becomes less than 1 i.e. equal to zero. Here, we have to print in postorder position to get the output in ascending order. We use preorder position to print in descending order. This is becuase we are taking the upper bound as input. Whereas, in the previous example, we took the lower bound as input. 
    ```python
    --8<--
    docs/Algorithms/Basic_Recursion/recursion_print_numbers_2.py
    --8<--
    ```
    The takeaway is that preorder position matches the input order and postorder position matches the reverse of the input order.

!!! approach "Approach 3: Print Both Ways"
    Uses both preorder and postorder positions to print numbers in both orders.
    ```python
    --8<--
    docs/Algorithms/Basic_Recursion/recursion_print_numbers_3.py
    --8<--
    ```

## Comparison of Approaches

| Position | When Operation Happens | Stack State | Output Order |
|----------|----------------------|-------------|--------------|
| Preorder | Before recursive call | During stack building | Same as Inout Order |
| Postorder | After recursive call | During stack unwinding | Reverse of Input Order |
| Both | Before and after | Both phases | Both orders |


!!! success "Key Takeaways"
    1. **Operation Placement**: The position of operations relative to the recursive call determines the order of execution
    2. **Stack Behavior**:
        - Stack builds up: Follows input order (n → n-1 → n-2 → ... → 1)
        - Stack unwinds: Reverse of input order (1 → 2 → ... → n-1 → n)
    3. **Memory Usage**: All approaches use O(n) stack space
    4. **Choose Based On**:
        - Same as input order → Use preorder position
        - Reverse of input order → Use postorder position
        - Both orders → Use both positions