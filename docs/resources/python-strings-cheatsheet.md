# Python Strings Cheatsheet

Strings in Python are immutable sequences of characters. This cheatsheet covers all essential string operations, methods, and formatting techniques with clear examples and explanations.

## Creating Strings

```python
# String literals
single_quoted = 'Hello, world!'
double_quoted = "Hello, world!"

# How Python handles string literals internally:
"""
In Python 3, all string literals are stored as Unicode by default, not with any specific encoding.
Python strings are sequences of Unicode code points (abstract characters), not bytes.
This means when you type:
    s = "Hello, world!"
Python stores this as Unicode code points, not in any specific encoding like UTF-8 or ASCII.

Encoding only happens when you:
1. Convert the string to bytes using s.encode()
2. Write the string to a file or external system
3. Send the string over a network connection

Until then, Python handles all strings as abstract Unicode sequences internally,
regardless of whether they contain ASCII characters, Japanese, emoji, or other symbols.
"""

# Triple-quoted strings (can span multiple lines)
multi_line = """This is a string that
spans multiple lines
with preserved line breaks."""

# Raw strings (ignore escape sequences)
raw_string = r"C:\Users\John\Documents"  # Backslashes are treated literally

# Escape sequences in regular strings
escaped_string = "Line 1\nLine 2\tTabbed"  # \n for newline, \t for tab
quote_in_string = "He said, \"Hello!\""    # Escaped quotes

# Unicode characters
unicode_string = "\u00A9 2023"  # © 2023
emoji = "\U0001F600"            # 😀

# Byte strings (sequence of bytes, not characters)
byte_string = b"Hello"          # Only ASCII characters allowed
encoded = "こんにちは".encode('utf-8')  # Convert string to bytes with specific encoding

# String literals in source code files
"""
When Python reads your .py source file, it needs to know what encoding the file uses.
By default, Python 3 assumes UTF-8 encoding for source files.
You can specify a different encoding with a comment at the top of the file:
    # -*- coding: encoding -*-
For example:
    # -*- coding: latin-1 -*-

This only affects how Python reads your source code file, not how strings are stored in memory.
Once the string is parsed from the source file, it's stored as Unicode regardless of the
source file's encoding.
"""
```

## String Concatenation

```python
# Using + operator
greeting = "Hello" + ", " + "world!"  # "Hello, world!"

# Using += for in-place concatenation
message = "Hello"
message += ", world!"  # message is now "Hello, world!"

# Using join() with a list of strings (most efficient for multiple strings)
words = ["Hello", "world", "of", "Python"]
sentence = " ".join(words)  # "Hello world of Python"

# Implicit concatenation of string literals (no + needed)
long_string = ("This is a long string that "
               "is split across multiple lines "
               "in the source code.")  # Single string with no newlines

# String multiplication
repeated = "abc" * 3  # "abcabcabc"
separator = "-" * 20  # "--------------------"
```

## Accessing Characters

```python
message = "Hello, world!"

# Indexing (0-based)
first_char = message[0]     # "H"
last_char = message[-1]     # "!"

# Slicing [start:stop:step]
first_five = message[:5]    # "Hello"
last_five = message[-5:]    # "orld!"
every_other = message[::2]  # "Hlo ol!"
reversed_str = message[::-1]  # "!dlrow ,olleH"

# Length
length = len(message)  # 13

# Remember: Strings are immutable
# message[0] = "h"  # This raises TypeError
```

## String Methods for Searching

```python
text = "Python is amazing and Python is easy to learn."

# Finding substrings
first_pos = text.find("Python")    # 0 (first occurrence)
second_pos = text.find("Python", 1)  # 19 (starting from position 1)
not_found = text.find("Java")      # -1 (not found)

# rfind() searches from the end
last_pos = text.rfind("Python")    # 19 (last occurrence)

# index() is like find() but raises ValueError if not found
try:
    pos = text.index("Python")  # 0
    pos = text.index("Java")    # Raises ValueError
except ValueError:
    print("Substring not found")

# Counting occurrences
count = text.count("Python")  # 2
count_is = text.count("is")   # 2

# Checking if string starts/ends with substring
starts_with = text.startswith("Python")  # True
ends_with = text.endswith("learn.")      # True

# Checking prefix/suffix with offset
starts_with_at_19 = text.startswith("Python", 19)  # True
ends_with_partial = text.endswith("easy", 0, 30)   # True

# Checking if substring is present
contains_python = "Python" in text  # True
contains_java = "Java" in text      # False
```

## String Methods for Case Conversion

```python
text = "Python is AMAZING!"

# Case conversion
lower_case = text.lower()       # "python is amazing!"
upper_case = text.upper()       # "PYTHON IS AMAZING!"
title_case = text.title()       # "Python Is Amazing!"
capitalized = text.capitalize() # "Python is amazing!"
swapped_case = text.swapcase()  # "pYTHON IS amazing!"

# Checking case properties
is_lower = text.islower()       # False
is_upper = text.isupper()       # False
is_title = text.istitle()       # False

# Properly capitalizing titles
import string
title = "the lord of the rings"
words = title.split()
capitalized_words = [word.capitalize() if word not in ['a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'from', 'by', 'in'] or i == 0 or i == len(words) - 1 else word for i, word in enumerate(words)]
proper_title = " ".join(capitalized_words)  # "The Lord of the Rings"
```

