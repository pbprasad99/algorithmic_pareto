# Backtracking

Backtracking seems confusing and difficult to learn, because there are many different ways of doing the same thing.

Here, we solve the same problem in many different ways only to see the possibilities.

There is no staisfying and clear definition of backtracking I have found yet. I like to define it as an exhaustive search technique where you make a choice, explore that choice and then undo the choice (backtrack) to make another choice. 

***This act of making a choice and undoing it is backtracking.***

It looks very much like a depth first tree traversal (or graph) traversal with state management.

## Problem: Generate N-bit Binary Numbers

Given an integer n, generate all possible binary numbers of length n and return them as a list of strings.

### Examples:
```
Input: n = 2
Output: ["00", "01", "10", "11"]

Input: n = 3
Output: ["000", "001", "010", "011", "100", "101", "110", "111"]
```

### Constraints:
- 1 ≤ n ≤ 16
- The result list should be in lexicographically sorted order
- Each binary number in the output should be exactly n digits long (pad with leading zeros if necessary)

## Implementation Approaches

!!! approach "Approach 0: Pure Recursion"
    Uses recursive decomposition without backtracking. Each recursive call returns its own result list.
    ```python
    --8<--
    docs/Algorithms/Backtracking/generate_nbit_binary_numbers_1.py
    --8<--
    ```
    
    This approach:
    - Uses pure recursive decomposition
    - Each call builds its own result independently
    - No need for global state or backtracking
    - More intuitive but less memory efficient
    - Time: O(2^n), Space: O(2^n) due to string copies

!!! approach "Approach 1: Pre-allocated Array"
    Uses a fixed-size array with direct index assignments. Most memory efficient for known size problems.
    ```python
    --8<--
    docs/Algorithms/Backtracking/generate_nbit_binary_numbers_2.py
    --8<--
    ```

!!! approach "Approach 2: Stack-based with Dual Recursion"
    Uses explicit push/pop operations with two separate recursive calls for '0' and '1'.
    ```python
    --8<--
    docs/Algorithms/Backtracking/generate_nbit_binary_numbers_3.py
    --8<--
    ```

!!! approach "Approach 3: For-loop Choices"
    Uses iteration over choices, making it more extensible for problems with multiple choices.
    ```python
    --8<--
    docs/Algorithms/Backtracking/generate_nbit_binary_numbers_4.py
    --8<--
    ```

!!! approach "Approach 4: Dynamic Stack with For-loop"
    Combines dynamic stack operations with for-loop choice iteration for clearer state management.
    ```python
    --8<--
    docs/Algorithms/Backtracking/generate_nbit_binary_numbers_5.py
    --8<--
    ```

## Comparison of Approaches

| Approach | Memory Usage | State Management | Extensibility | Code Clarity |
|----------|-------------|------------------|---------------|--------------|
| Pure Recursion | O(2^n) | None (functional) | Limited | Excellent |
| Pre-allocated Array | Most efficient (O(n) fixed) | Implicit (overwrites) | Limited | Good |
| Stack with Dual Recursion | O(n) with resizing | Explicit (push/pop) | Limited | Very Good |
| For-loop Choices | O(n) fixed | Implicit (overwrites) | Excellent | Good |
| Dynamic Stack with For-loop | O(n) with resizing | Most explicit | Excellent | Excellent |

!!! success "Key Takeaways"

    1. **Pure Recursion**: Intuitive but least memory efficient. No bactracking involved.
    2. **Pre-allocated Array**: Best for memory efficiency when size is known
    3. **Stack with Dual Recursion**: Most intuitive for binary choices
    4. **For-loop Choices**: Most extensible for varying number of choices
    5. **Dynamic Stack with For-loop**: Best balance of clarity and flexibility
    


