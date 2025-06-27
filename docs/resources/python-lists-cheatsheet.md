# Python Lists Cheatsheet

Lists are one of Python's most versatile and commonly used data structures. They store ordered collections of items that can be of any type. This cheatsheet covers all essential list operations and methods with clear examples and explanations.

## Creating Lists

```python
# Empty list
empty_list = []
empty_list = list()

# List with initial values
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, [1, 2]]

# Using the list() constructor
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']

# List of repeated values
zeros = [0] * 5  # [0, 0, 0, 0, 0]
repeated = ["ab"] * 3  # ['ab', 'ab', 'ab']

# Using range
range_list = list(range(5))  # [0, 1, 2, 3, 4]
even_numbers = list(range(0, 10, 2))  # [0, 2, 4, 6, 8]

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
even_squares = [x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]
```

## Accessing Elements

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Indexing (0-based)
first = fruits[0]  # "apple"
last = fruits[-1]  # "elderberry"

# Slicing [start:stop:step]
first_three = fruits[0:3]  # ["apple", "banana", "cherry"]
first_three = fruits[:3]   # Same as above (start defaults to 0)
last_three = fruits[2:]    # ["cherry", "date", "elderberry"] (stop defaults to length)
copy_list = fruits[:]      # Creates a shallow copy of the list

# Extended slicing
every_second = fruits[::2]  # ["apple", "cherry", "elderberry"]
reversed_list = fruits[::-1]  # ["elderberry", "date", "cherry", "banana", "apple"]
```

### Understanding Slice Notation [start:stop:step]

The slice notation `[start:stop:step]` is a powerful feature for accessing portions of lists:

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Slice syntax: list[start:stop:step]
# - start: the index to start from (inclusive)
# - stop: the index to stop before (exclusive)
# - step: the stride between elements

# Important: Slicing ALWAYS creates a new list with copied elements
original = [1, 2, 3, 4, 5]
sliced = original[1:4]  # Creates a new list [2, 3, 4]
original[1] = 20        # Modifying original doesn't affect sliced
print(sliced)           # Still [2, 3, 4]

# Basic slice with all parameters
subset = numbers[1:8:2]  # [1, 3, 5, 7]
# Starts at index 1, stops before index 8, takes every 2nd element

# Omitting parameters (uses defaults)
first_five = numbers[:5]    # [0, 1, 2, 3, 4] (start defaults to 0)
from_three = numbers[3:]    # [3, 4, 5, 6, 7, 8, 9] (stop defaults to len(numbers))
every_third = numbers[::3]  # [0, 3, 6, 9] (start=0, stop=len(numbers))

# Negative indices count from the end
last_three = numbers[-3:]   # [7, 8, 9] (start at 3rd from end)
except_last_two = numbers[:-2]  # [0, 1, 2, 3, 4, 5, 6, 7] (stop 2 from end)

# Negative step reverses the slice direction
reversed_numbers = numbers[::-1]  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
reversed_subset = numbers[7:2:-1]  # [7, 6, 5, 4, 3] (start at 7, stop before 2, go backwards)
last_three_reversed = numbers[-1:-4:-1]  # [9, 8, 7]

# Empty slices
empty1 = numbers[5:5]      # [] (start equals stop)
empty2 = numbers[7:3]      # [] (start > stop with positive step)
empty3 = numbers[3:7:-1]   # [] (start < stop with negative step)

# Slice bounds are automatically adjusted if out of range
large_stop = numbers[5:100]  # [5, 6, 7, 8, 9] (stop is truncated to list length)
negative_start = numbers[-100:3]  # [0, 1, 2] (start is truncated to list beginning)

# Memory usage consideration:
# Since slicing creates a new list, be cautious with very large lists
# If you don't need a copy, consider using itertools.islice for iteration only
import itertools
for item in itertools.islice(large_list, 1, 8, 2):
    process(item)  # More memory efficient than looping through a slice
```

### Common Slice Patterns

```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Get first n elements
first_3 = items[:3]  # [0, 1, 2]

# Get last n elements
last_3 = items[-3:]  # [7, 8, 9]

# Get all except first n elements
skip_first_2 = items[2:]  # [2, 3, 4, 5, 6, 7, 8, 9]

# Get all except last n elements
skip_last_2 = items[:-2]  # [0, 1, 2, 3, 4, 5, 6, 7]

# Reverse a list
reversed_items = items[::-1]  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# Every nth element
every_3rd = items[::3]  # [0, 3, 6, 9]

# Every nth element, starting from mth
from_2nd_every_3rd = items[1::3]  # [1, 4, 7]

# Middle slice
middle = items[3:7]  # [3, 4, 5, 6]

# Reversing a specific section
reversed_section = items[:5] + items[5:8][::-1] + items[8:]
# [0, 1, 2, 3, 4, 7, 6, 5, 8, 9]
```

