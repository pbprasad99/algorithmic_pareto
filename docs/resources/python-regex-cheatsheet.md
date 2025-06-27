# Python Regular Expressions Cheatsheet

## Basic Patterns

### Literal Characters

Regular expressions match literal characters by default.

```python
import re
text = "Python is powerful"
result = re.search("Python", text)  # Matches "Python"
```

### Metacharacters

Special characters with meaning in regex must be escaped with a backslash `\` to match literally.

```python
# Metacharacters: . ^ $ * + ? { } [ ] \ | ( )
text = "Cost: $25.99"
result = re.search("\$\d+\.\d+", text)  # Matches "$25.99"
```

## Character Classes

### Single Character Matchers

`.` (dot) matches any character except a newline.

```python
pattern = "c.t"
# Matches "cat", "cut", "c@t", etc.
```

### Character Sets

`[ ]` define a character set - matches any single character within the brackets.

```python
pattern = "[aeiou]"  # Matches any single vowel
re.findall(pattern, "apple")  # Returns ['a', 'e']

# Range of characters
pattern = "[a-z]"  # Matches any lowercase letter
pattern = "[A-Za-z]"  # Matches any letter
pattern = "[0-9]"  # Matches any digit
```

### Negated Character Sets

`[^ ]` matches any character NOT in the set.

```python
pattern = "[^0-9]"  # Matches any non-digit
re.findall(pattern, "abc123")  # Returns ['a', 'b', 'c']
```

## Predefined Character Classes

Shorthand notation for common character sets:

```python
\d  # Matches any digit [0-9]
\D  # Matches any non-digit [^0-9]
\w  # Matches any word character [a-zA-Z0-9_]
\W  # Matches any non-word character
\s  # Matches any whitespace character (space, tab, newline)
\S  # Matches any non-whitespace character

# Example
pattern = r"\d\s\w+"  # Digit, followed by whitespace, followed by 1+ word chars
re.search(pattern, "7 apples")  # Matches "7 apples"
```

## Anchors and Boundaries

Anchors match positions rather than characters:

```python
^  # Matches the start of a string
$  # Matches the end of a string
\b  # Matches a word boundary
\B  # Matches a non-word boundary

# Examples
pattern = r"^Python"  # Matches "Python" only at the start
re.search(pattern, "Python is great")  # Match
re.search(pattern, "I love Python")    # No match

pattern = r"Python$"  # Matches "Python" only at the end
re.search(pattern, "I love Python")    # Match
re.search(pattern, "Python is great")  # No match

pattern = r"\bcat\b"  # Matches the word "cat" with boundaries
re.search(pattern, "The cat sits")     # Match
re.search(pattern, "category")         # No match
```

### The Dual Meaning of ^

It's important to note that the caret symbol `^` has two distinct meanings in regular expressions:

1. **Outside square brackets**: When used at the beginning of a pattern, it's an anchor that matches the start of a string or line.
   ```python
   pattern = r"^abc"  # Matches "abc" only at the start of the string
   ```

2. **Inside square brackets**: When used as the first character inside square brackets, it negates the character class, meaning "match any character EXCEPT these."
   ```python
   pattern = r"[^0-9]"  # Matches any character that is NOT a digit
   ```

This distinction is crucial when reading and writing regex patterns. For example, in an email validation pattern:
```python
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
```
The first `^` indicates the match must start at the beginning of the string, while in `[a-zA-Z0-9._%+-]` the characters are simply a positive character class defining what's allowed in the username portion of the email.


## Quantifiers

Quantifiers specify how many times a pattern should match:

```python
*      # 0 or more repetitions
+      # 1 or more repetitions
?      # 0 or 1 repetition
{n}    # Exactly n repetitions
{n,}   # n or more repetitions
{n,m}  # Between n and m repetitions

