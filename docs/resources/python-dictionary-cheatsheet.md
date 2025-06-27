# Python Dictionary Methods Cheatsheet

Dictionaries are versatile data structures in Python that store key-value pairs. This cheatsheet covers all essential dictionary methods with clear examples and explanations.

## Creating Dictionaries

There are several ways to create dictionaries in Python:

```python
# Empty dictionary
empty_dict = {}
empty_dict = dict()

# Dictionary with initial values
user = {"name": "John", "age": 30, "is_admin": False}

# Using dict() constructor
user = dict(name="John", age=30, is_admin=False)

# From a list of tuples
user = dict([("name", "John"), ("age", 30), ("is_admin", False)])

# Dictionary comprehension
squares = {x: x*x for x in range(6)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

## Basic Operations

### Accessing Values

```python
user = {"name": "John", "age": 30, "is_admin": False}

# Using square brackets (raises KeyError if key doesn't exist)
name = user["name"]  # "John"

# Using get() (returns None or a default value if key doesn't exist)
age = user.get("age")  # 30
score = user.get("score")  # None
role = user.get("role", "user")  # "user" (default value)
```

### Adding/Updating Items

```python
user = {"name": "John", "age": 30}

# Using square brackets
user["email"] = "john@example.com"  # Adds new key-value pair
user["age"] = 31  # Updates existing value

# Using update() - add/update multiple key-value pairs
user.update({"phone": "555-1234", "age": 32})
user.update(country="USA", zip="10001")
```

### Removing Items

```python
user = {"name": "John", "age": 30, "email": "john@example.com", "phone": "555-1234"}

# pop() - removes item and returns its value
email = user.pop("email")  # Returns "john@example.com" and removes the key-value pair
nonexistent = user.pop("address", "Not found")  # Returns "Not found" (default value)

# popitem() - removes and returns the last inserted key-value pair
last_item = user.popitem()  # Returns ("phone", "555-1234") in Python 3.7+

# del statement - removes specified key
del user["age"]

# clear() - removes all items
user.clear()  # user is now {}
```

## Dictionary Methods

### Copying Dictionaries

```python
original = {"name": "John", "age": 30, "scores": [85, 90, 78]}

# Shallow copy - nested objects are references
shallow_copy = original.copy()
shallow_copy = dict(original)  # Alternative

# Deep copy - completely independent copy
import copy
deep_copy = copy.deepcopy(original)

# Demonstrating the difference
shallow_copy["scores"].append(92)  # Also affects original["scores"]
deep_copy["scores"].append(95)     # Does NOT affect original["scores"]
```

### Getting Keys, Values, and Items

```python
user = {"name": "John", "age": 30, "is_admin": False}

# Get all keys
keys = user.keys()  # dict_keys(['name', 'age', 'is_admin'])

# Get all values
values = user.values()  # dict_values(['John', 30, False])

# Get all key-value pairs as tuples
items = user.items()  # dict_items([('name', 'John'), ('age', 30), ('is_admin', False)])

# These return dynamic view objects that update when the dictionary changes
user["email"] = "john@example.com"
# Now keys contains 'email', values contains 'john@example.com', and items contains the new pair

# Convert to lists if needed
keys_list = list(user.keys())
```

### Checking Dictionary Contents

```python
user = {"name": "John", "age": 30, "is_admin": False}

# Check if key exists
"name" in user  # True
"email" in user  # False
"email" not in user  # True

# Check for a specific value (less efficient, searches all values)
30 in user.values()  # True

# Length of dictionary
len(user)  # 3
```

### Dictionary Merging and Unpacking (Python 3.5+)

```python
# Using update() to merge (modifies the first dictionary)
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
dict1.update(dict2)  # dict1 is now {"a": 1, "b": 3, "c": 4}

# Using unpacking operator ** to merge (creates a new dictionary)
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged = {**dict1, **dict2}  # {"a": 1, "b": 3, "c": 4}