## String Methods for Stripping and Padding

```python
# Removing whitespace
text = "   Hello, world!   "
left_strip = text.lstrip()     # "Hello, world!   "
right_strip = text.rstrip()    # "   Hello, world!"
both_strip = text.strip()      # "Hello, world!"

# Removing specific characters
text = "###Hello, world!###"
stripped = text.strip('#')     # "Hello, world!"
left_stripped = text.lstrip('#')  # "Hello, world!###"
right_stripped = text.rstrip('#') # "###Hello, world!"

# Padding strings
text = "Hello"
left_pad = text.ljust(10)      # "Hello     "
right_pad = text.rjust(10)     # "     Hello"
center_pad = text.center(11)   # "   Hello   "

# Padding with specific character
left_pad = text.ljust(10, '-')  # "Hello-----"
right_pad = text.rjust(10, '-') # "-----Hello"
center_pad = text.center(11, '-') # "---Hello---"

# Zero-padding numbers
num = 42
zero_padded = str(num).zfill(5)  # "00042"

# Tabulation using expandtabs
tabbed = "Name\tAge\tCity"
expanded = tabbed.expandtabs(15)  # "Name           Age            City"
```

## String Methods for Replacing and Splitting

```python
text = "Python is amazing and Python is easy to learn"

# Replacing substrings
replaced = text.replace("Python", "JavaScript")  # "JavaScript is amazing and JavaScript is easy to learn"
replace_once = text.replace("Python", "JavaScript", 1)  # "JavaScript is amazing and Python is easy to learn"

# Splitting strings
words = text.split()            # ['Python', 'is', 'amazing', 'and', 'Python', 'is', 'easy', 'to', 'learn']
phrases = text.split(" and ")   # ['Python is amazing', 'Python is easy to learn']

# Splitting with max splits
limited_split = text.split(" ", 3)  # ['Python', 'is', 'amazing', 'and Python is easy to learn']

# Splitting by lines
multi_line = "Line 1\nLine 2\nLine 3"
lines = multi_line.splitlines()   # ['Line 1', 'Line 2', 'Line 3']
lines_with_breaks = multi_line.splitlines(True)  # ['Line 1\n', 'Line 2\n', 'Line 3']

# Splitting from the right
rsplit_result = text.rsplit(" ", 2)  # ['Python is amazing and Python is easy', 'to', 'learn']

# Joining strings
words = ["Python", "is", "amazing"]
joined = " ".join(words)  # "Python is amazing"
csv_line = ",".join(words)  # "Python,is,amazing"
```

## String Methods for Checking Content

```python
# Checking character types
num_str = "12345"
alpha_str = "Hello"
alnum_str = "Hello123"
space_str = "   \t\n"
whitespace_with_text = "  Hello  "

# Differences between digit/decimal/numeric methods:
# isdecimal(): Only decimal digits (0-9 and equivalents)
# isdigit(): Decimal digits plus other digit characters (like superscripts)
# isnumeric(): Any character that represents a number (including fractions, Roman numerals)

# Decimal digits (0-9)
"123".isdecimal()  # True
"123".isdigit()    # True
"123".isnumeric()  # True

# Superscript/subscript numbers
"²³".isdecimal()   # False - not standard decimal digits
"²³".isdigit()     # True - these are digit characters
"²³".isnumeric()   # True - these represent numeric values

# Vulgar fractions
"½".isdecimal()    # False - not a standard decimal digit
"½".isdigit()      # False - not a digit character
"½".isnumeric()    # True - represents a numeric value

# Roman numerals
"Ⅶ".isdecimal()    # False
"Ⅶ".isdigit()      # False
"Ⅶ".isnumeric()    # True - represents a numeric value

# Non-Western digits (e.g., Arabic-Indic digits)
"٣٤٥".isdecimal()  # True - these are decimal digits, just from a different script
"٣٤٥".isdigit()    # True
"٣٤٥".isnumeric()  # True

# Other character type checks
alpha_str.isalpha()    # True (only alphabetic characters)
alnum_str.isalnum()    # True (alphabetic or numeric)
alpha_str.isascii()    # True (only ASCII characters)

space_str.isspace()    # True (only whitespace)
whitespace_with_text.isspace()  # False (contains non-whitespace)

# Checking identifiers
variable_name = "my_var_1"
variable_name.isidentifier()  # True (valid Python identifier)
"1invalid".isidentifier()     # False (starts with a digit)

# Checking printable characters
"Hello\n".isprintable()  # False (contains non-printable newline)
"Hello!".isprintable()   # True (all printable)

# Complex example: validating user input
def validate_username(username):
    """Check if username meets requirements: alphanumeric, 3-20 chars."""
    if not (3 <= len(username) <= 20):
        return False, "Username must be 3-20 characters."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    if username[0].isdigit():
        return False, "Username must start with a letter."
    return True, "Username is valid."
```