# Examples
pattern = r"ab*c"     # Matches "ac", "abc", "abbc", etc.
pattern = r"ab+c"     # Matches "abc", "abbc", etc. (not "ac")
pattern = r"colou?r"  # Matches "color" or "colour"
pattern = r"\d{2,4}"  # Matches 2 to 4 digits
```

### Greedy vs. Non-Greedy

Quantifiers are greedy by default (match as much as possible). Adding `?` after a quantifier makes it non-greedy.

```python
text = "<div>Content</div><div>More</div>"

# Greedy matching
pattern = r"<div>.*</div>"
re.findall(pattern, text)  # Returns ['<div>Content</div><div>More</div>']

# Non-greedy matching
pattern = r"<div>.*?</div>"
re.findall(pattern, text)  # Returns ['<div>Content</div>', '<div>More</div>']
```

## Grouping and Capturing

Parentheses `( )` create capture groups:

```python
pattern = r"(\d{3})-(\d{3})-(\d{4})"
match = re.search(pattern, "Phone: 123-456-7890")
match.group(0)  # Entire match: "123-456-7890"
match.group(1)  # First group: "123"
match.group(2)  # Second group: "456"
match.group(3)  # Third group: "7890"
match.groups()  # All groups: ("123", "456", "7890")
```

### Named Groups

Use `(?P<name>...)` for named groups:

```python
pattern = r"(?P<area>\d{3})-(?P<prefix>\d{3})-(?P<line>\d{4})"
match = re.search(pattern, "Phone: 123-456-7890")
match.group("area")    # "123"
match.group("prefix")  # "456"
match.group("line")    # "7890"
```

### Non-Capturing Groups

Use `(?:...)` for non-capturing groups:

```python
pattern = r"(?:\d{3})-\d{3}-(\d{4})"
match = re.search(pattern, "123-456-7890")
match.groups()  # Only contains ("7890"), the first part isn't captured
```

## Alternation

The pipe symbol `|` works as an OR operator:

```python
pattern = r"cat|dog"
re.findall(pattern, "I have a cat and a dog")  # Returns ['cat', 'dog']

# Grouped alternation
pattern = r"(cat|dog)s?"
re.findall(pattern, "I have cats and a dog")  # Returns ['cat', 'dog']
```

## Lookahead and Lookbehind

These are zero-width assertions that don't consume characters:

```python
# Positive lookahead (?=...): Match if followed by pattern
pattern = r"\w+(?=\s+is)"
re.findall(pattern, "Python is great, Java is powerful")  # ['Python', 'Java']

# Negative lookahead (?!...): Match if NOT followed by pattern
pattern = r"Python(?!\s+3)"
re.search(pattern, "Python 2.7")  # Match
re.search(pattern, "Python 3.9")  # No match

# Positive lookbehind (?<=...): Match if preceded by pattern
pattern = r"(?<=\$)\d+"
re.findall(pattern, "Items: $10, $25, €30")  # ['10', '25']

# Negative lookbehind (?<!...): Match if NOT preceded by pattern
pattern = r"(?<!\$)\d+"
re.findall(pattern, "$10, 20, $30")  # ['0', '20', '0']
```

## Common Functions

### re.search()

Finds the first match of the pattern:

```python
result = re.search(r"\d+", "abc123def456")
if result:
    print(result.group())  # "123"
```

### re.match()

Matches pattern only at the beginning of the string:

```python
re.match(r"\d+", "123abc")   # Match
re.match(r"\d+", "abc123")   # No match
```

### re.findall()

Returns all non-overlapping matches as a list:

```python
re.findall(r"\d+", "abc123def456")  # Returns ['123', '456']
```

### re.finditer()

Returns an iterator of match objects:

```python
for match in re.finditer(r"\d+", "abc123def456"):
    print(match.group(), match.span())  # "123" (3, 6), "456" (9, 12)
```

### re.sub()

Substitutes matches with a replacement:

```python
# Basic substitution
re.sub(r"\d+", "NUM", "abc123def456")  # Returns "abcNUMdefNUM"

