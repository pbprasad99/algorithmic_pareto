# Python Sets Cheatsheet

Sets are unordered collections of unique elements in Python. They offer powerful operations for mathematical set operations like unions, intersections, and differences. This cheatsheet covers all essential set operations and methods with clear examples.

## Creating Sets

```python
# Empty set (cannot use {} as that creates an empty dictionary)
empty_set = set()

# Set with initial values
colors = {"red", "green", "blue"}

# From other iterables
numbers = set([1, 2, 3, 2, 1])  # {1, 2, 3} (duplicates removed)
letters = set("hello")  # {'h', 'e', 'l', 'o'} (only unique letters)

# Set comprehension
even_numbers = {x for x in range(10) if x % 2 == 0}  # {0, 2, 4, 6, 8}
```

## Basic Operations

### Adding Elements

```python
fruits = {"apple", "banana"}

# Add a single element
fruits.add("orange")  # {"apple", "banana", "orange"}

# Adding a duplicate has no effect
fruits.add("apple")  # Still {"apple", "banana", "orange"}

# Add multiple elements
fruits.update(["mango", "grape"])  # {"apple", "banana", "orange", "mango", "grape"}
fruits.update(("pear", "kiwi"), {"plum", "peach"})  # Can update from multiple iterables
```

### Removing Elements

```python
colors = {"red", "green", "blue", "yellow"}

# remove() - raises KeyError if element doesn't exist
colors.remove("green")  # {"red", "blue", "yellow"}

# discard() - no error if element doesn't exist
colors.discard("purple")  # No change, no error
colors.discard("yellow")  # {"red", "blue"}

# pop() - removes and returns an arbitrary element
item = colors.pop()  # Could be "red" or "blue"

# clear() - removes all elements
colors.clear()  # set() (empty set)
```

### Checking Membership

```python
fruits = {"apple", "banana", "orange"}

# Using 'in' operator
"apple" in fruits  # True
"mango" in fruits  # False
"mango" not in fruits  # True

# Checking if set is empty
bool(fruits)  # True if not empty, False if empty
len(fruits) == 0  # True if empty
```

## Set Methods vs. Operators

Python sets provide both methods and overloaded operators for set operations. Here's a comparison:

| Operation | Method | Operator | Description |
|-----------|--------|----------|-------------|
| Union | `a.union(b, ...)` | `a \| b \| ...` | Elements in either set |
| Intersection | `a.intersection(b, ...)` | `a & b & ...` | Elements in all sets |
| Difference | `a.difference(b, ...)` | `a - b - ...` | Elements in `a` but not in others |
| Symmetric Difference | `a.symmetric_difference(b)` | `a ^ b` | Elements in either set but not in both |
| Subset | `a.issubset(b)` | `a <= b` | True if all elements of `a` are in `b` |
| Proper Subset | `a < b` | True if `a` is a subset of `b` and `a != b` |
| Superset | `a.issuperset(b)` | `a >= b` | True if all elements of `b` are in `a` |
| Proper Superset | `a > b` | True if `a` is a superset of `b` and `a != b` |
| Disjoint | `a.isdisjoint(b)` | | True if `a` and `b` have no elements in common |

## Set Operations with Methods

### Union

```python
a = {1, 2, 3}
b = {3, 4, 5}
c = {5, 6, 7}

# Union of two sets
a.union(b)  # {1, 2, 3, 4, 5}

# Union of multiple sets
a.union(b, c)  # {1, 2, 3, 4, 5, 6, 7}

# In-place union (modifies a)
a.update(b)  # a is now {1, 2, 3, 4, 5}
```

### Intersection

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
c = {4, 5, 6, 7}

# Intersection of two sets
a.intersection(b)  # {3, 4}

# Intersection of multiple sets
a.intersection(b, c)  # {4}

# In-place intersection (modifies a)
a.intersection_update(b)  # a is now {3, 4}
```

### Difference

```python
a = {1, 2, 3, 4, 5}
b = {4, 5, 6}
c = {4, 7}

# Difference between two sets
a.difference(b)  # {1, 2, 3}