## Modifying Lists

### Adding Elements

```python
fruits = ["apple", "banana"]

# Append a single element to the end
fruits.append("cherry")  # ["apple", "banana", "cherry"]

# Insert an element at a specific position
fruits.insert(1, "apricot")  # ["apple", "apricot", "banana", "cherry"]

# Extend the list with another iterable
fruits.extend(["date", "elderberry"])  # ["apple", "apricot", "banana", "cherry", "date", "elderberry"]
# Equivalent to:
fruits += ["fig", "grape"]  # ["apple", "apricot", "banana", "cherry", "date", "elderberry", "fig", "grape"]
```

### Removing Elements

```python
fruits = ["apple", "banana", "cherry", "date", "banana", "elderberry"]

# Remove by value (first occurrence)
fruits.remove("banana")  # ["apple", "cherry", "date", "banana", "elderberry"]

# Remove by index and get the value
cherry = fruits.pop(1)  # cherry = "cherry", fruits = ["apple", "date", "banana", "elderberry"]
last = fruits.pop()     # last = "elderberry", fruits = ["apple", "date", "banana"]

# Remove by index without returning the value
del fruits[1]  # fruits = ["apple", "banana"]

# Remove a slice
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
del fruits[1:3]  # fruits = ["apple", "date", "elderberry"]

# Clear the entire list
fruits.clear()  # fruits = []
```

### Modifying Elements

```python
fruits = ["apple", "banana", "cherry"]

# Change a single element
fruits[1] = "blueberry"  # ["apple", "blueberry", "cherry"]

# Change multiple elements with slice assignment
fruits[0:2] = ["apricot", "blackberry"]  # ["apricot", "blackberry", "cherry"]

# Insert multiple elements with slice assignment
fruits = ["apple", "cherry"]
fruits[1:1] = ["banana", "blackberry"]  # ["apple", "banana", "blackberry", "cherry"]

# Replace with fewer elements
fruits = ["apple", "banana", "blackberry", "cherry"]
fruits[1:3] = ["blueberry"]  # ["apple", "blueberry", "cherry"]
```

## List Operations

### Concatenation and Repetition

```python
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Concatenation
combined = list1 + list2  # [1, 2, 3, 4, 5, 6]

# Repetition
repeated = list1 * 3  # [1, 2, 3, 1, 2, 3, 1, 2, 3]
```

### Checking Membership

```python
fruits = ["apple", "banana", "cherry"]

# Check if an element is in the list
"banana" in fruits  # True
"mango" in fruits   # False
"mango" not in fruits  # True
```

### List Methods for Sorting and Reversing

```python
numbers = [3, 1, 4, 1, 5, 9, 2]

# Sort the list in-place
numbers.sort()  # [1, 1, 2, 3, 4, 5, 9]

# Sort in descending order
numbers.sort(reverse=True)  # [9, 5, 4, 3, 2, 1, 1]

# Sort with a custom key function
words = ["apple", "Banana", "cherry"]
words.sort()  # ["Banana", "apple", "cherry"] (uppercase comes before lowercase)
words.sort(key=str.lower)  # ["apple", "Banana", "cherry"] (case-insensitive sort)

# Create a new sorted list without modifying the original
numbers = [3, 1, 4, 1, 5, 9, 2]
sorted_numbers = sorted(numbers)  # sorted_numbers = [1, 1, 2, 3, 4, 5, 9], numbers unchanged
desc_numbers = sorted(numbers, reverse=True)  # [9, 5, 4, 3, 2, 1, 1]

# Reverse the list in-place
numbers.reverse()  # [2, 9, 5, 1, 4, 1, 3]

# Create a reversed iterator without modifying the original
numbers = [1, 2, 3, 4, 5]
rev_iter = reversed(numbers)  # returns an iterator
rev_list = list(rev_iter)  # rev_list = [5, 4, 3, 2, 1], numbers unchanged
```

### Finding Elements

```python
fruits = ["apple", "banana", "cherry", "banana", "elderberry"]

# Find the index of the first occurrence
banana_index = fruits.index("banana")  # 1

# Find with a start and end range
banana_index = fruits.index("banana", 2)  # 3 (search starts from index 2)
banana_index = fruits.index("banana", 2, 4)  # 3 (search from index 2 up to index 4)

# Count occurrences
banana_count = fruits.count("banana")  # 2
```

### Common Operations with Lists

