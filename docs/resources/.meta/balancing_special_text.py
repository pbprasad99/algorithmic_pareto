"""Given a unique text that consists of characters [a-j] & numbers [0-9], the text is unique because, for every character in the text, its corresponding number must be present.


The mapping is as follows: 'a' ↔ 0, 'b' ↔ 1, 'c' ↔ 2, 'd' ↔ 3, 'e' ↔ 4, 'f' ↔ 5, 'g' ↔ 6, 'h' ↔ 7, 'i' ↔ 8, 'j' ↔ 9.


For example, 'bj19' is balanced as 'b' has corresponding number '1' & 'j' has corresponding number '9'. In contrast, the example 'abc1' is unbalanced as it is missing the digits that should correspond to 'a' and 'c' (i.e., '0' and '2'). Also, the example 'd345' is unbalanced as it is missing the corresponding letters for the digits '4' and '5', which are 'e' and 'f'.


Count the number of additional characters/digits that need to be added to balance the given text.

Constraints
The input variable text is a string.
The characters in the text can only be lowercase letters from 'a' to 'j' and digits from '0' to '9'.
The length of the text can be any positive integer.

Test Case #1
Input: "bj19d345"
Output: 4
Description: The text ""bj19d345"" contains the pairs ""b-1"" and ""j-9"", but is missing ""a"", ""c"", ""e"", and ""f"" which correspond to the digits ""0"", ""2"", ""4"", and ""5"", thus 4 additional characters are needed.
Test Case #2
Input: "a0f5h7"
Output: 3
Description: The text ""a0f5h7"" has the pairs ""a-0"", ""f-5"", and ""h-7"". The corresponding letters ""b-1"", ""c-2"", and ""e-4"" are missing, thus 3 additional characters are needed.
Test Case #3
Input: "a1f4i7"
Output: 6
Description: The text ""a1f4i7"" balances the pairs ""a-1"" and ""f-4"". The missing counterparts are ""0"" for "a", ""b"" for "1", ""5"" for "f", ""e"" for "4", ""8"" for "i", and ""h"" for "7", hence a total of 6 additional characters are needed."""
def count_to_balance(text):
    """
    Counts the number of additional characters/digits needed to balance the text.

    Args:
        text: The input string.

    Returns:
        The number of additional characters/digits needed.
    """
    char_present = [False] * 10
    digit_present = [False] * 10

    # Mark presence of characters and digits
    for char in text:
        if 'a' <= char <= 'j':
            char_present[ord(char) - ord('a')] = True
        elif '0' <= char <= '9':
            digit_present[int(char)] = True

    # Count missing counterparts
    missing_count = 0
    for i in range(10):
        if char_present[i] and not digit_present[i]:
            missing_count += 1
        elif not char_present[i] and digit_present[i]:
            missing_count += 1

    return missing_count

# Test cases
print(count_to_balance("bj19d345"))  # Expected output: 4
print(count_to_balance("a0f5h7"))    # Expected output: 3
print(count_to_balance("a1f4i7"))    # Expected output: 6