# Difference between multiple sets
a.difference(b, c)  # {1, 2, 3}

# In-place difference (modifies a)
a.difference_update(b)  # a is now {1, 2, 3}
```

### Symmetric Difference

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Symmetric difference (elements in either set but not in both)
a.symmetric_difference(b)  # {1, 2, 5, 6}

# In-place symmetric difference (modifies a)
a.symmetric_difference_update(b)  # a is now {1, 2, 5, 6}
```

### Subset, Superset, and Disjoint Tests

```python
a = {1, 2}
b = {1, 2, 3, 4}
c = {5, 6}

# Subset
a.issubset(b)  # True (all elements of a are in b)
b.issubset(a)  # False

# Superset
b.issuperset(a)  # True (all elements of a are in b)
a.issuperset(b)  # False

# Disjoint (no common elements)
a.isdisjoint(c)  # True (a and c have no common elements)
a.isdisjoint(b)  # False (a and b share elements)
```

## Set Operations with Operators

### Union with |

```python
a = {1, 2, 3}
b = {3, 4, 5}
c = {5, 6, 7}

# Union using the | operator
a | b  # {1, 2, 3, 4, 5}

# Union of multiple sets
a | b | c  # {1, 2, 3, 4, 5, 6, 7}

# In-place union using |=
a |= b  # a is now {1, 2, 3, 4, 5}
```

### Intersection with &

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
c = {4, 5, 6, 7}

# Intersection using the & operator
a & b  # {3, 4}

# Intersection of multiple sets
a & b & c  # {4}

# In-place intersection using &=
a &= b  # a is now {3, 4}
```

### Difference with -

```python
a = {1, 2, 3, 4, 5}
b = {4, 5, 6}
c = {4, 7}

# Difference using the - operator
a - b  # {1, 2, 3}

# Difference of multiple sets
a - b - c  # {1, 2, 3}

# In-place difference using -=
a -= b  # a is now {1, 2, 3}
```

### Symmetric Difference with ^

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Symmetric difference using the ^ operator
a ^ b  # {1, 2, 5, 6}

# In-place symmetric difference using ^=
a ^= b  # a is now {1, 2, 5, 6}
```

### Comparison Operators

```python
a = {1, 2}
b = {1, 2, 3, 4}
c = {1, 2}

# Subset
a <= b  # True (a is a subset of b)
a < b   # True (a is a proper subset of b)
a <= c  # True (a is a subset of c)
a < c   # False (a equals c, not a proper subset)

# Superset
b >= a  # True (b is a superset of a)
b > a   # True (b is a proper superset of a)
c >= a  # True (c is a superset of a)
c > a   # False (c equals a, not a proper superset)

# Equality
a == c  # True (a and c contain the same elements)
a != b  # True (a and b are different)
```

## Other Useful Set Methods

### copy()

```python
a = {1, 2, 3}
b = a.copy()  # Creates a new set with the same elements

# Changes to b don't affect a
b.add(4)  # b is now {1, 2, 3, 4}, a is still {1, 2, 3}
```

### Immutable Sets (frozenset)

```python
# Regular sets are mutable and can't be used as dictionary keys
regular_set = {1, 2, 3}

# Frozensets are immutable (can't be changed after creation)
frozen = frozenset([1, 2, 3])

# This works
dictionary = {frozen: "This is a valid key"}

# This raises TypeError
# dictionary = {regular_set: "This will fail"}

# Frozensets support the same operations as regular sets,
# except methods that modify the set
result = frozen.union({4, 5})  # Creates a new frozenset
# frozen.add(4)  # This would raise an AttributeError
```

## Practical Examples

### Removing Duplicates

```python
# Remove duplicates from a list while preserving order
def remove_duplicates(items):
    return list(dict.fromkeys(items))

# Alternative with sets (doesn't preserve order)
def remove_duplicates_set(items):
    return list(set(items))

items = [3, 1, 2, 1, 3, 4, 2]
remove_duplicates(items)      # [3, 1, 2, 4]
remove_duplicates_set(items)  # Order not guaranteed
```