```python
numbers = [1, 2, 3, 4, 5]

# Length
length = len(numbers)  # 5

# Min and max values
min_value = min(numbers)  # 1
max_value = max(numbers)  # 5

# Sum of all elements
total = sum(numbers)  # 15

# Sum with a start value
total = sum(numbers, 10)  # 25 (10 + 1 + 2 + 3 + 4 + 5)

# Any and all
has_any_even = any(x % 2 == 0 for x in numbers)  # True
all_positive = all(x > 0 for x in numbers)  # True
```

## List Iteration

### Forward Iteration

```python
fruits = ["apple", "banana", "cherry", "date"]

# Using a for loop (simplest approach)
for fruit in fruits:
    print(fruit)

# With index using enumerate
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")  # "0: apple", "1: banana", etc.

# Using range and index
for i in range(len(fruits)):
    print(fruits[i])
```

### Reverse Iteration

There are several ways to iterate through a list in reverse order:

```python
fruits = ["apple", "banana", "cherry", "date"]

# Method 1: Using reversed() function
# Creates an iterator that accesses the list in reverse order
# Most Pythonic and generally preferred approach
for fruit in reversed(fruits):
    print(fruit)  # "date", "cherry", "banana", "apple"

# Method 2: Using negative indexing with range
# Explicitly calculates each index in reverse
for i in range(len(fruits)-1, -1, -1):
    print(fruits[i])  # "date", "cherry", "banana", "apple"

# Method 3: Using a reversed slice
# Creates a new reversed list in memory
for fruit in fruits[::-1]:
    print(fruit)  # "date", "cherry", "banana", "apple"

# Method 4: Using a while loop with decreasing index
# Rarely used but shows explicit index manipulation
i = len(fruits) - 1
while i >= 0:
    print(fruits[i])  # "date", "cherry", "banana", "apple"
    i -= 1

# Method 5: With index using enumerate and reversed
for i, fruit in enumerate(reversed(fruits)):
    print(f"{len(fruits)-1-i}: {fruit}")  # "3: date", "2: cherry", etc.
```

### Performance and Use Case Comparison

```python
# For most cases, choose based on what you need:

# 1. reversed(): Best for simple iteration
# - Memory efficient (doesn't create a copy)
# - Clean and idiomatic Python
# - Use when you just need to process items in reverse

for item in reversed(my_list):
    process(item)

# 2. Range with negative indices: Best when you need precise index control
# - Slightly more verbose
# - Gives you the exact reverse position
# - Use when you need the reverse index for calculations

for i in range(len(my_list)-1, -1, -1):
    process(my_list[i], i)

# 3. Slicing with [::-1]: Best when you need the reversed list for further operations
# - Creates a new list in memory (higher memory usage)
# - Convenient when you need the reversed list for multiple operations
# - Avoid for very large lists if memory is a concern

reversed_list = my_list[::-1]
for item in reversed_list:
    process(item)
# You can continue using reversed_list after the loop

# 4. While loop: Rarely needed
# - Most verbose and least Pythonic
# - Useful only in specific scenarios where you need complex index manipulation
# - Generally avoid unless you have a specific reason

# 5. Reversed with enumerate: Best when you need both item and original position
# - Slightly more complex but very versatile
# - Great for when position matters in reverse order

for i, item in enumerate(reversed(my_list)):
    original_index = len(my_list) - 1 - i
    process(item, original_index)
```

### Iterating Through Multiple Lists

```python
# Zip multiple lists (parallel iteration)
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Zip with different length lists (stops at shortest)
numbers = [1, 2]
letters = ["a", "b", "c"]
for num, letter in zip(numbers, letters):
    print(num, letter)  # Only prints "1 a", "2 b"

# Use zip_longest from itertools for different length lists
from itertools import zip_longest
for num, letter in zip_longest(numbers, letters, fillvalue=0):
    print(num, letter)  # "1 a", "2 b", "0 c"

# Nested iteration
matrix = [[1, 2, 3], [4, 5, 6]]
for row in matrix:
    for element in row:
        print(element)  # 1, 2, 3, 4, 5, 6
```

### Functions Similar to zip() for List Operations

Python's standard library offers several functions that, like `zip()`, help with sophisticated list operations:

```python
from itertools import *

# 1. enumerate() - Adds counter to an iterable
for i, item in enumerate(["a", "b", "c"]):
    print(f"{i}: {item}")  # "0: a", "1: b", "2: c"

# Start counting from a specific number
for i, item in enumerate(["a", "b", "c"], start=1):
    print(f"{i}: {item}")  # "1: a", "2: b", "3: c"

# 2. zip_longest() - Like zip but doesn't stop at the shortest iterable
list1 = [1, 2]
list2 = ["a", "b", "c"]
for pair in zip_longest(list1, list2, fillvalue=0):
    print(pair)  # (1, 'a'), (2, 'b'), (0, 'c')

# 3. chain() - Combines multiple iterables sequentially
for item in chain([1, 2], [3, 4], [5, 6]):
    print(item)  # 1, 2, 3, 4, 5, 6

# 4. product() - Cartesian product of iterables (all combinations)
for pair in product([1, 2], ["a", "b"]):
    print(pair)  # (1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')

# 5. combinations() - All possible r-length combinations
for combo in combinations([1, 2, 3, 4], 2):
    print(combo)  # (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)

# 6. permutations() - All possible r-length orderings
for perm in permutations([1, 2, 3], 2):
    print(perm)  # (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)

# 7. groupby() - Groups consecutive items by a key function
animals = ["duck", "dog", "deer", "cat", "cow"]
# Must be sorted first for groupby to work as expected
animals.sort(key=lambda x: x[0])  # Sort by first letter
for key, group in groupby(animals, key=lambda x: x[0]):
    print(key, list(group))  # 'c' ['cat', 'cow'], 'd' ['deer', 'dog', 'duck']

# 8. islice() - Like slice notation but for any iterable
for item in islice(range(10), 2, 8, 2):
    print(item)  # 2, 4, 6

# 9. map() - Apply a function to each item in one or more iterables
for item in map(lambda x, y: x + y, [1, 2, 3], [10, 20, 30]):
    print(item)  # 11, 22, 33

# 10. filter() - Keep only items that pass a test function
for item in filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]):
    print(item)  # 2, 4, 6

# 11. starmap() - Apply function using arguments unpacked from each iterable
for item in starmap(pow, [(2, 3), (4, 2), (10, 3)]):
    print(item)  # 8, 16, 1000
```

### Combining Iteration Functions for Advanced Operations

These functions can be composed to create powerful data processing pipelines:

```python
# Example 1: Process pairs of adjacent items in a list
numbers = [1, 2, 3, 4, 5]
adjacent_pairs = list(zip(numbers, numbers[1:]))
# [(1, 2), (2, 3), (3, 4), (4, 5)]

# Example 2: Create a sliding window of a specified size
def sliding_window(iterable, size):
    """Create a sliding window of `size` elements over the iterable."""
    iterables = tee(iterable, size)
    return zip(*[islice(it, i, None) for i, it in enumerate(iterables)])

list(sliding_window([1, 2, 3, 4, 5, 6], 3))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)]

# Example 3: Group items with a specific property together
data = [
    {"name": "Alice", "role": "developer"},
    {"name": "Bob", "role": "manager"},
    {"name": "Charlie", "role": "developer"}
]

from operator import itemgetter
# Sort by role first (groupby requires sorted data)
data.sort(key=itemgetter("role"))
for role, group in groupby(data, key=itemgetter("role")):
    print(f"{role}: {[person['name'] for person in group]}")
# developer: ['Alice', 'Charlie']
# manager: ['Bob']

# Example 4: Filter and transform data in one pipeline
import itertools as it
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(map(lambda x: x**2, 
                 filter(lambda x: x % 2 == 0, numbers)))
# [4, 16, 36, 64, 100]

# Same operation with list comprehension (usually more readable)
result = [x**2 for x in numbers if x % 2 == 0]
```

## List Comprehensions

```python
# Basic syntax: [expression for item in iterable if condition]

# Transform elements
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # [1, 4, 9, 16, 25]

# Filter elements
even_numbers = [x for x in numbers if x % 2 == 0]  # [2, 4]

# Both transform and filter
even_squares = [x**2 for x in numbers if x % 2 == 0]  # [4, 16]

# Nested loops
pairs = [(x, y) for x in [1, 2] for y in [3, 4]]
# [(1, 3), (1, 4), (2, 3), (2, 4)]

# Conditional expressions (ternary)
values = [1, -2, 3, -4, 5]
abs_values = [x if x > 0 else -x for x in values]  # [1, 2, 3, 4, 5]
```

## Nested Lists and Matrices

```python
# Creating a nested list
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Accessing elements
top_left = matrix[0][0]  # 1
middle = matrix[1][1]    # 5
bottom_right = matrix[2][2]  # 9

# Modifying elements
matrix[0][1] = 20  # [[1, 20, 3], [4, 5, 6], [7, 8, 9]]

# Creating a matrix with list comprehension
matrix = [[i * 3 + j + 1 for j in range(3)] for i in range(3)]
# [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flattening a nested list
flat = [x for sublist in matrix for x in sublist]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Transpose a matrix (convert rows to columns)
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

## Copying Lists

```python
original = [1, 2, [3, 4]]