# Python 3.9+ uses the | operator
merged = dict1 | dict2  # {"a": 1, "b": 3, "c": 4}
dict1 |= dict2          # In-place update, equivalent to dict1.update(dict2)
```

### Default Values with setdefault()

```python
user = {"name": "John", "age": 30}

# If key exists, returns its value; otherwise, sets the key to default and returns default
email = user.setdefault("email", "not provided")  # "not provided", adds to dictionary
name = user.setdefault("name", "Unknown")  # "John", doesn't change existing value

# Great for counting occurrences
text = "mississippi"
char_count = {}
for char in text:
    char_count.setdefault(char, 0)
    char_count[char] += 1
# char_count is {'m': 1, 'i': 4, 's': 4, 'p': 2}
```

### Dictionary Iteration

```python
user = {"name": "John", "age": 30, "is_admin": False}

# Iterate over keys (default)
for key in user:
    print(key)  # "name", "age", "is_admin"

# Explicit iterations
for key in user.keys():
    print(key)

for value in user.values():
    print(value)  # "John", 30, False

for key, value in user.items():
    print(f"{key}: {value}")
```

## Advanced Dictionary Features

### Dictionary Comprehensions

```python
# Basic dictionary comprehension
squares = {x: x*x for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# With conditional logic
even_squares = {x: x*x for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Transforming dictionaries
prices = {"apple": 0.75, "banana": 0.5, "orange": 0.8}
cents = {fruit: int(price * 100) for fruit, price in prices.items()}
# {"apple": 75, "banana": 50, "orange": 80}
```

### fromkeys() Method

```python
# Create a dictionary with specified keys and a default value
keys = ["name", "age", "email"]
user = dict.fromkeys(keys, "unknown")
# {"name": "unknown", "age": "unknown", "email": "unknown"}

# Default value is None if not specified
empty_user = dict.fromkeys(keys)
# {"name": None, "age": None, "email": None}
```

### Ordered Dictionaries (Python 3.7+)

As of Python 3.7, regular dictionaries maintain insertion order.

```python
# Dictionaries remember the order in which keys were inserted
colors = {}
colors["red"] = "#FF0000"
colors["green"] = "#00FF00"
colors["blue"] = "#0000FF"

for color in colors:
    print(color)  # Prints "red", "green", "blue" in that order

# For Python 3.6 and earlier, use collections.OrderedDict
from collections import OrderedDict
ordered = OrderedDict([("red", "#FF0000"), ("green", "#00FF00"), ("blue", "#0000FF")])
```

### defaultdict - Dictionaries with Default Values

```python
from collections import defaultdict

# Creates a dictionary where missing keys get a default value from the specified factory
int_dict = defaultdict(int)  # Default value is 0
int_dict["a"] += 1  # No KeyError, sets int_dict["a"] to 1

list_dict = defaultdict(list)  # Default value is an empty list
list_dict["colors"].append("red")  # No KeyError, adds "red" to the list

set_dict = defaultdict(set)  # Default value is an empty set
set_dict["fruits"].add("apple")
set_dict["fruits"].add("banana")
set_dict["fruits"].add("apple")  # Duplicate ignored (set property)
print(set_dict["fruits"])  # {'apple', 'banana'}
print(set_dict["vegetables"])  # Empty set() created automatically

# Example use case: grouping unique items by category
log_entries = [
    ("error", "Connection timeout"),
    ("warning", "Disk space low"),
    ("error", "Permission denied"),
    ("error", "Connection timeout"),  # Duplicate error
    ("info", "Process started"),
    ("warning", "Disk space low")     # Duplicate warning
]

# Group unique messages by log level
logs_by_level = defaultdict(set)
for level, message in log_entries:
    logs_by_level[level].add(message)

# Result: {'error': {'Connection timeout', 'Permission denied'}, 
#          'warning': {'Disk space low'}, 
#          'info': {'Process started'}}

# Custom factory function
def get_user_template():
    return {"name": "Guest", "access_level": 0}

users = defaultdict(get_user_template)
print(users["user1"])  # {"name": "Guest", "access_level": 0}
```

### Counter - Dictionary for Counting

```python
from collections import Counter

# Count occurrences of elements
text = "mississippi"
counter = Counter(text)
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# Most common elements
counter.most_common(2)  # [('i', 4), ('s', 4)] - top 2 most common

# Update counter
counter.update("missouri")
# Counter({'i': 7, 's': 5, 'm': 2, 'p': 2, 'o': 1, 'u': 1, 'r': 1})

# Arithmetic operations
c1 = Counter("hello")
c2 = Counter("world")
print(c1 + c2)  # Sum of counts
print(c1 - c2)  # Subtract counts (keeping only positive counts)
```

## Practical Dictionary Examples

### Grouping Data

```python
# Group people by their role
people = [
    {"name": "Alice", "role": "developer"},
    {"name": "Bob", "role": "manager"},
    {"name": "Charlie", "role": "developer"},
    {"name": "Diana", "role": "designer"}
]

roles = {}
for person in people:
    role = person["role"]
    if role not in roles:
        roles[role] = []
    roles[role].append(person["name"])

# roles is {'developer': ['Alice', 'Charlie'], 'manager': ['Bob'], 'designer': ['Diana']}

# Cleaner with defaultdict
from collections import defaultdict
roles = defaultdict(list)
for person in people:
    roles[person["role"]].append(person["name"])
```

### Memoization (Caching Results)

```python
# Cache results of expensive function calls
fibonacci_cache = {}

def fibonacci(n):
    # If we have cached the result, return it
    if n in fibonacci_cache:
        return fibonacci_cache[n]
    
    # Otherwise calculate it
    if n <= 1:
        result = n
    else:
        result = fibonacci(n-1) + fibonacci(n-2)
    
    # Cache the result before returning
    fibonacci_cache[n] = result
    return result

# Calculate fibonacci(30) much faster with caching
fibonacci(30)  # This would be very slow without caching
```

### Transforming Lists to Dictionaries

```python
# List of tuples to dictionary
items = [("a", 1), ("b", 2), ("c", 3)]
item_dict = dict(items)  # {"a": 1, "b": 2, "c": 3}

# Two parallel lists to dictionary
keys = ["name", "age", "job"]
values = ["Alice", 28, "Developer"]
user_dict = dict(zip(keys, values))
# {"name": "Alice", "age": 28, "job": "Developer"}

# Creating a lookup table
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]
user_lookup = {user["id"]: user for user in users}
# Quick access by ID: user_lookup[2]["name"] == "Bob"
```

### Sorting Dictionaries

```python
grades = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95}

