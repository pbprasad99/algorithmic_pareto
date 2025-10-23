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

So finally this is how to do it :
```
s = "Hello, World! Python is amazing."

# Create translation table
import string
translator = str.maketrans('', '', string.punctuation)

# Remove punctuation
clean_text = s.translate(translator)
print(clean_text)
```

But one big problem : It removes apostrophe from 'shouldn't', 'how's' 

You could just exclude apostrophe from string.punctutaion and use translate + str.maketrans.

Or use a regex. The following is from Claude :



```python
import re

s = "This is a test string, with punctuation. This shouldn't fail...!"

# re.sub(pattern,with_whatever, input_string)
text = re.sub(r'[^\w\d\s\']+', '', s)
print(text)
```

In this code:

1. `re.sub()` is being used to substitute matches of a pattern with a replacement string (empty string in this case).

2. The regex pattern `r'[^\w\d\s\']+` breaks down as:
   - `[^...]`: A negated character class (matches any character NOT in the brackets)
   - `\w`: Word characters (letters, digits, underscores)
   - `\d`: Digits (0-9)
   - `\s`: Whitespace characters (spaces, tabs, newlines)
   - `\'`: The apostrophe character (')
   - `+`: One or more occurrences of the preceding character class

3. So this pattern will match one or more characters that are NOT:
   - Letters, digits, or underscores
   - Digits (redundant, as digits are already covered by \w)
   - Whitespace characters
   - Apostrophes

4. When these matched characters are replaced with an empty string, you get a string with:
   - All punctuation marks removed EXCEPT for apostrophes
   - All letters, numbers, spaces, and apostrophes preserved

The output would be:
```
This is a test string with punctuation This shouldn't fail
```

This approach is useful when you want to preserve contractions and possessives in English text (like "shouldn't", "John's", etc.) while removing other punctuation marks. It's a selective punctuation removal that's more language-aware than simply removing all punctuation.

See also : https://stackoverflow.com/questions/59877761/how-to-strip-string-from-punctuation-except-apostrophes-for-nlp

## Raw Strings

The `r` before the string in `r'[^\w\s]'` is a prefix that denotes a "raw string" in Python. It's particularly useful when working with regular expressions. Here's what it does:

## Raw String Prefix (`r`)

When you place an `r` before a string literal in Python, it tells the interpreter to treat backslashes (`\`) as literal characters rather than escape characters.

### Without the `r` prefix:
```python
pattern = '\w'  # Python interprets \w as a special escape sequence
```
In a normal string, backslashes have special meaning. For example, `\n` represents a newline, `\t` represents a tab, etc.

### With the `r` prefix:
```python
pattern = r'\w'  # Python treats \w literally as backslash + w
```
In a raw string, backslashes are treated as literal backslashes, not as the start of an escape sequence.

## Why it's important for regex:

Regular expressions use backslashes extensively to denote special character classes:
- `\w` matches word characters
- `\d` matches digits
- `\s` matches whitespace

Without the `r` prefix, you would need to escape each backslash in your regex pattern:
```python
# Without raw string - need to double escape
pattern = '\\w\\s'  # To match a word character followed by whitespace
```

With the `r` prefix, you can write regex patterns more naturally:
```python
# With raw string - cleaner syntax
pattern = r'\w\s'  # Same pattern, more readable
```

Using raw strings makes regular expressions much more readable and less prone to errors, as you don't need to worry about Python's string escape processing interfering with regex syntax.


Additional Resources :

https://www.stratascratch.com/blog/python-string-methods-here-is-how-to-master-them/