# Shallow copy (copies references to nested objects)
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

# Changing a nested list in a shallow copy
copy1[2][0] = 30  # This also affects original and other copies
# original = [1, 2, [30, 4]]
# copy1 = [1, 2, [30, 4]]
# copy2 = [1, 2, [30, 4]]

# Deep copy (completely independent copy)
import copy
deep_copy = copy.deepcopy(original)
deep_copy[2][0] = 100  # Only affects deep_copy
# deep_copy = [1, 2, [100, 4]]
# original = [1, 2, [30, 4]]
```

## Advanced List Techniques

### List Slicing Tricks

```python
numbers = [1, 2, 3, 4, 5]

# Reverse a list with slicing (creates a new list)
reversed_list = numbers[::-1]  # [5, 4, 3, 2, 1]

# Create a shallow copy with slicing
copy_list = numbers[:]    # [1, 2, 3, 4, 5]
copy_list2 = numbers[::]  # [1, 2, 3, 4, 5] (same as [:])

# Verifying that slicing creates shallow copies, not deep copies
nested = [[1, 2], [3, 4]]
sliced_copy = nested[:]    # Creates a shallow copy
sliced_copy2 = nested[::]  # Also creates a shallow copy (identical to [:])

# Proof 1: Modifying nested elements in the original affects all shallow copies
print("Original nested list:", nested)              # [[1, 2], [3, 4]]
print("Shallow copy before modification:", sliced_copy)  # [[1, 2], [3, 4]]

nested[0][0] = 99  # Modify a nested element in the original
print("Original after modification:", nested)            # [[99, 2], [3, 4]]
print("Shallow copy after modification:", sliced_copy)   # [[99, 2], [3, 4]] - nested elements are shared
print("Shallow copy2 after modification:", sliced_copy2) # [[99, 2], [3, 4]] - same behavior with [::]

# Proof 2: Using 'is' to check if nested objects are the same objects in memory
print(nested[0] is sliced_copy[0])  # True - they reference the same object
print(nested[1] is sliced_copy[1])  # True - they reference the same object

# Contrast with a deep copy
import copy
deep_copy = copy.deepcopy(nested)
nested[0][1] = 88
print("Original after second modification:", nested)     # [[99, 88], [3, 4]]
print("Shallow copy after second mod:", sliced_copy)     # [[99, 88], [3, 4]] - affected by the change
print("Deep copy after second mod:", deep_copy)          # [[99, 2], [3, 4]] - not affected by the change

# Proof that deep copy creates different objects
print(nested[0] is deep_copy[0])  # False - they are different objects
print(nested[1] is deep_copy[1])  # False - they are different objects

# Important: Shallow vs. Deep Copy with Immutable Types
numbers = [1, 2, 3, 4, 5]  # List of immutable integers
shallow_copy = numbers[:]
deep_copy = copy.deepcopy(numbers)

# For lists containing only immutable types, shallow and deep copies behave the same
numbers[0] = 99
print("Original after modification:", numbers)        # [99, 2, 3, 4, 5]
print("Shallow copy after modification:", shallow_copy)  # [1, 2, 3, 4, 5] - unaffected
print("Deep copy after modification:", deep_copy)        # [1, 2, 3, 4, 5] - unaffected

# Why? Immutable objects cannot be changed in-place
# So even though shallow copies share references to the same immutable objects,
# when you modify the list, you're replacing the objects, not modifying them
strings = ["hello", "world"]
strings_shallow = strings[:]
strings[0] = "goodbye"  # This replaces the string, not modifies it
print(strings)          # ["goodbye", "world"]
print(strings_shallow)  # ["hello", "world"] - unaffected

# This distinction only matters with mutable types (lists, dicts, custom objects, etc.)
# For immutable types, shallow copies are sufficient and more efficient

# For a true deep copy, use the copy module
import copy
deep_copy = copy.deepcopy(nested)
nested[0][1] = 88
print(nested)      # [[99, 88], [3, 4]]
print(deep_copy)   # [[99, 2], [3, 4]] - changes in original don't affect deep copy

# Get every nth element
every_second = numbers[::2]  # [1, 3, 5]
every_third = numbers[::3]   # [1, 4]

# Reverse every nth element
reverse_every_second = numbers[::-2]  # [5, 3, 1]

# Partial slice with step
middle_reversed = numbers[3:0:-1]  # [4, 3, 2]

# Replace a slice
numbers[1:4] = [20, 30, 40]  # [1, 20, 30, 40, 5]

# Delete a slice
numbers = [1, 2, 3, 4, 5]
numbers[1:3] = []  # [1, 4, 5]