# Sort by keys
sorted_by_name = dict(sorted(grades.items()))
# {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'Diana': 95}

# Sort by values (ascending)
sorted_by_grade = dict(sorted(grades.items(), key=lambda item: item[1]))
# {'Charlie': 78, 'Alice': 85, 'Bob': 92, 'Diana': 95}

# Sort by values (descending)
top_students = dict(sorted(grades.items(), key=lambda item: item[1], reverse=True))
# {'Diana': 95, 'Bob': 92, 'Alice': 85, 'Charlie': 78}
```

## Performance Tips

1. **Dictionary lookups are fast**: Accessing keys has O(1) average time complexity.

2. **Use `in` operator** to check for key existence instead of catching KeyError:
   ```python
   # Faster and cleaner
   if key in my_dict:
       value = my_dict[key]
   ```

3. **Use get() with default** rather than checking and setting:
   ```python
   # Instead of
   if key not in my_dict:
       my_dict[key] = default_value
   value = my_dict[key]
   
   # Use
   value = my_dict.get(key, default_value)
   ```

4. **Use dictionary comprehensions** instead of loops for transformations:
   ```python
   # Faster than manual loop
   squared = {k: v**2 for k, v in numbers.items()}
   ```

5. **Consider specialized dictionary types** for specific use cases:
   - `defaultdict` for automatic default values
   - `Counter` for counting occurrences
   - `OrderedDict` for maintaining insertion order (pre-Python 3.7)
