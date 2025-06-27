# Python Cheatsheet

!!! warning "WIP" 

Python utility functions to keep in your L1 cache for coding interviews.

## Strings

### str.alnum 

>"mystring".isalnum()  

str.isalnum() returns True if all characters in the string are alphanumeric and the string is not empty.
If the string contains spaces, special characters, or is empty, it will return False.

??? example "[Valid Palindrome](https://leetcode.com/problems/valid-palindrome/description/){target="_blank"}"

    ```python
     class Solution:
         def isPalindrome(self, s: str) -> bool:
     
             start,end = 0, len(s)-1
     
             while start < end :
                 if not s[start].isalnum() : 
                     start+=1
                     continue
                 if not s[end].isalnum() :
                     end-=1
                     continue
                 
                 if not s[start].lower() == s[end].lower() :
                     return False
                 
                 start +=1
                 end-=1
     
             return True
    ```


### ord 

>ord('c')

The ord() function in Python is used to get the Unicode code point (an integer) of a given character. It is the inverse of the chr() function, which converts a Unicode code point back to a character.

??? example "[Score of String](https://leetcode.com/problems/score-of-a-string/){target="_blank"}"

    ```python
    class Solution:
        def scoreOfString(self, s: str) -> int:
            # Initializing this to cancel out the effect of the first element.
            prev=ord(s[0]) 
            res = 0 
            for c in s :
                curr = ord(c)
                res+= abs(curr - prev)
                prev = curr 
            return res 
    ```
### Bisect left with custom key

https://docs.python.org/3/library/bisect.html

```python
# from solution for https://leetcode.com/problems/insert-interval/
from bisect import bisect_left
intervals = [[0,1], [4,5]]
new_interval = [3,4]
intervals.insert(
     bisect_left(intervals,new_interval[0],key=lambda x : x[0]),
     new_interval
)
```

In Python, the insert() method is used to add an element to a list at a specific, chosen index. This method modifies the list in-place, meaning it directly changes the original list rather than creating a new one.

`list.insert(index,element)`


### Sort by ascending with descending tie breaker

```python
"""
https://leetcode.com/problems/remove-covered-intervals/description/
"""
class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # Sort by start point.
        # If two intervals share the same start point
        # put the longer one to be the first.
        intervals.sort(key = lambda x: (x[0], -x[1]))
        count = 0
        
        prev_end = 0
        for _, end in intervals:
            # if current interval is not covered
            # by the previous one
            if end > prev_end:
                count += 1    
                prev_end = end
        
        return count
```


### isinstance

Checks if the object is of a specified type.

```python
#ref : https://www.w3schools.com/python/ref_func_isinstance.asp

def flatten_list(nested_list):
    """
    Flatten a nested list of any depth into a 1D list.
    
    Args:
        nested_list: A list that may contain nested lists as elements
        
    Returns:
        A flattened 1D list containing all elements in the nested list
    """
    res = []
    for item in nested_list :
        if isinstance(item, list) :
            res.extend(flatten_list(item))
        else :
            res.append(item)
    return res

test_case_1 = [[1, 2, [3, 4], 5], [6], [7, [8, [9, 10]]]]
test_case_2 = [[1, "a", [3.1415, [True, 0]], "b"], [None, [2, [3, "text"]]]]
test_case_3 = [[[[]]], [], [[], [[], [[]]]]]

print(flatten_list(test_case_1))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(flatten_list(test_case_2))  # [1, 'a', 3.1415, True, 0, 'b', None, 2, 3, 'text']
print(flatten_list(test_case_3))  # [] 
```

### removing punctutation


```
>>> import string
>>> string.punctuation
'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```

string also has :
```
>>> dir(string)
['Formatter', 'Template', '_ChainMap', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_re', '_sentinel_dict', '_string', 'ascii_letters', 'ascii_lowercase', 'ascii_uppercase', 'capwords', 'digits', 'hexdigits', 'octdigits', 'printable', 'punctuation', 'whitespace']
#example
>>> string.ascii_letters
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

How not to use translate. Does not work:

```
>>> 'a'.translate({'a':'b'})
'a' # expected b
```

Use with str.maketrans

```
>>> str.maketrans('a','b')
{97: 98}
>>> 'a'.translate({97:98})
'b'
```

or in one shot :
```
'a'.translate(str.maketrans('a','b'))
```

You can also remove stuff by combining str.makestrans and translate. str.maketrans takes a third argument for removing characters.
```
>>> str.maketrans('','','a')
{97: None}
```

Cant replace strings with this approach. 

```
>>> str.maketrans('replacethis','withthat','andremovethis')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: the first two maketrans arguments must have equal length
```

Its for replacing characters with their mappings:

```
>>> str.maketrans('replacethis','replacethat','removethis')
{114: None, 101: None, 112: 112, 108: 108, 97: 97, 99: 99, 116: None, 104: None, 105: None, 115: None, 109: None, 111: None, 118: None}
>>> str.maketrans('r','r')
{114: 114}
>>> str.maketrans('r','r','r')
{114: None}
# The last argument for removal, overwrites and thus iverrides Mapping arguments.
>>> 'r'.translate(str.maketrans('r','r','r'))
''

```

See also : https://stackoverflow.com/questions/59877761/how-to-strip-string-from-punctuation-except-apostrophes-for-nlp


Additional Resources :

https://www.stratascratch.com/blog/python-string-methods-here-is-how-to-master-them/