# Insert without replacing
numbers = [1, 2, 3]
numbers[1:1] = [10, 11]  # [1, 10, 11, 2, 3]
```

### Using zip() with Lists

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

# Combine multiple lists element-wise
combined = list(zip(names, ages))
# [('Alice', 25), ('Bob', 30), ('Charlie', 35)]

# Unzip a list of tuples
names, ages = zip(*combined)
# names = ('Alice', 'Bob', 'Charlie')
# ages = (25, 30, 35)

# Iterate over multiple lists simultaneously
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# Create a dictionary from two lists
name_to_age = dict(zip(names, ages))
# {'Alice': 25, 'Bob': 30, 'Charlie': 35}
```

### List as a Stack and Queue

```python
# Using a list as a stack (last-in, first-out)
stack = []
stack.append(1)  # Add to top: [1]
stack.append(2)  # Add to top: [1, 2]
stack.append(3)  # Add to top: [1, 2, 3]
top_item = stack.pop()  # top_item = 3, stack = [1, 2]

# Using a list as a queue (first-in, first-out) - inefficient for large lists
queue = []
queue.append(1)  # Add to end: [1]
queue.append(2)  # Add to end: [1, 2]
queue.append(3)  # Add to end: [1, 2, 3]
first_item = queue.pop(0)  # first_item = 1, queue = [2, 3]
# Note: For efficient queues, use collections.deque instead
```

### List Unpacking

List unpacking (also called sequence unpacking) allows you to assign multiple variables from the values in a list or other iterable in a single operation. Let's explore how it works:

```python
# Basic unpacking
first, second, third = [1, 2, 3]
# first = 1, second = 2, third = 3

# How unpacking works behind the scenes:
# 1. Python sees multiple targets on the left side of =
# 2. It evaluates the expression on the right side ([1, 2, 3])
# 3. It checks if the number of targets matches the number of values
# 4. It assigns each value to its corresponding target variable

# Must have exactly the same number of variables as elements
# This raises ValueError: too many values to unpack
# a, b = [1, 2, 3]

# This also raises ValueError: not enough values to unpack
# a, b, c, d = [1, 2, 3]

# Unpacking with * (rest/starred unpacking)
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

# The * operator collects "the rest" of the values into a list
# It can appear anywhere in the unpacking:
head, *middle, tail = [1, 2, 3, 4, 5]
# head = 1, middle = [2, 3, 4], tail = 5

*start, end = [1, 2, 3]
# start = [1, 2], end = 3

# Only one starred expression is allowed in an assignment
# This raises SyntaxError:
# *start, *end = [1, 2, 3, 4]

# Ignoring values with _
first, *_, last = [1, 2, 3, 4, 5]
# first = 1, last = 5, middle values collected but ignored
# Using _ is a convention indicating the value won't be used

# Unpacking nested structures
(a, b), (c, d) = [(1, 2), (3, 4)]
# a = 1, b = 2, c = 3, d = 4

# Unpacking in for loops
points = [(1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"Point: ({x}, {y})")

# Swapping values (a classic Python idiom)
a, b = 1, 2
a, b = b, a  # a = 2, b = 1
# This works because the right side is evaluated first as a tuple (2, 1),
# then unpacked into the variables on the left

# Unpacking and functions
def get_coordinates():
    return (3, 4)  # Returns a tuple

x, y = get_coordinates()  # Unpacks the returned tuple
# x = 3, y = 4

# Merging lists with unpacking (Python 3.5+)
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]  # [1, 2, 3, 4, 5, 6]

# Can combine with normal elements
combined = [0, *list1, 3.5, *list2, 7]  # [0, 1, 2, 3, 3.5, 4, 5, 6, 7]

# Works with any iterable on the right side
combined = [*list1, *"abc"]  # [1, 2, 3, 'a', 'b', 'c']

# Unpacking dictionaries (with ** operator)
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
combined_dict = {**dict1, **dict2}  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# In function calls
numbers = [1, 2, 3]
print(*numbers)  # Equivalent to print(1, 2, 3)

# Extended unpacking in function calls with keywords
point = {"x": 1, "y": 2}
draw_point(**point)  # Equivalent to draw_point(x=1, y=2)
```

#### How Unpacking Differs from Indexing

Unpacking offers several advantages over accessing list elements by index:

```python
items = [1, 2, 3]

# Using indexing
first = items[0]
second = items[1]
third = items[2]

# Using unpacking
first, second, third = items

# Unpacking is more concise and clearly communicates intent
# It also validates the expected structure - unpacking will fail
# if the list doesn't have exactly the expected number of elements

# With extended unpacking, we get even more flexibility
first, *rest = items  # Adapts to lists of different lengths
```

