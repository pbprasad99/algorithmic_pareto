

# Number Theoretic Notation
  

!!! Question "[From here](https://www.math.uh.edu/~minru/spring11/fundamental-theorem.pdf){target="_blank"}"

    ```
    Lemma. If m | pq and (m,p) = 1, then m | q.
    ```

Vertical Bar is the *divides* symbol.

m | pq means that m divides the product pq, meaning there exists some integer k such that pq = km.

This is called the *gcd notation* :

```(m,p) = 1```

Here it is used to express that m and p are co-prime or relatively prime. Meaning that their GCD is 1 and they share no common factors other than 1.



!!! success "Translation"
    ```
    If m divides pq and m and p are co-prime, then m must divide q.
    ```

Isn't it simple or at least approachable, once you understand what the notation means? 

So, I worked with Claude 4.0 to generate the following guide. I think it did a pretty good job. 

!!! warning "Following Content is AI Generated"


## Basic Number Systems and Sets

Number theory begins with understanding different types of numbers and their standard mathematical notation.

### Standard Number Sets

The foundation of number theory rests on several key number systems, each with specific notation:

**Natural Numbers**: \\(\mathbb{N}\\) represents the set of natural numbers. The exact definition varies by context:

- \\(\mathbb{N} = \{1, 2, 3, 4, \ldots\}\\) (positive integers only)
- \\(\mathbb{N}_0 = \{0, 1, 2, 3, \ldots\}\\) (including zero)
- \\(\mathbb{N}^* = \{1, 2, 3, 4, \ldots\}\\) (explicitly positive)

**Integers**: \\(\mathbb{Z} = \{\ldots, -2, -1, 0, 1, 2, \ldots\}\\) includes all positive and negative whole numbers.

**Rational Numbers**: \\(\mathbb{Q} = \{\frac{a}{b} : a, b \in \mathbb{Z}, b \neq 0\}\\) represents all fractions.

**Real Numbers**: \\(\mathbb{R}\\) encompasses all rational and irrational numbers.

**Complex Numbers**: \\(\mathbb{C} = \{a + bi : a, b \in \mathbb{R}, i^2 = -1\}\\) extends the reals.

### Modular Arithmetic Sets

**Integers modulo n**: The set \\(\mathbb{Z}/n\mathbb{Z} = \{0, 1, 2, \ldots, n-1\}\\) represents equivalence classes under modular arithmetic. Alternative notation \\(\mathbb{Z}_n\\) exists but can create confusion with p-adic integers.

**Units modulo n**: \\((\mathbb{Z}/n\mathbb{Z})^*\\) denotes integers relatively prime to \\(n\\) in the range \\(\{1, 2, \ldots, n-1\}\\).

## Divisibility and Basic Relations

Understanding when one integer divides another forms a cornerstone of number theory.

### Divisibility Notation

The expression \\(a \mid b\\) means "a divides b" or "a is a divisor of b." This indicates that \\(b = ka\\) for some integer \\(k\\).

**Examples**:
- \\(3 \mid 12\\) since \\(12 = 4 \times 3\\)
- \\(5 \mid 35\\) since \\(35 = 7 \times 5\\)

The negation \\(a \nmid b\\) means "a does not divide b."

### Greatest Common Divisor (GCD)

The greatest common divisor has several notational conventions. The most unambiguous is \\(\gcd(a,b)\\), though traditional mathematics sometimes uses \\((a,b)\\).

**Key Properties**:
- \\(\gcd(a,b) = \gcd(b, a \bmod b)\\) (Euclidean algorithm)
- \\(\gcd(a,b) \cdot \text{lcm}(a,b) = ab\\)

**Examples**:
- \\(\gcd(12, 18) = 6\\)
- \\(\gcd(17, 19) = 1\\) (relatively prime)

### Least Common Multiple (LCM)

The least common multiple uses \\(\text{lcm}(a,b)\\) or traditional bracket notation \\([a,b]\\).

**Examples**:
- \\(\text{lcm}(12, 18) = 36\\)
- \\(\text{lcm}(4, 6) = 12\\)

## Prime Numbers and Factorization

Prime numbers serve as the building blocks of all integers through unique factorization.

### Prime Notation and Factorization

Individual primes are typically denoted by lowercase \\(p\\), with subscripts for distinct primes: \\(p_1, p_2, \ldots, p_k\\).

**Fundamental Theorem of Arithmetic**: Every integer \\(n > 1\\) has a unique prime factorization:
\\[n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}\\]

where \\(p_1 < p_2 < \cdots < p_k\\) are distinct primes and \\(e_i \geq 1\\).

**Examples**:
- \\(12 = 2^2 \cdot 3^1\\)
- \\(100 = 2^2 \cdot 5^2\\)

### Prime-Related Functions

**Prime counting function**: \\(\pi(x)\\) counts primes up to \\(x\\)
- \\(\pi(10) = 4\\) (primes: 2, 3, 5, 7)

**Number of prime factors**: 
- \\(\Omega(n)\\) counts prime factors with multiplicity
- \\(\omega(n)\\) counts distinct prime factors

