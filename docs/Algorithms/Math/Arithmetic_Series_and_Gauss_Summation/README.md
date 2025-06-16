# Arithmetic Series

An arithmetic series is one in which the difference between any two consecutive terms is constant.


## Gauss' Summation

As the story goes, when Gauss was a schoolboy his teacher gave the class a task of adding the numbers 1..100 and that is when Gauss came up with this insight :

```
#terms for 3 and 4 are ommitted, but you get the picture..

1 2 3 4 5 6 7 8 9 10
|_|_____|_|_____|__| 
  |   1+10=11   |
  |_____|_|_____|
      2+9=11
        |_|
      5+6=11

    
``` 

There are 10//2 11s in this sum. So the sum for first 10 numbers is `10//2 * (10+1)`.


For odd numbers we can compe with the same formula through a different route.Reverse the series and add each individual term of reverserse serioes to the original series :

```
1   2  3  4  5  6  7  8  9  10  11
11 10  9  8  7  6  5  4  3  2   1
----------------------------------
12 12  12 12 12 12 12 12 12 12 12
```
We are multiplying n+1,  n times.  And since we multiplied the entire series sum by two by adding it to itsself, we finally divide by two. 

Therefore for 11 the series sum is `( (11+1)*11 ) // 2`.

So, utlimately the formula is the same for both even and odd number of terms.

More formally, this is the formula for the sum of the first \( n \) natural numbers:

\[
S = 1 + 2 + 3 + \cdots + n = \frac{n(n+1)}{2}
\]


## Generalizing to Any Arithmetic Series

The formula for the sum of an arithmetic series can be applied to any sequence where the difference between consecutive terms is constant.

Given an arithmetic series:

\[
a_1,\, a_2,\, a_3,\, \ldots,\, a_n
\]

where:

- \( a_1 \) is the first term,
- \( d \) is the common difference,
- \( n \) is the number of terms,

the sum \( S \) of the series is:

\[
S = \frac{n}{2} \times (a_1 + a_n)
\]

where \( a_n \) is the last term.

Alternatively, since \( a_n = a_1 + (n-1)d \), the formula can also be written as:

\[
S = \frac{n}{2} \times [2a_1 + (n-1)d]
\]

**Example:**

For the series \( 2,\, 4,\, 6,\, 8 \) :

- \( a_1 = 2 \)
- \( d = 2 \)
- \( n = 4 \)
- \( a_n = 8 \)

Applying the formula:

\[
S = \frac{4}{2} \times (2 + 8) = 2 \times 10 = 20
\]

This formula works for any arithmetic series, not just the sum of the first \( n \) natural numbers.

## Additional Resources

1. https://mathbitsnotebook.com/Algebra2/Sequences/SSGauss.html 

## Practice

??? example "[Arranging Coins](https://leetcode.com/problems/arranging-coins/description/){target="_blank"}"
    ```python
    --8<--
    docs/Algorithms/Math/Arithmetic_Series_and_Gauss_Summation/441_arranging_coins.py
    --8<--
    ```