### Finding Common and Unique Elements

```python
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]

# Find elements in both lists
common = set(list1) & set(list2)  # {4, 5}

# Find elements unique to first list
only_in_list1 = set(list1) - set(list2)  # {1, 2, 3}

# Find elements unique to second list
only_in_list2 = set(list2) - set(list1)  # {6, 7, 8}

# Find elements in either list but not both
symmetric_diff = set(list1) ^ set(list2)  # {1, 2, 3, 6, 7, 8}

# Union (all unique elements from both lists)
all_elements = set(list1) | set(list2)  # {1, 2, 3, 4, 5, 6, 7, 8}
```

### Set Operations on Strings

```python
string1 = "hello"
string2 = "world"

# Find common characters
common_chars = set(string1) & set(string2)  # {'l', 'o'}

# Find characters unique to first string
only_in_string1 = set(string1) - set(string2)  # {'h', 'e'}

# Find characters unique to second string
only_in_string2 = set(string2) - set(string1)  # {'w', 'r', 'd'}

# All unique characters from both strings
all_chars = set(string1) | set(string2)  # {'h', 'e', 'l', 'o', 'w', 'r', 'd'}
```

### Power Set (All Possible Subsets)

```python
def power_set(s):
    """Return the power set of set s (all possible subsets)"""
    result = [frozenset()]  # Start with the empty set
    for x in s:
        # For each element, add a new subset by including it in each existing subset
        result.extend([subset | {x} for subset in result])
    return result

s = {1, 2, 3}
subsets = power_set(s)
# Returns: [frozenset(), frozenset({1}), frozenset({2}), frozenset({1, 2}), 
#           frozenset({3}), frozenset({1, 3}), frozenset({2, 3}), frozenset({1, 2, 3})]
```

### Grouping Elements

```python
data = [
    {"name": "Alice", "department": "Engineering"},
    {"name": "Bob", "department": "Marketing"},
    {"name": "Charlie", "department": "Engineering"},
    {"name": "Diana", "department": "HR"}
]

# Group employees by department
departments = {}
for employee in data:
    dept = employee["department"]
    if dept not in departments:
        departments[dept] = set()
    departments[dept].add(employee["name"])

# Result: {'Engineering': {'Alice', 'Charlie'}, 'Marketing': {'Bob'}, 'HR': {'Diana'}}
```

## Performance Considerations

1. **Set operations are optimized**:
   Set operations like union, intersection, and difference are highly optimized and often faster than equivalent operations with lists.

2. **Membership testing is O(1)**:
   Checking if an element is in a set (`x in s`) is much faster than checking in a list, especially for large collections.

3. **Sets require hashable elements**:
   Elements in a set must be hashable (immutable). Lists, dictionaries, and other sets cannot be elements of a regular set.

4. **Memory usage**:
   Sets typically use more memory than lists with the same elements due to their hash table implementation.

5. **Set comprehensions**:
   For creating sets from other iterables with transformations, set comprehensions are often more efficient and readable than loops.

## When to Use Sets

Sets are ideal when you need:

1. **Uniqueness**: Automatically eliminate duplicates
2. **Fast membership testing**: Check if elements exist in a collection
3. **Mathematical set operations**: Union, intersection, difference
4. **Removing duplicates** from sequences (though order is not preserved)
5. **Finding common or unique items** between collections

However, sets are not suitable when:
1. You need to maintain order (use lists or OrderedDict)
2. You need to store duplicate elements (use lists)
3. You need to store unhashable objects (use lists)

## Appendix: Understanding Subset and Superset Relationships

This appendix provides a deeper understanding of subset and superset relationships, including the distinction between subset/superset and proper subset/proper superset.

### Subset vs. Proper Subset

#### Subset (⊆)
A set A is a **subset** of set B if **every element** in A is also in B.

Key characteristics:
- Every element of A must be in B
- A and B can be equal (contain the same elements)
- An empty set is a subset of any set
- Every set is a subset of itself

In Python, subset relationship is tested with the `<=` operator or the `issubset()` method:

```python
a = {1, 2}
b = {1, 2, 3, 4}
c = {1, 2}

# Using operators
a <= b  # True (a is a subset of b)
a <= c  # True (a equals c, so a is a subset of c)

# Using methods
a.issubset(b)  # True
a.issubset(c)  # True
```

#### Proper Subset (⊂)
A set A is a **proper subset** of set B if A is a subset of B, but A ≠ B.

Key characteristics:
- Every element of A must be in B
- B must contain at least one element that is not in A
- A and B cannot be equal
- A set is never a proper subset of itself

In Python, proper subset relationship is tested with the `<` operator, but there's no direct method equivalent. You can combine methods to check for proper subset:

```python
a = {1, 2}
b = {1, 2, 3, 4}
c = {1, 2}

# Using operators
a < b  # True (a is a proper subset of b)
a < c  # False (a equals c, so not a proper subset)

# Using methods (combined approach)
a.issubset(b) and a != b  # True
a.issubset(c) and a != c  # False

# Alternative using length
a.issubset(b) and len(a) < len(b)  # True
a.issubset(c) and len(a) < len(c)  # False

# Alternative using set difference
a.issubset(b) and bool(b - a)  # True
a.issubset(c) and bool(c - a)  # False
```

### Superset vs. Proper Superset

#### Superset (⊇)
A set A is a **superset** of set B if **every element** in B is also in A.

Key characteristics:
- Every element of B must be in A
- A and B can be equal
- Any set is a superset of the empty set
- Every set is a superset of itself

In Python, superset relationship is tested with the `>=` operator or the `issuperset()` method:

```python
a = {1, 2, 3, 4}
b = {1, 2}
c = {1, 2, 3, 4}

# Using operators
a >= b  # True (a is a superset of b)
a >= c  # True (a equals c, so a is a superset of c)

# Using methods
a.issuperset(b)  # True
a.issuperset(c)  # True
```

#### Proper Superset (⊃)
A set A is a **proper superset** of set B if A is a superset of B, but A ≠ B.

Key characteristics:
- Every element of B must be in A
- A must contain at least one element that is not in B
- A and B cannot be equal
- A set is never a proper superset of itself

In Python, proper superset relationship is tested with the `>` operator, but there's no direct method equivalent. You can combine methods to check for proper superset:

```python
a = {1, 2, 3, 4}
b = {1, 2}
c = {1, 2, 3, 4}

# Using operators
a > b  # True (a is a proper superset of b)
a > c  # False (a equals c, so not a proper superset)

# Using methods (combined approach)
a.issuperset(b) and a != b  # True
a.issuperset(c) and a != c  # False

# Alternative using length
a.issuperset(b) and len(a) > len(b)  # True
a.issuperset(c) and len(a) > len(c)  # False

# Alternative using set difference
a.issuperset(b) and bool(a - b)  # True
a.issuperset(c) and bool(a - c)  # False
```

### Helper Functions for Proper Subset/Superset Tests

If you need to check for proper subset/superset relationships frequently, you might consider creating helper functions:

```python
def is_proper_subset(a, b):
    """Check if set a is a proper subset of set b."""
    return a.issubset(b) and a != b

def is_proper_superset(a, b):
    """Check if set a is a proper superset of set b."""
    return a.issuperset(b) and a != b

# Usage
a = {1, 2}
b = {1, 2, 3, 4}
print(is_proper_subset(a, b))    # True
print(is_proper_superset(b, a))  # True
```

### Visual Representation

To visualize these relationships:

1. **Subset (A ⊆ B)**:
   - Set A is fully contained within set B
   - The circles representing A and B can be identical

2. **Proper Subset (A ⊂ B)**:
   - Set A is fully contained within set B
   - Set B has additional elements not in A
   - The circles cannot be identical

3. **Superset (A ⊇ B)**:
   - Set A fully contains set B
   - The circles representing A and B can be identical

4. **Proper Superset (A ⊃ B)**:
   - Set A fully contains set B
   - Set A has additional elements not in B
   - The circles cannot be identical