#### Connection to *args and **kwargs in Functions

Unpacking is closely related to how `*args` and `**kwargs` work in Python functions. The same unpacking mechanisms are at play, just in different contexts:

```python
# Regular unpacking in assignment
a, *b = [1, 2, 3, 4]  # a = 1, b = [2, 3, 4]

# *args in function definition collects positional arguments into a tuple
def print_all(*args):
    print(f"You passed {len(args)} arguments: {args}")
    # args is a tuple containing all positional arguments

print_all(1, 2, 3)  # You passed 3 arguments: (1, 2, 3)

# The * in *args is the same concept as in unpacking, but:
# - In assignment (a, *b = ...), * collects values into a list
# - In function params (*args), * collects arguments into a tuple

# Unpacking in function calls (the inverse of *args)
numbers = [1, 2, 3]
print_all(*numbers)  # Unpacks the list into separate arguments
                    # Equivalent to print_all(1, 2, 3)

# **kwargs collects keyword arguments into a dictionary
def user_info(**kwargs):
    print(f"User information: {kwargs}")
    # kwargs is a dictionary containing all keyword arguments

user_info(name="Alice", age=30, city="New York")
# User information: {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Dictionary unpacking in function calls (the inverse of **kwargs)
user_data = {"name": "Bob", "age": 25, "city": "Boston"}
user_info(**user_data)  # Unpacks the dictionary into keyword arguments
                       # Equivalent to user_info(name="Bob", age=25, city="Boston")

# Combining *args and **kwargs gives maximum flexibility
def flexible_function(*args, **kwargs):
    print(f"Positional args: {args}")
    print(f"Keyword args: {kwargs}")

flexible_function(1, 2, 3, name="Alice", age=30)
# Positional args: (1, 2, 3)
# Keyword args: {'name': 'Alice', 'age': 30}

# Real-world example: Wrapper functions that pass through arguments
def log_and_call(func, *args, **kwargs):
    print(f"Calling {func.__name__} with {args} and {kwargs}")
    return func(*args, **kwargs)

def add(a, b):
    return a + b

result = log_and_call(add, 5, 3)
# Calling add with (5, 3) and {}
# result = 8
```

This symmetry in Python's design makes the language very consistent:
- When defining functions: `*args` and `**kwargs` collect multiple arguments
- When calling functions: `*iterable` and `**dict` unpack collections into arguments
- In assignments: `*variable` collects multiple values

#### Behind the Scenes of Star Unpacking

The `*` operator in unpacking works by:
1. Collecting all "extra" items not assigned to regular variables
2. Creating a new list with those items
3. Assigning that list to the starred variable

If there are no "extra" items for the starred variable, it gets an empty list:

```python
a, *b, c = [1, 2]  # a = 1, b = [], c = 2
```

### Filtering and Transforming with map() and filter()

```python
numbers = [1, 2, 3, 4, 5]

# Map: Apply a function to each element
squares = list(map(lambda x: x**2, numbers))
# [1, 4, 9, 16, 25]

# Filter: Keep elements that satisfy a condition
even = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4]

# Combining map and filter
even_squares = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
# [4, 16]

# List comprehension equivalents (generally more readable)
squares = [x**2 for x in numbers]
even = [x for x in numbers if x % 2 == 0]
even_squares = [x**2 for x in numbers if x % 2 == 0]
```

## Performance Considerations

1. **Appending vs. Prepending**:
   - Appending to a list with `append()` is O(1) (constant time)
   - Prepending with `insert(0, item)` is O(n) (linear time)
   - For frequent prepends, consider using `collections.deque`

2. **List Comprehensions**:
   - Generally faster than equivalent for loops
   - More memory-efficient than building a list with multiple `append()` calls

3. **Copying**:
   - Slicing `[:]` and `copy()` create shallow copies (faster but share nested objects)
   - `copy.deepcopy()` creates independent copies (slower but safer for nested structures)

4. **Searching**:
   - `x in my_list` is O(n) - must check each element
   - For frequent lookups, consider using a set or dictionary instead

5. **Sorting**:
   - `sort()` is in-place and modifies the original list
   - `sorted()` creates a new list and leaves the original unchanged
   - Both use Timsort algorithm with O(n log n) time complexity

6. **Concatenation**:
   - `+` creates a new list, which can be inefficient for repeated operations
   - `extend()` or `+=` modifies in-place and is more efficient for repeated operations

## Common Patterns and Recipes

### Removing Duplicates While Preserving Order