**Examples**:
- \\(\Omega(12) = 3\\) since \\(12 = 2^2 \cdot 3\\)
- \\(\omega(12) = 2\\) since 12 has two distinct prime factors

## Congruences and Modular Arithmetic

Congruences provide a powerful framework for studying integer relationships.

### Congruence Notation

The fundamental congruence relation \\(a \equiv b \pmod{n}\\) means \\(n \mid (a-b)\\).

**Standard form**: \\(a \equiv b \pmod{n}\\) with parentheses around the modulus.

**Examples**:
- \\(13 \equiv 1 \pmod{12}\\) since \\(12 \mid (13-1)\\)
- \\(25 \equiv 4 \pmod{7}\\) since \\(7 \mid (25-4)\\)

**Key properties**:
- **Reflexive**: \\(a \equiv a \pmod{n}\\)
- **Symmetric**: If \\(a \equiv b \pmod{n}\\), then \\(b \equiv a \pmod{n}\\)
- **Transitive**: If \\(a \equiv b \pmod{n}\\) and \\(b \equiv c \pmod{n}\\), then \\(a \equiv c \pmod{n}\\)

### Modular Arithmetic Operations

Operations preserve congruences:
- \\((a + b) \bmod n\\)
- \\((a \cdot b) \bmod n\\)
- \\(a^k \bmod n\\)

**Multiplicative inverse**: \\(a^{-1} \pmod{n}\\) exists when \\(\gcd(a,n) = 1\\).

**Example**: \\(3^{-1} \equiv 4 \pmod{11}\\) since \\(3 \cdot 4 \equiv 1 \pmod{11}\\).

## Euler's Totient Function

Euler's totient function counts integers relatively prime to a given number.

### Definition and Notation

\\(\phi(n)\\) (or \\(\varphi(n)\\)) equals the number of positive integers less than or equal to \\(n\\) that are relatively prime to \\(n\\).

**Formula for prime powers**: If \\(p\\) is prime, then:
- \\(\phi(p) = p - 1\\)
- \\(\phi(p^k) = p^k - p^{k-1} = p^{k-1}(p-1)\\)

**General formula**: For \\(n\\) with prime factorization \\(n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}\\):
\\[\phi(n) = n \prod_{i=1}^{k} \left(1 - \frac{1}{p_i}\right)\\]

**Examples**:
- \\(\phi(9) = 6\\) (numbers 1, 2, 4, 5, 7, 8 are relatively prime to 9)
- \\(\phi(12) = 4\\) (numbers 1, 5, 7, 11 are relatively prime to 12)

### Euler's Theorem

For \\(\gcd(a,n) = 1\\): \\(a^{\phi(n)} \equiv 1 \pmod{n}\\)

**Fermat's Little Theorem** (special case): For prime \\(p\\) and \\(\gcd(a,p) = 1\\): \\(a^{p-1} \equiv 1 \pmod{p}\\)

## Floor and Ceiling Functions

These functions convert real numbers to integers with specific rounding behavior.

### Floor Function

\\(\lfloor x \rfloor\\) gives the greatest integer less than or equal to \\(x\\).

**Examples**:
- \\(\lfloor 3.7 \rfloor = 3\\)
- \\(\lfloor -2.3 \rfloor = -3\\)
- \\(\lfloor 5 \rfloor = 5\\)

### Ceiling Function

\\(\lceil x \rceil\\) gives the smallest integer greater than or equal to \\(x\\).

**Examples**:
- \\(\lceil 3.2 \rceil = 4\\)
- \\(\lceil -2.3 \rceil = -2\\)
- \\(\lceil 5 \rceil = 5\\)

### Applications in Number Theory

**Counting divisors**: The number of multiples of \\(d\\) up to \\(n\\) is \\(\lfloor n/d \rfloor\\).

**Division algorithm**: For integers \\(a\\) and \\(b > 0\\): \\(a = bq + r\\) where \\(q = \lfloor a/b \rfloor\\) and \\(0 \leq r < b\\).

## Summation and Product Notation

These operators handle collections of terms systematically.

### Summation Over Divisors

A fundamental pattern in number theory involves summing over all divisors of an integer.

**Notation**: \\(\sum_{d \mid n} f(d)\\) means sum \\(f(d)\\) over all positive divisors \\(d\\) of \\(n\\).

**Examples**:
- \\(\sum_{d \mid n} 1 = d(n)\\) (number of divisors)
- \\(\sum_{d \mid n} d = \sigma(n)\\) (sum of divisors)
- \\(\sum_{d \mid n} \phi(d) = n\\) (fundamental identity)

### Summation Over Primes

**Examples**:
- \\(\sum_{p \leq x} \frac{1}{p}\\) (sum of reciprocals of primes up to \\(x\\))
- \\(\sum_{\substack{p \text{ prime} \\ p \equiv 1 \pmod{4}}} \frac{1}{p^s}\\) (conditional summation)

### Product Notation

**Euler product formula**: 
\\[\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} = \prod_{p \text{ prime}} \frac{1}{1-p^{-s}}\\]

