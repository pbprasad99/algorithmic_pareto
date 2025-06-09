# Introduction

!!! note 
    This article is heavily based on [this awesome video by mcoding](https://youtu.be/tgVSkMA8joQ?si=dt5o2em5Nv2ghTj2){target="_blank"}. This is perhaps the best resource on the internet to understand binary search.

## Bisect Left

Binary search (also called **bisection search**) is an algorithm to find an element quickly in a sorted array.

!!! example 
    Suppose we are trying to find 7 in this array :
    `[2,3,3,4,6,7,8,9]`

1. **Is the element you want to find in the left half or the right half?** → Right half
    
     Our search space is now only the right half.
     ```
     [        6,7,8,9 ] # remaining 4
     ```
2. **Repeat the process**
     ```
     [        6,7     ] # remaining 2
     [          7     ] # remaining 1
     ```
3. **Finally there is just one element left. That's our element.**
         
At each step you cut out half of the search space. How can the idea be so simple, but the implementation be so difficult?. It's not - you just have to think about it in the right way.

**The First Decision: What Do You Want to Return? The object itself, or the index where it is at?**

- The index itself is a "more useful piece of information". You can always just grab the object at that index later.

**What do we do when the object we are looking for is not there?**

- Return -1? Raise exception? 
- What if there are multiple valid indices to choose from? 

With every arbitrary choice we make, we would have to remember the implementation details for each choice.

!!! warning "Implementation Complexity"
    A better way to do it, is to rephrase the question, so that there is always exactly one answer.If I were going to add another element to the array, say 7, where should I put it so that it is the first 7?
 
* If there are no 7s in the array, this answer would be the index where you would put 7 to maintain the sorted property of the array. 
* If there is at least one 7, the answer would be the index of the first 7.
* The index would be zero if the array is empty, which is not actually a valid index, but is the right answer to our Question!
* It could also be `(n-1) + 1` if the element is absent from the array and greater than all elements in a non-empty array. This is also not a valid index. But, again,it is the right answer to our Question.

!!! tip "Correct Implementation Strategy"
    The array being **sorted** is not actually the property being used in binary search. The property is that everything greater than 7 is to the right of 7 and everything less than 7 is to the left of 7.

Here, I disturbed the order of some elements in a sorted array:
`[2, 3, 5, 4, 6, 7, 9, 8]`

The array is no longer in sorted order, but notice the steps are exactly the same. What we need is that everything less than 7 is to the left of 7 and everything greater than 7 should be to the right. 

!!! tip "Important Insight"
    In fact, the numbers can be replaced with the important information: **Is this number less than 7?**
    
!!! info "Pointers"
    ```
    [2, 3, 5, 4, 6, 7, 9, 8]
     T  T  T  T  T  F  F  F  #<7?
    ```

Notice how any **Trues** are on the left and any **Falses** are on the right.

Now that we are looking at the relevant data, where do we insert 7 so that it is the first 7?

Notice that the answer we are looking for is the index of the first **False** value or the end of the array if there are no false values. This is the key insight, we need to keep in mind that makes the implementation extremely easy to remember :

!!! tip
    Squint Your Eyes and Find the First False Value


Ok, let's write the implementation:
!!! code "Bisect Left"
    ```python linenums="1"
    def bisect(arr, x):
        lo = 0
        hi = len(arr)     
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] < x:  # mid is a True value
                lo = mid + 1
            else:            # mid is a False Value
                hi = mid
        return lo
    ```

The first two lines inside the function, initialize lo and hi.

!!! tip 
    ***lo and hi are lower and upper bounds on where this First FALSE index is.*** 

If our answer is zero, it would mean that first value is False or array is empty. If it is len(arr), it would mean that all the values are True and we would have to put the new element at the end of the array.

The idea of the while loop (line 4), is that we continuously decrease the upper bound and increase the upper bound until they are equal. lo and hi will meet at the unique index we are looking for. So, we could return lo or high, once the while loop runs, it would make no difference.


Next, we calculate the midpoint in each iteration of the while loop. Python can represent arbitrarily large integers, so you do not have to worry about overflow. But, if you were using another language, you might have to worry about overflow. In that case, you would represent mid as `lo+(hi-lo)//2` : lo plus half the distance between hi and lo. If you do it this way, it will never overflow.

!!! warning "Comparing mid with x"
    Next comes the part which is often written incorrectly. We must compare whatever is at mid with our search term `x`. Remember, we are looking for the first False value where True of False is determined by the question : Is this element strictly Less than `x`: 
    ```python
    if arr[mid] < x :
        lo = mid+1   # mid is a True Value
    else :
        hi =mid      # mid is a False Value
    ```
    If `mid` is strictly less than `x`, it is a `True` Value. Since the Value at `mid` is `True`, the earliest a `False` Value could occur is the next index which is `mid+1`. Therefore, our lower bound becomes `mid+1`

    What if `mid` is a `False` Value? In this case the FIRST `False` Value could not be any later than mid. But it could be mid or earlier than mid. There could be other `False` values before midm. So our upper bound becomes mid.

    When the while loop is done, lo and hi meet at the index we are looking for.



How do we know that this implementation always gives the right answer?
 - We know that lo is always <=  answer
 - We also know that answer is always <= hi
 - In each iteration the difference between hi and lo always decreases by at least one.
 
 Thereifre, lo and hi always meet at the answer.

But how do we know that in each iteration lo and hi come closer to each other by at least one?  
If we enter the True clause on line no. 6 `lo = mid+1` ensures that lo always increases by at least one.

If we enter the False clause on lines 8,9 we are setting hi to mid. So, hopefully we are lowering hi. But how do we know mid is actually strictly less than hi?

Here we are actually using the property that **integer division rounds down**. Inside the while loop: **while lo < hi, lo is strictly less than hi**.
So **lo + hi** is strictly less than **hi + hi**.

That means for calculating **mid**:
**mid = (lo + hi) // 2**

When we divide **(lo + hi)** by 2 and round down we will get something strictly less than **(hi + hi) // 2** i.e. **hi**.

### Checking the return value of Bisect Left

Since bisect left can return an out of bounds index and not necessarily the index of a matching value, you have to handle this when using it, depending on what you are trying to do.  

!!! example "Checking if x exists using bisect left"
    ```
    def search(arr:list, x) ->int :
        idx = bisect_left(arr,x)
        if i != len(arr) and arr[i] == x:
            return i
        raise ValueError(f"{x} not found!")
    ```

## Bisect Right

But wait. Your ask: instead of returning a 7 so that it is the first seven, could I not return the index, so that it would be the last 7?

You could. You could follow the same analysis and get a very similar algorithm.

To find where it should go to be the first 7, the relevant piece of information is: **"Is this (current element) strictly less than 7"**

To find where it should go to be the last element, the relevant piece of information i: **"Is this (current element) less than or equal to  7"**

!!! info "Bisect Left vs Bisect Right"
    ```
    [2, 3, 5, 4, 6, 7, 7, 7, 8, 9]
    [T, T, T, T, T, F, F, F, F, F] #<7  ; Bisect Left
    [T, T, T, T, T, T, T, T, F, F] #<=7 ; Bisect Right
    ```

In either case, you are looking for the **first False value**. You just need to decide what you mean by True or False.

!!! code "Bisect Right"
    ```python linenums="1"
    def bisect_right(arr, x):
        lo = 0
        hi = len(arr)     
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= x:  # mid is a True value
                lo = mid + 1
            else:            # mid is a False Value
                hi = mid
        return lo
    ```

### Checking the return value of Bisect Right
Bisect right can return values from 0 to len(arr). If it returns zero it means that either arr is empty or all elements in the array are greater than x. Any other value could mean x exists at i-1. A return value of len(arr) means x is greater than or equal to all elements in the array.

!!! example "Checking if x exists using bisect right"
    ```
    def search(arr:list, x) ->int :
        idx = bisect_right(arr,x)
        if i > 0 and arr[i-1] == x:
            return i
        raise ValueError(f"{x} not found!")
    ```


## Summary

!!! success "Key Takeaways"
    - Binary search is fundamentally about finding boundaries in sorted data
    - Reframe the problem as "find the first False value" 
    - The difference between `bisect_left` and `bisect_right` is just changing `<` to `≤`
    - Always think about what "True" and "False" mean in your specific context