## String Formatting

### %-formatting (old style)

```python
name = "Alice"
age = 30

# Basic formatting
message = "Hello, %s. You are %d years old." % (name, age)
# "Hello, Alice. You are 30 years old."

# Format specifiers
float_value = 3.14159
formatted = "Value: %.2f" % float_value  # "Value: 3.14"

# Width and alignment
formatted = "%-10s | %10s" % ("Left", "Right")  # "Left       |      Right"

# Named placeholders
formatted = "%(name)s is %(age)d years old." % {"name": "Bob", "age": 25}
# "Bob is 25 years old."
```

### str.format() (new style)

```python
name = "Alice"
age = 30

# Basic formatting
message = "Hello, {}. You are {} years old.".format(name, age)
# "Hello, Alice. You are 30 years old."

# Positional arguments
message = "Hello, {0}. In 5 years, you'll be {1} years old.".format(name, age + 5)
# "Hello, Alice. In 5 years, you'll be 35 years old."

# Named placeholders
message = "Hello, {name}. You are {age} years old.".format(name=name, age=age)
# "Hello, Alice. You are 30 years old."

# Format specifiers
pi = 3.14159
formatted = "Pi: {:.2f}".format(pi)  # "Pi: 3.14"

# Width, alignment, and fill characters
left = "{:<10}".format("Left")    # "Left      "
right = "{:>10}".format("Right")  # "     Right"
center = "{:^10}".format("Center")  # "  Center  "
custom = "{:*^10}".format("Custom")  # "**Custom**"

# Accessing object attributes and dictionary items
person = {"name": "Alice", "age": 30}
message = "{p[name]} is {p[age]} years old.".format(p=person)
# "Alice is 30 years old."

# Formatting integers
decimal = "{:d}".format(42)       # "42"
binary = "{:b}".format(42)        # "101010"
octal = "{:o}".format(42)         # "52"
hexadecimal = "{:x}".format(42)   # "2a"
hexadecimal_upper = "{:X}".format(42)  # "2A"

# Formatting with commas for thousands
large_num = "{:,}".format(1234567)  # "1,234,567"

# Formatting dates
import datetime
now = datetime.datetime.now()
formatted_date = "{:%Y-%m-%d %H:%M:%S}".format(now)
# e.g., "2023-06-27 15:30:45"
```

### f-strings (Python 3.6+)

```python
name = "Alice"
age = 30

# Basic formatting
message = f"Hello, {name}. You are {age} years old."
# "Hello, Alice. You are 30 years old."

# Expressions in placeholders
message = f"In 5 years, {name} will be {age + 5} years old."
# "In 5 years, Alice will be 35 years old."

# Format specifiers
pi = 3.14159
formatted = f"Pi: {pi:.2f}"  # "Pi: 3.14"

# Width, alignment, and fill characters
left = f"{'Left':<10}"    # "Left      "
right = f"{'Right':>10}"  # "     Right"
center = f"{'Center':^10}"  # "  Center  "
custom = f"{'Custom':*^10}"  # "**Custom**"

# Dynamic width
width = 10
dynamic = f"{'Dynamic':^{width}}"  # "  Dynamic  "

# Accessing object attributes and dictionary items
person = {"name": "Alice", "age": 30}
message = f"{person['name']} is {person['age']} years old."
# "Alice is 30 years old."

# Using ! for conversion types
message = f"Representation: {name!r}"  # "Representation: 'Alice'"

# Using = to display expression and result (Python 3.8+)
calculation = f"{age=}"  # "age=30"
expression = f"{age + 5=}"  # "age + 5=35"

# Multiline f-strings
query = f"""
SELECT *
FROM users
WHERE name = '{name}'
  AND age > {age - 5}
"""
```

## String Formatting Using Template Strings

```python
from string import Template

# Creating a template
t = Template("$name is $age years old")

# Substituting values
result = t.substitute(name="Alice", age=30)
# "Alice is 30 years old"

# Safe substitution (doesn't raise KeyError)
result = t.safe_substitute(name="Alice")
# "Alice is $age years old"

# Using a dictionary
values = {"name": "Bob", "age": 25}
result = t.substitute(values)
# "Bob is 25 years old"

# Using $ literally
t = Template("Amount: $$${amount}")
result = t.substitute(amount=100)
# "Amount: $100"
```

## Advanced String Operations

### String Comparison

