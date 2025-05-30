---
title: Fun Facts about two's complement encoding 
slug: Fun Facts about two's complement encoding 
date: 2025-05-20

tags :
  - C
  - Basics
categories:
  - C
  - Basics
  - Encodings
---

While revisiting my old notes on Standard C , I came across this fun fact: In two’s complement, values like 0xF, 0xFF, and 0xFFFF all represent -1. Let's see why this is and explore some other properties of 2's complement encoding. 

<!-- more -->

## SIgned Vs Unsigned encoding for integers

Most computers use two’s complement to represent negative values. In this system, the most significant bit (MSB) is treated as having a negative weight.

**Unsigned Example:**  
1111 → 8 + 4 + 2 + 1 = 15

**Signed Example:**  
1111 → -8 + 4 + 2 + 1 = -1

This means:  
- 0xF = -1  
- 0xFF = -1  
- 0xFFF = -1  
- 0xFFFF = -1  
…and so on, for all bits set in any size.


For a byte, numbers from 0x00 to 0x7F are positive and have the same encoding in both signed and unsigned (two’s complement) form.


## Range for N-bit Signed Integers

Let us dig a little bit deeper. What could be the the range for an N-Bit Signed Integer.

The Lowest value would be if the Most Significant Bit is set and no other bit is set.

For a 4- bit Integer: 

```
BIT representation        :   1     0     0      0
Postition Value of bits   :  2^3   2^2   2^1    2^0 
Sign                      :  Negative since MSB is set 
Decimal Value             : -8                     
```

The lowest value will always be -(2^(N-1))

Conversely, the highest positive value will be when the MSB is not set and all other bits are set. This is equal to 2^(N-1) -1.

For a 4- bit Integer: 

```
BIT representation        :   0     1     1      1
Postition Value of bits   :  2^3   2^2   2^1    2^0 
Sign                      :  Positive since MSB is not set 
Decimal Value             :  7                     
```

Did you also notice that -(2^(N-1)) + (2^(N-1)-1) = -1?

This is why 0xFFFFF... is always -1 in 2's complement.


## Extension 

In fact, you can represent any N-bit signed integers in N+x bits bits simply by extending the Most Significant Bit x times.

```
	4-bit       8-bit       16-bit              Decimal
	0111        00000111    0000000000000111    +7
	1110        11111110    1111111111111110    -2
```

## Truncation 

An N-bit signed integer can be truncated to N-x bits and hold the same value by removing the Highest Order x Bits excluding the  MSB as long as they match the MSB (Sign Bit).

```
11100  is -4
1100   is -4
100    is -4
10     is NOT -4 . It is -2.   
```

## Getting Two's Complement of a Number

For getting 2's complement of a number you  flip the bits and add 1.

```
4-bit   Decimal 
0011      3       
1100     -4          
1101     -3          #Two's complement of 0011
```

[ As two why this works see Ref 2 below ] 

## Overflow Detection

In 2's complement overflow is not possible when adding numbers with opposite signs. When adding numbers of the same sign, if there is an overflow you will get the wrong sign bit. 

* If both numbers are positive and you get a negative result.

* If both numbers ar negative and you get a positive result.

[Ref 1]

## Why 2's complement?

It's convenient. The same Adders in Hardware can be used for doing addition and subtraction. All you have to do is flip bits and add 1 to get the negative representation of a positive number and vice-versa.

It is also Bijective, which is to say that it can uniquely represent negative integers, positive integers and zero.


## Additional References

1. https://web.archive.org/web/20131031093811/http://www.cs.uwm.edu/~cs151/Bacon/Lecture/HTML/ch03s09.html
2. https://www.cs.cornell.edu/~tomf/notes/cps104/twoscomp.html
