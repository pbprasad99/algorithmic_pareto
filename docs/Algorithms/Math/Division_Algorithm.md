# The Division Algorithm

!!! quote "[LibreTexts- Mathematics](https://math.libretexts.org/Bookshelves/Combinatorics_and_Discrete_Mathematics/A_Spiral_Workbook_for_Discrete_Mathematics_(Kwong)/05%3A_Basic_Number_Theory/5.02%3A_Division_Algorithm){target="_blank"}"
    Given any integers $a$ and $b$, where $a > 0$, there exist integers $q$ and $r$ such that
        
    $b = aq + r$
    
    where $0 \leq r < a$. Furthermore, $q$ and $r$ are uniquely determined by $a$ and $b$.
    
    The integers $b$, $a$, $q$, and $r$ are called the dividend, divisor, quotient, and remainder, respectively. Notice that $b$ is a multiple of $a$ if and only if $r = 0$.

 - b - Dividend
 - a - Divisor
 - q - Quotient
 - r - Remainnder 

## In Python

divmod(dividend,divisor) -> (quotient, remainder)

divmod(b,a) -> (b//a,b%a)

!!! example
    ```python
    >>>divmod(1,10)
    >>>(0, 1)
    ```

!!! example
    ```python
    >>> divmod(4,2)
    (2, 0)
    >>> 4 // 2
    2
    >>> 4 % 2
    0
    ```

## Python Rounds Negative Nymbers away from zero

In python :

15 / -4  = - 3.75

But,

14// - 4 =  - 4


To round towards zero, do floating point division and convert to int.

```python
Do floating point division then convert to an int. No extra modules needed.

Python 3:

>>> int(-1 / 2)
0
>>> int(-3 / 2)
-1
>>> int(1 / 2)
0
>>> int(3 / 2)
1

Python 2:

>>> int(float(-1) / 2)
0
>>> int(float(-3) / 2)
-1
>>> int(float(1) / 2)
0
>>> int(float(3) / 2)
1
```

??? example "[Example - Evaluate RPN](https://leetcode.com/problems/evaluate-reverse-polish-notation/){target="_blank"}"
    ```python
    """
    What is the data :
    RPN expression as a list of tokens
    tokens = ["2","1","+","3","*"]
    
    
    For each opearator +,-,*,/ there will be two pops.
    first pop is the rhs and second pop is the lhs 
    
    Pitfall :
    In python integer division truncates away from zero
    >>> -4//3
    -2             ## Truncates away from zero for negative numbers
    >>> 4//3    
    1              ## Truncates towards zero for positive numbers
    
    To handle this :
    >>> -4/3               ## Do floating point division first
    -1.3333333333333333
    >>> int(-4/3)          ## Then cast to int and result will always truncate towards zero.
    -1
    """
    class Solution:
        def evalRPN(self, tokens: List[str]) -> int:
            evaluate  = {
                '+' : lambda x,y : x+y ,
                '-' : lambda x,y : x-y,
                '/' : lambda x,y : int(x/y),
                '*' : lambda x,y : x*y 
            }
            stack = []
            for token in tokens : 
                if token in evaluate :
                    rhs = stack.pop()
                    lhs = stack.pop()
                    stack.append(evaluate[token](lhs,rhs))
                else :
                    stack.append(int(token))
            return stack[-1]
    ```
    

## Additional Resources : 

[LibreTexts- Mathematics](https://math.libretexts.org/Bookshelves/Combinatorics_and_Discrete_Mathematics/A_Spiral_Workbook_for_Discrete_Mathematics_(Kwong)/05%3A_Basic_Number_Theory/5.02%3A_Division_Algorithm){target="_blank"}