```python
# Case-sensitive comparison
"apple" == "apple"   # True
"apple" == "Apple"   # False

# Case-insensitive comparison
"apple".lower() == "Apple".lower()  # True
"apple".casefold() == "Apple".casefold()  # True (safer for international text)

# Comparing strings lexicographically
"apple" < "banana"  # True (a comes before b)
"apple" < "BANANA"  # False (uppercase comes before lowercase in ASCII)

# Sorting strings with a custom key
# More Pythonic approach using a tuple key with lambda
strings = ["Apple", "apple", "Banana", "banana"]

# Sort case-insensitive first, then case-sensitive for ties
sorted_strings = sorted(strings, key=lambda s: (s.lower(), s))
# ['apple', 'Apple', 'banana', 'Banana']

# Sort by length, then alphabetically
words = ["cat", "elephant", "dog", "mouse"]
by_length = sorted(words, key=lambda s: (len(s), s))
# ['cat', 'dog', 'mouse', 'elephant']

# Sort with custom ordering (putting specific strings first)
priority = {"high": 0, "medium": 1, "low": 2}
tasks = ["high task", "low task", "medium task"]
by_priority = sorted(tasks, key=lambda s: priority.get(s.split()[0], 999))
# ['high task', 'medium task', 'low task']
```

### Regular Expressions with Strings

```python
import re

text = "Contact us at info@example.com or support@example.org"

# Finding all matches
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
# ['info@example.com', 'support@example.org']

# Search and replace
censored = re.sub(r'[A-Za-z0-9._%+-]+@', "EMAIL@", text)
# "Contact us at EMAIL@example.com or EMAIL@example.org"

# Splitting with regex
words = re.split(r'\W+', "Hello, world! How are you?")
# ['Hello', 'world', 'How', 'are', 'you', '']

# Match objects for more information
pattern = re.compile(r'(\w+)@(\w+)\.(\w+)')
for match in pattern.finditer(text):
    print(f"Full match: {match.group(0)}")
    print(f"Username: {match.group(1)}")
    print(f"Domain: {match.group(2)}")
    print(f"TLD: {match.group(3)}")

# Search with regex
match = re.search(r'\d+', "Order #12345 received")
if match:
    print(f"Found number: {match.group()}")  # "Found number: 12345"
```

### Unicode and Encoding