# Using backreferences
re.sub(r"(\d{3})-(\d{3})-(\d{4})", r"(\1) \2-\3", "123-456-7890")
# Returns "(123) 456-7890"

# Using a function for replacement
def double_digits(match):
    return str(int(match.group()) * 2)

re.sub(r"\d+", double_digits, "abc123def456")  # Returns "abc246def912"
```

### re.split()

Splits a string by pattern matches:

```python
re.split(r"\s+", "Split   these words")  # Returns ['Split', 'these', 'words']
re.split(r"[,;]", "apple,orange;banana")  # Returns ['apple', 'orange', 'banana']
```

## Flags

Modify regex behavior with flags:

```python
re.IGNORECASE  # or re.I: Case-insensitive matching
re.search(r"python", "Python", re.IGNORECASE)  # Match

re.MULTILINE  # or re.M: ^ and $ match start/end of each line
text = "Line 1\nLine 2"
re.findall(r"^Line", text, re.MULTILINE)  # Returns ['Line', 'Line']

re.DOTALL  # or re.S: Dot matches any character including newline
re.search(r"Line 1.+Line 2", "Line 1\nLine 2", re.DOTALL)  # Match

re.VERBOSE  # or re.X: Allow whitespace and comments in pattern
pattern = re.compile(r"""
    \d{3}  # Area code
    [-.]?  # Optional separator
    \d{3}  # Prefix
    [-.]?  # Optional separator
    \d{4}  # Line number
    """, re.VERBOSE)

# Multiple flags
re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
```

## Raw Strings

Use raw strings (`r"..."`) to avoid issues with backslashes:

```python
# Without raw string
re.search("\\d+", "123")  # Need double backslash

# With raw string (recommended)
re.search(r"\d+", "123")  # Much cleaner
```

## Practical Examples

### Email Validation

```python
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
re.match(email_pattern, "user@example.com")  # Match
re.match(email_pattern, "invalid@email")     # No match
```

### URL Extraction

```python
url_pattern = r"https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)"
re.findall(url_pattern, "Visit https://example.com and http://test.org")
# Returns ['https://example.com', 'http://test.org']
```

### Date Formatting

```python
# Convert MM/DD/YYYY to YYYY-MM-DD
date_text = "Today's date: 12/25/2023"
re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\1-\2", date_text)
# Returns "Today's date: 2023-12-25"
```

### Password Validation

```python
# At least 8 chars with 1+ uppercase, 1+ lowercase, 1+ digit, 1+ special char
password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
re.match(password_pattern, "Passw0rd!")  # Match
re.match(password_pattern, "password")   # No match
```

### Stripping HTML Tags

```python
html_text = "<p>This is <b>bold</b> text.</p>"
re.sub(r"<[^>]*>", "", html_text)  # Returns "This is bold text."
```

### Extracting Quoted Text

```python
text = 'She said "hello" and he replied "goodbye"'
re.findall(r'"([^"]*)"', text)  # Returns ['hello', 'goodbye']
```

## Performance Tips

1. **Compile patterns** for repeated use:
   ```python
   pattern = re.compile(r"\d+")
   pattern.findall("123 456")  # More efficient for multiple operations
   ```

2. **Avoid unnecessary backtracking**:
   ```python
   # Instead of r"a.*z"
   # Use r"a[^z]*z" if possible
   ```

3. **Use non-capturing groups** when you don't need the captured text:
   ```python
   # Instead of r"(pattern)"
   # Use r"(?:pattern)" when you don't need to reference the group
   ```

4. **Be specific** rather than using broad patterns:
   ```python
   # Instead of r".*"
   # Use r"\d+" if you're specifically looking for digits
   ```

5. **Use appropriate anchors** to limit search space:
   ```python
   # Instead of r"pattern"
   # Use r"^pattern$" if you want to match the entire string
   ```