```python
def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Usage
unique = remove_duplicates([1, 2, 3, 1, 2, 4, 5])  # [1, 2, 3, 4, 5]

# One-liner using dict.fromkeys() (Python 3.6+ preserves order)
unique = list(dict.fromkeys([1, 2, 3, 1, 2, 4, 5]))  # [1, 2, 3, 4, 5]
```

### Counting Occurrences

```python
from collections import Counter

items = ["apple", "banana", "apple", "orange", "banana", "apple"]

# Using Counter
counts = Counter(items)
# Counter({'apple': 3, 'banana': 2, 'orange': 1})

# Most common elements
most_common = counts.most_common(2)  # [('apple', 3), ('banana', 2)]

# Manual counting with dictionary
count_dict = {}
for item in items:
    count_dict[item] = count_dict.get(item, 0) + 1
# {'apple': 3, 'banana': 2, 'orange': 1}
```

### Grouping Items

```python
from itertools import groupby
from operator import itemgetter

# Grouping sorted data
data = [
    {"name": "Alice", "department": "HR"},
    {"name": "Bob", "department": "IT"},
    {"name": "Charlie", "department": "HR"},
    {"name": "David", "department": "IT"},
]

# Data must be sorted by the grouping key
data.sort(key=itemgetter("department"))

# Group by department
for department, group in groupby(data, key=itemgetter("department")):
    print(f"{department}: {list(group)}")
# HR: [{'name': 'Alice', 'department': 'HR'}, {'name': 'Charlie', 'department': 'HR'}]
# IT: [{'name': 'Bob', 'department': 'IT'}, {'name': 'David', 'department': 'IT'}]

# Using defaultdict (no sorting required)
from collections import defaultdict

groups = defaultdict(list)
for item in data:
    groups[item["department"]].append(item)

for department, members in groups.items():
    print(f"{department}: {members}")
```

### Finding Indices of All Occurrences

```python
def find_all_indices(lst, value):
    return [i for i, x in enumerate(lst) if x == value]

# Usage
indices = find_all_indices([1, 2, 3, 1, 2, 1], 1)  # [0, 3, 5]
```

### Chunking a List

```python
def chunk_list(lst, chunk_size):
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

# Usage
chunks = chunk_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
# [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
```

### Rotating a List

```python
def rotate_list(lst, k):
    """Rotate a list k positions to the right."""
    if not lst:
        return lst
    k = k % len(lst)  # Handle cases where k > len(lst)
    return lst[-k:] + lst[:-k]

# Usage
rotated = rotate_list([1, 2, 3, 4, 5], 2)  # [4, 5, 1, 2, 3]
```

## Interacting with Other Data Structures

### Converting Between Lists and Other Data Types

```python
# List to string
items = ["a", "b", "c"]
joined = "".join(items)  # "abc"
joined_comma = ", ".join(items)  # "a, b, c"

# String to list
text = "apple,banana,cherry"
items = text.split(",")  # ["apple", "banana", "cherry"]

# List to tuple
tuple_items = tuple([1, 2, 3])  # (1, 2, 3)

# List to set (removes duplicates)
unique_items = set([1, 2, 2, 3, 3, 3])  # {1, 2, 3}

# List to dictionary
keys = ["a", "b", "c"]
values = [1, 2, 3]
dictionary = dict(zip(keys, values))  # {"a": 1, "b": 2, "c": 3}
```

### Working with CSV Data

```python
import csv

# Writing a list to a CSV file
data = [
    ["Name", "Age", "City"],
    ["Alice", 25, "New York"],
    ["Bob", 30, "Los Angeles"],
    ["Charlie", 35, "Chicago"]
]

with open("people.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Reading a CSV file into a list
rows = []
with open("people.csv", "r", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)
```

## Appendix: List Methods Summary

Here's a quick reference of all list methods:

| Method | Description | Example |
|--------|-------------|---------|
| `append(x)` | Add item to the end | `lst.append(5)` |
| `extend(iterable)` | Add items from iterable to the end | `lst.extend([5, 6])` |
| `insert(i, x)` | Insert item at position | `lst.insert(0, 'start')` |
| `remove(x)` | Remove first occurrence of value | `lst.remove(5)` |
| `pop([i])` | Remove & return item at position (default: last) | `lst.pop()`, `lst.pop(0)` |
| `clear()` | Remove all items | `lst.clear()` |
| `index(x[, start[, end]])` | Return first index of value | `lst.index(5)` |
| `count(x)` | Count occurrences of value | `lst.count(5)` |
| `sort(*, key=None, reverse=False)` | Sort in-place | `lst.sort()` |
| `reverse()` | Reverse in-place | `lst.reverse()` |
| `copy()` | Return a shallow copy | `lst.copy()` |