```python
# Understanding Unicode vs. Encodings (like UTF-8)
"""
The difference between Unicode and UTF-8:

1. Unicode is a CHARACTER SET - a standard that maps characters to unique code points
   - Unicode assigns each character a unique numerical value (code point)
   - For example, 'A' has code point U+0041, '世' has code point U+4E16
   - Unicode doesn't specify how these code points should be stored in memory or files
   - It's just a conceptual mapping: Character ↔ Code Point

2. UTF-8 is an ENCODING - a method for storing Unicode code points as bytes
   - UTF-8 defines the actual bit/byte sequences used to represent Unicode code points
   - It's a variable-width encoding: common characters use fewer bytes
   - ASCII characters (U+0000 to U+007F) use 1 byte in UTF-8
   - Other characters use 2-4 bytes depending on their code point value
   - It's just one of several ways to encode Unicode (others include UTF-16, UTF-32)

In Python 3:
- Strings store Unicode code points internally (not bytes)
- When you need to save or transmit text, you encode these code points to bytes
- UTF-8 is the most common encoding, but others can be used depending on requirements
"""

# Unicode characters and code points
char = "é"
code_point = ord(char)  # 233 (the Unicode code point for é)
back_to_char = chr(code_point)  # "é" (convert code point back to character)

# The Unicode standard contains over 140,000 characters
print(ord("A"))        # 65 (Basic Latin)
print(ord("Ω"))        # 937 (Greek)
print(ord("世"))        # 19990 (CJK Unified Ideographs)
print(ord("😀"))        # 128512 (Emoji)

# UTF-8 encoding of these characters (variable length)
print(len("A".encode("utf-8")))   # 1 byte
print(len("Ω".encode("utf-8")))   # 2 bytes
print(len("世".encode("utf-8")))   # 3 bytes
print(len("😀".encode("utf-8")))   # 4 bytes

# UTF-8 encoding preserves ASCII compatibility
ascii_str = "ABC123"
utf8_bytes = ascii_str.encode("utf-8")
print(utf8_bytes)  # b'ABC123' - each ASCII character is 1 byte in UTF-8

# For non-ASCII characters, UTF-8 uses multi-byte sequences
mixed_str = "Hello, 世界! 👋"
utf8_bytes = mixed_str.encode("utf-8")
print(utf8_bytes)  # b'Hello, \xe4\xb8\x96\xe7\x95\x8c! \xf0\x9f\x91\x8b'
print([len(c.encode("utf-8")) for c in mixed_str])  # [1, 1, 1, 1, 1, 1, 3, 3, 1, 4]

# Other Unicode encodings handle bytes differently
print(len("😀".encode("utf-8")))   # 4 bytes in UTF-8
print(len("😀".encode("utf-16")))  # 4 bytes in UTF-16 (2 surrogate pairs)
print(len("😀".encode("utf-32")))  # 4 bytes in UTF-32 (fixed width)

# String encoding: Converting Unicode strings to bytes
text = "こんにちは"  # "Hello" in Japanese

# .encode(encoding, errors) converts a string to a bytes object
# Important: encode() ALWAYS returns a bytes object, not a string
encoded = text.encode("utf-8")  
print(encoded)  # b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf'
print(type(encoded))  # <class 'bytes'>

# Why ASCII characters don't show as hex in bytes representation:
ascii_bytes = "hello".encode("utf-8")
print(ascii_bytes)  # b'hello'

# This is because Python displays bytes objects in a dual format:
# 1. ASCII-printable bytes (32-126) are shown as their character representation
# 2. Non-ASCII-printable bytes are shown as hex escape sequences (\xNN)

# Let's see this with a mixed string:
mixed = "hello世界"
mixed_bytes = mixed.encode("utf-8")
print(mixed_bytes)  # b'hello\xe4\xb8\x96\xe7\x95\x8c'
# 'hello' shows as ASCII characters, but the Chinese characters show as hex

# To see the actual integer values of each byte:
print([b for b in ascii_bytes])  # [104, 101, 108, 108, 111]
print([b for b in encoded])      # [227, 129, 147, 227, 130, 147, ...] 

# Both are just sequences of bytes (integers 0-255), they just display differently
# You can confirm they're the same type:
print(type(ascii_bytes) == type(encoded))  # True

# Key differences between str and bytes:
# - str: sequence of Unicode characters (can contain any character)
# - bytes: sequence of integers between 0-255 (represents raw data)

# Common encodings
utf8_bytes = text.encode("utf-8")    # Variable-width encoding (1-4 bytes per character)
utf16_bytes = text.encode("utf-16")  # Usually 2 or 4 bytes per character, with BOM

# ASCII vs. Unicode encodings:
# ASCII is a 7-bit encoding that can only represent characters with code points 0-127
# It's actually a subset of UTF-8, meaning any valid ASCII text is also valid UTF-8
print("ASCII encoding vs. other Unicode encodings:")

# For ASCII-only text, UTF-8 and ASCII encoding produce identical results
ascii_text = "Hello, world!"
print(ascii_text.encode("ascii"))  # b'Hello, world!'
print(ascii_text.encode("utf-8"))  # b'Hello, world!'

# The difference appears with non-ASCII characters
mixed_text = "Hello, café!"  # Contains the non-ASCII 'é' character

# UTF-8 can handle any Unicode character
utf8_result = mixed_text.encode("utf-8")  
print(utf8_result)  # b'Hello, caf\xc3\xa9!' ('é' takes 2 bytes in UTF-8)

# ASCII can only handle ASCII characters (code points 0-127)
try:
    ascii_result = mixed_text.encode("ascii")  # Raises UnicodeEncodeError
except UnicodeEncodeError as e:
    print(f"ASCII encoding error: {e}")
    # Handle encoding errors with the errors parameter
    ascii_replace = mixed_text.encode("ascii", errors="replace")  # b'Hello, caf?!'
    ascii_ignore = mixed_text.encode("ascii", errors="ignore")    # b'Hello, caf!'
    ascii_xmlcharrefreplace = mixed_text.encode("ascii", errors="xmlcharrefreplace")  # b'Hello, caf&#233;!'
    
    print(f"With replace: {ascii_replace}")
    print(f"With ignore: {ascii_ignore}")
    print(f"With xmlcharrefreplace: {ascii_xmlcharrefreplace}")

# Comparing sizes of different encodings
sample = "Hello, 世界"  # "Hello, World" with Chinese characters
print(f"Text length: {len(sample)} characters")
print(f"ASCII (with replace): {len(sample.encode('ascii', errors='replace'))} bytes")
print(f"UTF-8: {len(sample.encode('utf-8'))} bytes")
print(f"UTF-16: {len(sample.encode('utf-16'))} bytes")
print(f"UTF-32: {len(sample.encode('utf-32'))} bytes")

# UTF-8 advantages:
# - Backward compatible with ASCII (ASCII chars use 1 byte)
# - Variable width (saves space for common Latin characters)
# - Self-synchronizing (can detect start of next character)
# - No endianness issues (unlike UTF-16/UTF-32)

# Decoding: Converting bytes back to strings
decoded = encoded.decode("utf-8")  # "こんにちは"

# The decode method has the same error handling options
try:
    corrupt_decoded = b'\xe3\x81\x93\xe3'.decode("utf-8")  # Raises UnicodeDecodeError (incomplete byte sequence)
except UnicodeDecodeError:
    # Handle decoding errors with the errors parameter
    replace_decoded = b'\xe3\x81\x93\xe3'.decode("utf-8", errors="replace")  # "こ�"
    ignore_decoded = b'\xe3\x81\x93\xe3'.decode("utf-8", errors="ignore")    # "こ"

# Practical examples

# 1. File I/O with encoding
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("Hello, café!")  # Saved as UTF-8 bytes

with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()  # Decoded from UTF-8 bytes to string

# 2. Web requests
import urllib.request
response = urllib.request.urlopen("https://www.example.com")
html_bytes = response.read()  # Bytes
encoding = response.headers.get_content_charset() or "utf-8"  # Get encoding from headers or default
html_string = html_bytes.decode(encoding)  # Convert to string

# 3. Database storage
# When storing strings in databases, you need to ensure the database
# uses the right encoding (usually UTF-8) and that your connection
# is configured to use that encoding

# Detecting encoding
# Python doesn't have a built-in way to detect encoding reliably,
# but the chardet library can make educated guesses:
try:
    import chardet
    unknown_bytes = b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf'
    detected = chardet.detect(unknown_bytes)
    print(f"Detected encoding: {detected['encoding']}, confidence: {detected['confidence']}")
    # Might output: "Detected encoding: utf-8, confidence: 0.87"
except ImportError:
    pass  # chardet not installed

# Normalizing Unicode (handling composed vs decomposed forms)
from unicodedata import normalize
composed = "é"  # Single character
decomposed = "e\u0301"  # 'e' followed by combining acute accent
normalize("NFC", decomposed) == composed  # True (normalizes to composed form)
normalize("NFD", composed) == decomposed  # True (normalizes to decomposed form)
```