**Totient function product**:
\\[\phi(n) = n \prod_{\substack{p \text{ prime} \\ p \mid n}} \left(1 - \frac{1}{p}\right)\\]

## Asymptotic Notation

Asymptotic analysis describes the growth behavior of functions as their arguments approach infinity.

### Big O Family (Bachmann-Landau Notation)

**Big O**: \\(f(n) = O(g(n))\\) means \\(f\\) grows at most as fast as \\(g\\).
- Formally: \\(\exists c > 0, n_0\\) such that \\(|f(n)| \leq c|g(n)|\\) for all \\(n \geq n_0\\)

**Big Omega**: \\(f(n) = \Omega(g(n))\\) means \\(f\\) grows at least as fast as \\(g\\).

**Big Theta**: \\(f(n) = \Theta(g(n))\\) means \\(f\\) and \\(g\\) have the same growth rate.

**Little o**: \\(f(n) = o(g(n))\\) means \\(f\\) grows strictly slower than \\(g\\).

**Asymptotic equivalence**: \\(f(n) \sim g(n)\\) means \\(\lim_{n \to \infty} \frac{f(n)}{g(n)} = 1\\).

### Applications in Number Theory

**Prime Number Theorem**: \\(\pi(x) \sim \frac{x}{\ln x}\\)

**Divisor function**: \\(d(n) = O(n^{\epsilon})\\) for any \\(\epsilon > 0\\)

**Average order of Euler's totient**: \\(\sum_{n \leq x} \phi(n) \sim \frac{3x^2}{\pi^2}\\)

## Advanced Number Theory Symbols

Specialized symbols appear in deeper number theory topics.

### Legendre Symbol

For odd prime \\(p\\) and integer \\(a\\), the Legendre symbol \\(\left(\frac{a}{p}\right)\\) indicates quadratic residue status:

- \\(\left(\frac{a}{p}\right) = 1\\) if \\(a\\) is a quadratic residue modulo \\(p\\)
- \\(\left(\frac{a}{p}\right) = -1\\) if \\(a\\) is a quadratic non-residue modulo \\(p\\)  
- \\(\left(\frac{a}{p}\right) = 0\\) if \\(p \mid a\\)

**Example**: \\(\left(\frac{2}{7}\right) = 1\\) since \\(3^2 \equiv 2 \pmod{7}\\).

### Jacobi Symbol

The Jacobi symbol \\(\left(\frac{a}{n}\right)\\) extends the Legendre symbol to odd composite integers \\(n\\).

For \\(n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}\\):
\\[\left(\frac{a}{n}\right) = \prod_{i=1}^{k} \left(\frac{a}{p_i}\right)^{e_i}\\]

### Quadratic Reciprocity

For distinct odd primes \\(p\\) and \\(q\\):
\\[\left(\frac{p}{q}\right)\left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2} \cdot \frac{q-1}{2}}\\]

### Arithmetic Functions

**Möbius function**: \\(\mu(n)\\) equals:
- \\(1\\) if \\(n\\) is a square-free positive integer with even number of prime factors
- \\(-1\\) if \\(n\\) is a square-free positive integer with odd number of prime factors  
- \\(0\\) if \\(n\\) has a squared prime factor

**Von Mangoldt function**: \\(\Lambda(n)\\) equals \\(\ln p\\) if \\(n = p^k\\) for prime \\(p\\), and \\(0\\) otherwise.

**Dirichlet characters**: \\(\chi(n)\\) are completely multiplicative functions modulo some integer.

## Understanding Mathematical Expressions

## Understanding Mathematical Expressions

When reading number theory texts, you'll encounter mathematical expressions that combine multiple notations. Here are some common patterns:

### Complex Expressions

**Multiplicative functions**: An expression like \\(\sum_{d \mid n} \mu(d) f(n/d)\\) means "sum over all divisors \\(d\\) of \\(n\\), the product of the Möbius function \\(\mu(d)\\) and \\(f(n/d)\\)."

**Conditional sums**: \\(\sum_{\substack{p \leq x \\ p \equiv 1 \pmod{4}}} \frac{1}{p}\\) means "sum \\(\frac{1}{p}\\) over all primes \\(p\\) up to \\(x\\) that are congruent to 1 modulo 4."

**Product formulas**: \\(\prod_{p \mid n} \left(1 + \frac{1}{p}\right)\\) means "take the product over all primes \\(p\\) that divide \\(n\\) of the expression \\(\left(1 + \frac{1}{p}\right)\\)."

### Reading Order and Precedence

Mathematical expressions follow standard precedence rules:
1. Exponents and function applications (like \\(\phi(n)\\))
2. Multiplication and division
3. Addition and subtraction
4. Relations (like \\(\equiv\\), \\(\mid\\), \\(<\\))

**Example**: \\(a^{\phi(n)} \equiv 1 \pmod{n}\\) reads as "(\\(a\\) raised to the power \\(\phi(n)\\)) is congruent to 1 modulo \\(n\\)."

This comprehensive guide provides the foundational notation needed for understanding number theory concepts in academic literature and mathematical texts.