### String Interpolation in Different Contexts

```python
# In SQL queries (vulnerable to SQL injection - don't use in production!)
username = "O'Reilly"  # Note the apostrophe
# Wrong: f"SELECT * FROM users WHERE username = '{username}'"  # SQL injection risk!

# Safe parameterized query
query = "SELECT * FROM users WHERE username = %s"
# Then pass username as a parameter to your database driver

# In HTML (vulnerable to XSS - don't use in production!)
user_input = "<script>alert('XSS')</script>"
# Wrong: f"<div>{user_input}</div>"  # XSS risk!

# Safe HTML escaping
import html
safe_html = f"<div>{html.escape(user_input)}</div>"
# "<div>&lt;script&gt;alert('XSS')&lt;/script&gt;</div>"

# In shell commands (vulnerable to command injection - don't use in production!)
filename = "file; rm -rf /"
# Wrong: os.system(f"cat {filename}")  # Command injection risk!

# Safe command execution
import subprocess
subprocess.run(["cat", filename], check=True)  # Safe, no shell interpretation
```

## Common String Patterns

### String Parsing and Extraction

```python
# Extracting parts of a string using slicing
email = "user@example.com"
username = email[:email.find('@')]  # "user"
domain = email[email.find('@')+1:]  # "example.com"

# Extracting with regular expressions
import re
url = "https://www.example.com/path?param=value"
pattern = r"https?://(?:www\.)?([^/]+)(.*)"
match = re.match(pattern, url)
if match:
    domain = match.group(1)  # "example.com"
    path = match.group(2)    # "/path?param=value"

# Parsing key-value pairs
query_string = "name=John&age=30&city=New%20York"
params = {}
for pair in query_string.split('&'):
    if '=' in pair:
        key, value = pair.split('=', 1)
        params[key] = value.replace('%20', ' ')
# params = {'name': 'John', 'age': '30', 'city': 'New York'}
```

### Text Processing

```python
# Word count
text = "This is a sample text. This text has some duplicate words."
words = text.lower().split()
word_count = {}
for word in words:
    # Remove punctuation from word
    word = word.strip('.,!?:;()"\'')
    if word:
        word_count[word] = word_count.get(word, 0) + 1
# {'this': 2, 'is': 1, 'a': 1, 'sample': 1, 'text': 2, 'has': 1, 'some': 1, 'duplicate': 1, 'words': 1}

# Finding most common words
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
most_common = sorted_words[:3]  # [('this', 2), ('text', 2), ('is', 1)]

# Sentence tokenization (basic)
text = "Hello. How are you? I'm fine. Thanks."
sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
# ['Hello', 'How are you', "I'm fine", 'Thanks']

# More accurate sentence tokenization
import re
def split_into_sentences(text):
    # Handle common abbreviations to avoid false splits
    text = re.sub(r'([A-Z][a-z]{1,2})\. ', r'\1§ ', text)  # Mr. Dr. etc.
    # Split on sentence ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Restore periods in abbreviations
    return [s.replace('§', '.') for s in sentences]

# Text wrapping to a specific width
import textwrap
long_text = "This is a very long text that needs to be wrapped to fit within a specific width."
wrapped = textwrap.fill(long_text, width=30)
# This is a very long text that
# needs to be wrapped to fit
# within a specific width.
```

### String Validation

```python
# Email validation (simple)
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

is_valid_email("user@example.com")  # True
is_valid_email("invalid-email")     # False

# Phone number validation (US format)
def is_valid_us_phone(phone):
    # Remove any non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if we have 10 digits, or 11 digits starting with 1
    if len(digits_only) == 10:
        return True
    if len(digits_only) == 11 and digits_only[0] == '1':
        return True
    return False

is_valid_us_phone("(123) 456-7890")  # True
is_valid_us_phone("123-456-7890")    # True
is_valid_us_phone("1-123-456-7890")  # True
is_valid_us_phone("12345")          # False

# Password strength checking
def check_password_strength(password):
    """Check password strength and return feedback."""
    issues = []
    if len(password) < 8:
        issues.append("Password should be at least 8 characters")
    if not re.search(r'[A-Z]', password):
        issues.append("Password should contain uppercase letters")
    if not re.search(r'[a-z]', password):
        issues.append("Password should contain lowercase letters")
    if not re.search(r'\d', password):
        issues.append("Password should contain digits")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        issues.append("Password should contain special characters")
    
    if not issues:
        return "Strong password", []
    return "Weak password", issues
```

### JSON String Handling

```python
import json

# Converting Python objects to JSON strings
data = {
    "name": "Alice",
    "age": 30,
    "is_student": False,
    "courses": ["Python", "Data Science"],
    "grades": {"Python": 95, "Data Science": 88}
}

# Basic conversion
json_str = json.dumps(data)
# '{"name": "Alice", "age": 30, "is_student": false, "courses": ["Python", "Data Science"], "grades": {"Python": 95, "Data Science": 88}}'

# Pretty printing
pretty_json = json.dumps(data, indent=4, sort_keys=True)
# {
#     "age": 30,
#     "courses": [
#         "Python",
#         "Data Science"
#     ],
#     "grades": {
#         "Data Science": 88,
#         "Python": 95
#     },
#     "is_student": false,
#     "name": "Alice"
# }

# Parsing JSON strings
parsed_data = json.loads(json_str)
name = parsed_data["name"]  # "Alice"

# Handling JSON encoding for custom objects
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def person_to_dict(obj):
    if isinstance(obj, Person):
        return {"name": obj.name, "age": obj.age}
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

person = Person("Bob", 25)
person_json = json.dumps(person, default=person_to_dict)
# '{"name": "Bob", "age": 25}'
```

## String Performance Considerations

```python
# String concatenation in loops
# Inefficient (creates many intermediate strings):
result = ""
for i in range(1000):
    result += str(i)

# Efficient (collects strings and joins once):
parts = []
for i in range(1000):
    parts.append(str(i))
result = "".join(parts)

# String building with join is much faster than += for many concatenations
# Benchmark example:
import timeit

def concat_with_plus():
    result = ""
    for i in range(1000):
        result += str(i)
    return result

def concat_with_join():
    return "".join(str(i) for i in range(1000))

plus_time = timeit.timeit(concat_with_plus, number=100)
join_time = timeit.timeit(concat_with_join, number=100)
print(f"Plus: {plus_time:.6f}s, Join: {join_time:.6f}s, Ratio: {plus_time/join_time:.2f}x")
# Example output: "Plus: 0.068213s, Join: 0.005749s, Ratio: 11.87x"

# String interning
# Python automatically interns some strings to save memory
a = "hello"
b = "hello"
a is b  # True (same object due to interning)

c = "hello world"
d = "hello world"
c is d  # May be False, as longer strings might not be interned

# String copying (strings are immutable, so 'copying' just creates a reference)
original = "hello"
copy = original  # Just a reference, not a separate copy
copy is original  # True

# String memory usage
import sys
text = "hello"
memory = sys.getsizeof(text)  # Size in bytes (implementation dependent)
```

## Appendix: Common String Operations and Their Time Complexity

| Operation | Example | Time Complexity | Notes |
|-----------|---------|----------------|-------|
| Creation | `s = "hello"` | O(n) | n is the length of the string |
| Concatenation | `s1 + s2` | O(n + m) | n and m are the lengths of the strings |
| Repetition | `s * n` | O(n * m) | n is the repetition count, m is the length of s |
| Slicing | `s[1:5]` | O(k) | k is the length of the slice |
| Length | `len(s)` | O(1) | Constant time operation |
| Membership | `c in s` | O(n) | n is the length of the string |
| Indexing | `s[i]` | O(1) | Constant time operation |
| Iteration | `for c in s` | O(n) | n is the length of the string |
| String comparison | `s1 == s2` | O(n) | n is the length of the shorter string |
| `find()`, `index()` | `s.find("x")` | O(n) | n is the length of the string |
| `count()` | `s.count("x")` | O(n) | n is the length of the string |
| `split()` | `s.split()` | O(n) | n is the length of the string |
| `join()` | `",".join(list)` | O(n) | n is the total length of all strings |
| `strip()`, `lstrip()`, `rstrip()` | `s.strip()` | O(n) | n is the length of the string |
| Case conversion | `s.upper()` | O(n) | n is the length of the string |
| `replace()` | `s.replace("a", "b")` | O(n) | n is the length of the string |

## Appendix: Understanding Unicode and Encodings

### The Difference Between Unicode and UTF-8

Unicode and UTF-8 represent two different aspects of text handling in computing:

#### Unicode: A Character Set

Unicode is a **standard** that maps characters to unique code points:

- Unicode assigns each character a unique numerical value called a code point
- Code points are typically written as U+XXXX (e.g., U+0041 for 'A', U+4E16 for '世')
- Unicode currently defines over 140,000 characters covering virtually all modern writing systems
- Unicode doesn't specify how these code points should be stored in memory or files
- It's purely a conceptual mapping: Character ↔ Code Point

Examples of Unicode code points:
- 'A' → U+0041 (65 in decimal)
- 'ñ' → U+00F1 (241 in decimal)
- '€' → U+20AC (8364 in decimal)
- '世' → U+4E16 (19990 in decimal)
- '😀' → U+1F600 (128512 in decimal)

#### UTF-8: An Encoding

UTF-8 is an **encoding** - a method for storing Unicode code points as bytes:

- UTF-8 defines the actual bit/byte sequences used to represent Unicode code points
- It's a variable-width encoding: common characters use fewer bytes
- ASCII characters (U+0000 to U+007F) use 1 byte in UTF-8
- Other characters use 2-4 bytes depending on their code point value
- UTF-8 is just one of several ways to encode Unicode (others include UTF-16, UTF-32)

Characteristics of UTF-8:
- ASCII-compatible (ASCII characters are encoded the same way)
- Variable-width (1-4 bytes per character)
- Self-synchronizing (can detect character boundaries)
- Compact for Western languages
- Most common encoding on the web

### How UTF-8 Encoding Works

UTF-8 uses a variable number of bytes for different characters:

| Unicode Range | UTF-8 Byte Format | Bytes Used |
|---------------|-------------------|------------|
| U+0000 to U+007F | 0xxxxxxx | 1 byte |
| U+0080 to U+07FF | 110xxxxx 10xxxxxx | 2 bytes |
| U+0800 to U+FFFF | 1110xxxx 10xxxxxx 10xxxxxx | 3 bytes |
| U+10000 to U+10FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx | 4 bytes |

Examples of UTF-8 encoding:
- 'A' (U+0041) → 01000001 (1 byte)
- 'ñ' (U+00F1) → 11000011 10110001 (2 bytes)
- '€' (U+20AC) → 11100010 10000010 10101100 (3 bytes)
- '😀' (U+1F600) → 11110000 10011111 10011000 10000000 (4 bytes)

### Comparison with Other Unicode Encodings

| Encoding | Description | Advantages | Disadvantages |
|----------|-------------|------------|--------------|
| UTF-8 | Variable-width (1-4 bytes) | ASCII-compatible, compact for Latin text, no endianness issues | Less efficient for Asian scripts |
| UTF-16 | Variable-width (2 or 4 bytes) | Compact for Asian scripts | Not ASCII-compatible, endianness issues, surrogate pairs |
| UTF-32 | Fixed-width (4 bytes) | Simple indexing, no surrogate pairs | Memory inefficient, not ASCII-compatible, endianness issues |

### Python's String Handling

In Python 3:
- Strings are sequences of Unicode code points
- String literals in code are Unicode by default
- When you need to save or transmit text, you encode these code points to bytes
- When reading external data, you decode bytes back to Unicode strings

```python
# Unicode code points
char = "世"
code_point = ord(char)  # 19990
back_to_char = chr(code_point)  # '世'

# Encoding to bytes
utf8_bytes = char.encode("utf-8")   # b'\xe4\xb8\x96' (3 bytes)
utf16_bytes = char.encode("utf-16") # b'\xff\xfe\x16N' (4 bytes with BOM)
utf32_bytes = char.encode("utf-32") # b'\xff\xfe\x00\x00\x16N\x00\x00' (8 bytes with BOM)

# Decoding from bytes
char_again = utf8_bytes.decode("utf-8")  # '世'
```

### Common Encoding-Related Issues

1. **UnicodeEncodeError**: Raised when a string contains characters that cannot be encoded in the target encoding
   ```python
   "café".encode("ascii")  # UnicodeEncodeError: 'ascii' codec can't encode character '\xe9'
   ```

2. **UnicodeDecodeError**: Raised when bytes cannot be decoded using the specified encoding
   ```python
   b'\xff\xfe'.decode("utf-8")  # UnicodeDecodeError: invalid continuation byte
   ```

3. **Mojibake**: Garbled text resulting from decoding bytes with the wrong encoding
   ```python
   utf8_bytes = "café".encode("utf-8")
   wrong_decode = utf8_bytes.decode("latin-1")  # 'cafÃ©' (mojibake)
   ```

4. **BOM (Byte Order Mark)**: Special marker at the start of a file indicating endianness
   ```python
   # UTF-16 encodes a BOM by default
   "abc".encode("utf-16")  # b'\xff\xfe' (BOM) + b'a\x00b\x00c\x00'
   ```

### Best Practices for Handling Text in Python

1. **Use Unicode strings (default in Python 3)** for text processing
2. **Be explicit about encodings** when reading/writing files
3. **Use UTF-8** as your default encoding unless you have a specific reason not to
4. **Handle encoding errors** with appropriate error strategies
5. **Normalize Unicode** when comparing strings from different sources

