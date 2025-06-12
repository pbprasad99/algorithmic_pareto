# Set Theoretic Notation

!!! warning "AI Generated Content" 

!!! Warning "Refresh Page if math notation is not rendered"

A comprehensive reference for mathematical notation used in set theory, from basic concepts to advanced topics.

## Basic Set Notation

Set theory provides the foundation for modern mathematics through its system of notation for collections and relationships.

### Set Definition and Membership

**Sets** are collections of objects called elements or members. The fundamental relationship is membership.

**Membership**: \\(x \in A\\) means "\\(x\\) is an element of set \\(A\\)" or "\\(x\\) belongs to \\(A\\)."

**Non-membership**: \\(x \notin A\\) means "\\(x\\) is not an element of set \\(A\\)."

**Examples**:
- \\(3 \in \{1, 2, 3, 4\}\\) (3 is in the set)
- \\(5 \notin \{1, 2, 3, 4\}\\) (5 is not in the set)
- \\(\pi \in \mathbb{R}\\) (π is a real number)

### Set Builder Notation

Sets can be defined by listing elements or by describing properties.

**Roster notation**: \\(A = \{1, 2, 3, 4\}\\) lists all elements explicitly.

**Set-builder notation**: \\(A = \{x : P(x)\}\\) or \\(A = \{x \mid P(x)\}\\) means "the set of all \\(x\\) such that property \\(P(x)\\) holds."

**Examples**:
- \\(\{x \in \mathbb{Z} : x^2 < 10\}\\) (integers whose square is less than 10)
- \\(\{x \in \mathbb{R} \mid x > 0\}\\) (positive real numbers)
- \\(\{2n : n \in \mathbb{N}\}\\) (even natural numbers)

### Special Sets

**Empty set**: \\(\emptyset\\) or \\(\{\}\\) contains no elements.

**Universal set**: \\(U\\) or \\(\Omega\\) represents the collection of all objects under consideration in a particular context.

**Singleton set**: \\(\{a\}\\) contains exactly one element \\(a\\).

## Set Relationships

Understanding how sets relate to each other is fundamental to set theory.

### Subset Relations

**Subset**: \\(A \subseteq B\\) means "\\(A\\) is a subset of \\(B\\)" or "every element of \\(A\\) is also in \\(B\\)."

- Formally: \\(\forall x (x \in A \rightarrow x \in B)\\)

**Proper subset**: \\(A \subsetneq B\\) or \\(A \subset B\\) means "\\(A\\) is a proper subset of \\(B\\)" (\\(A \subseteq B\\) and \\(A \neq B\\)).

**Superset**: \\(B \supseteq A\\) means "\\(B\\) is a superset of \\(A\\)" (equivalent to \\(A \subseteq B\\)).

**Proper superset**: \\(B \supsetneq A\\) or \\(B \supset A\\) means "\\(B\\) is a proper superset of \\(A\\)."

**Examples**:
- \\(\{1, 2\} \subseteq \{1, 2, 3\}\\)
- \\(\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}\\)
- \\(\emptyset \subseteq A\\) for any set \\(A\\)

### Set Equality

**Set equality**: \\(A = B\\) means sets \\(A\\) and \\(B\\) have exactly the same elements.

- Equivalent to: \\(A \subseteq B\\) and \\(B \subseteq A\\)

**Set inequality**: \\(A \neq B\\) means sets \\(A\\) and \\(B\\) do not have the same elements.

## Set Operations

Set operations combine or modify sets to create new sets.

### Basic Operations

**Union**: \\(A \cup B\\) is the set of elements in \\(A\\) or \\(B\\) (or both).

- \\(A \cup B = \{x : x \in A \text{ or } x \in B\}\\)

**Intersection**: \\(A \cap B\\) is the set of elements in both \\(A\\) and \\(B\\).

- \\(A \cap B = \{x : x \in A \text{ and } x \in B\}\\)

**Difference**: \\(A \setminus B\\) or \\(A - B\\) is the set of elements in \\(A\\) but not in \\(B\\).

- \\(A \setminus B = \{x : x \in A \text{ and } x \notin B\}\\)

**Complement**: \\(A^c\\) or \\(\overline{A}\\) or \\(A'\\) is the set of elements not in \\(A\\) (relative to some universal set).

- \\(A^c = \{x \in U : x \notin A\}\\)

**Examples**:
- \\(\{1, 2\} \cup \{2, 3\} = \{1, 2, 3\}\\)
- \\(\{1, 2\} \cap \{2, 3\} = \{2\}\\)
- \\(\{1, 2, 3\} \setminus \{2\} = \{1, 3\}\\)

### Disjoint Sets

**Disjoint sets**: \\(A\\) and \\(B\\) are disjoint if \\(A \cap B = \emptyset\\).

**Pairwise disjoint**: A collection of sets is pairwise disjoint if every pair of distinct sets in the collection is disjoint.

### Extended Operations

**Symmetric difference**: \\(A \triangle B\\) or \\(A \oplus B\\) contains elements in exactly one of \\(A\\) or \\(B\\).

- \\(A \triangle B = (A \setminus B) \cup (B \setminus A) = (A \cup B) \setminus (A \cap B)\\)

## Generalized Operations

Set operations can be extended to collections of multiple sets.

### Indexed Families

**Indexed union**: \\(\bigcup_{i \in I} A_i\\) is the union of all sets \\(A_i\\) where \\(i\\) ranges over index set \\(I\\).

- \\(\bigcup_{i \in I} A_i = \{x : \exists i \in I, x \in A_i\}\\)

**Indexed intersection**: \\(\bigcap_{i \in I} A_i\\) is the intersection of all sets \\(A_i\\) where \\(i\\) ranges over index set \\(I\\).

- \\(\bigcap_{i \in I} A_i = \{x : \forall i \in I, x \in A_i\}\\)

**Common notations**:

- \\(\bigcup_{i=1}^{n} A_i = A_1 \cup A_2 \cup \cdots \cup A_n\\)
- \\(\bigcap_{i=1}^{\infty} A_i\\) (intersection of countably many sets)
- \\(\bigcup_{x \in X} A_x\\) (union indexed by elements of set \\(X\\))

### Partition

**Partition**: A partition of set \\(A\\) is a collection of non-empty, pairwise disjoint subsets whose union is \\(A\\).

If \\(\\{A_i\\}_{i \in I}\\) is a partition of \\(A\\), then:

- \\(A_i \neq \emptyset\\) for all \\(i \in I\\)
- \\(A_i \cap A_j = \emptyset\\) for \\(i \neq j\\)
- \\(\bigcup_{i \in I} A_i = A\\)

## Power Sets and Cardinality

These concepts deal with the "size" and structure of sets.

### Power Set

**Power set**: \\(\mathcal{P}(A)\\) or \\(2^A\\) is the set of all subsets of \\(A\\).

- \\(\mathcal{P}(A) = \{X : X \subseteq A\}\\)

**Examples**:
- \\(\mathcal{P}(\{1, 2\}) = \{\emptyset, \{1\}, \{2\}, \{1, 2\}\}\\)
- \\(\mathcal{P}(\emptyset) = \{\emptyset\}\\)

### Cardinality

**Cardinality**: \\(|A|\\) or \\(\\#A\\) or \\(\text{card}(A)\\) represents the number of elements in set \\(A\\).

**Finite sets**: \\(|A| = n\\) for some natural number \\(n\\).

**Infinite cardinalities**:

- \\(|\mathbb{N}| = \aleph_0\\) (aleph-null, countable infinity)
- \\(|\mathbb{R}| = 2^{\aleph_0} = \mathfrak{c}\\) (continuum, uncountable)

**Cardinality relationships**:

- \\(|A| = |B|\\) means \\(A\\) and \\(B\\) have the same cardinality
- \\(|A| \leq |B|\\) means there exists an injection from \\(A\\) to \\(B\\)
- \\(|A| < |B|\\) means \\(|A| \leq |B|\\) and \\(|A| \neq |B|\\)

## Relations and Functions

Relations and functions are special types of sets that describe connections between elements.

### Relations

**Relation**: A relation \\(R\\) from set \\(A\\) to set \\(B\\) is a subset of the Cartesian product \\(A \times B\\).

**Notation**: \\(aRb\\) or \\((a,b) \in R\\) means "\\(a\\) is related to \\(b\\) by relation \\(R\\)."

**Types of relations on a set \\(A\\)**:

- **Reflexive**: \\(\forall a \in A, aRa\\)
- **Symmetric**: \\(\forall a,b \in A, aRb \rightarrow bRa\\)
- **Transitive**: \\(\forall a,b,c \in A, (aRb \land bRc) \rightarrow aRc\\)
- **Antisymmetric**: \\(\forall a,b \in A, (aRb \land bRa) \rightarrow a = b\\)

**Equivalence relation**: A relation that is reflexive, symmetric, and transitive.

**Partial order**: A relation that is reflexive, antisymmetric, and transitive.

### Functions

**Function**: \\(f: A \rightarrow B\\) is a relation where each element in \\(A\\) is related to exactly one element in \\(B\\).

**Function notation**: \\(f(a) = b\\) means "function \\(f\\) maps element \\(a\\) to element \\(b\\)."

**Domain**: \\(\text{dom}(f)\\) is the set of all inputs to function \\(f\\).

**Codomain**: The set \\(B\\) in \\(f: A \rightarrow B\\).

**Range** or **Image**: \\(\text{range}(f) = \{f(a) : a \in A\}\\) is the set of all actual outputs.

**Image of a set**: \\(f[X] = \{f(x) : x \in X\}\\) for \\(X \subseteq A\\).

**Preimage**: \\(f^{-1}[Y] = \{x \in A : f(x) \in Y\}\\) for \\(Y \subseteq B\\).

### Function Properties

**Injective** (one-to-one): \\(\forall a_1, a_2 \in A, f(a_1) = f(a_2) \rightarrow a_1 = a_2\\)

**Surjective** (onto): \\(\forall b \in B, \exists a \in A, f(a) = b\\)

**Bijective**: Both injective and surjective.

**Inverse function**: If \\(f: A \rightarrow B\\) is bijective, then \\(f^{-1}: B \rightarrow A\\) exists.

## Cartesian Products and Tuples

These constructions create new sets from existing ones.

### Cartesian Product

**Cartesian product**: \\(A \times B = \{(a,b) : a \in A \text{ and } b \in B\}\\) is the set of all ordered pairs.

**Higher-order products**:

- \\(A \times B \times C = \{(a,b,c) : a \in A, b \in B, c \in C\}\\)
- \\(A^n = A \times A \times \cdots \times A\\) (\\(n\\) times)

**Examples**:
- \\(\{1,2\} \times \{a,b\} = \{(1,a), (1,b), (2,a), (2,b)\}\\)
- \\(\mathbb{R}^2 = \mathbb{R} \times \mathbb{R}\\) (the plane)

### Tuples and Sequences

**Ordered pair**: \\((a,b)\\) where order matters (\\((a,b) \neq (b,a)\\) unless \\(a = b\\)).

**n-tuple**: \\((a_1, a_2, \ldots, a_n)\\) is an ordered collection of \\(n\\) elements.

**Sequence**: An ordered list, often infinite:

- Finite sequence: \\((a_1, a_2, \ldots, a_n)\\)
- Infinite sequence: \\((a_1, a_2, a_3, \ldots)\\) or \\((a_n)_{n=1}^{\infty}\\)

## Advanced Set Theory Concepts

These concepts appear in more sophisticated mathematical contexts.

### Topology and Closure

**Closure**: \\(\overline{A}\\) or \\(\text{cl}(A)\\) represents the closure of set \\(A\\) in a topological space.

**Interior**: \\(\text{int}(A)\\) or \\(A^\circ\\) represents the interior of set \\(A\\).

**Boundary**: \\(\partial A\\) represents the boundary of set \\(A\\).

### Ordinal and Cardinal Numbers

**Ordinal numbers**: \\(\omega, \omega + 1, \omega \cdot 2, \ldots\\) represent positions in well-ordered sets.

**Cardinal numbers**: \\(\aleph_0, \aleph_1, \aleph_2, \ldots\\) represent sizes of infinite sets.

**Continuum hypothesis**: \\(2^{\aleph_0} = \aleph_1\\) (there is no cardinality strictly between \\(\aleph_0\\) and \\(2^{\aleph_0}\\)).

### Choice and Well-Ordering

**Axiom of Choice**: For any collection of non-empty sets, there exists a choice function that selects one element from each set.

**Well-ordering**: Every non-empty subset has a least element.

**Zorn's Lemma**: If every chain in a partially ordered set has an upper bound, then the set has a maximal element.

## Logical Quantifiers in Set Context

Set theory frequently uses logical notation to express properties precisely.

### Universal and Existential Quantifiers

**Universal quantifier**: \\(\forall x \in A, P(x)\\) means "for all \\(x\\) in \\(A\\), property \\(P(x)\\) holds."

**Existential quantifier**: \\(\exists x \in A, P(x)\\) means "there exists an \\(x\\) in \\(A\\) such that property \\(P(x)\\) holds."

**Unique existence**: \\(\exists! x \in A, P(x)\\) means "there exists a unique \\(x\\) in \\(A\\) such that \\(P(x)\\) holds."

**Examples**:
- \\(\forall x \in \mathbb{R}, x^2 \geq 0\\) (all real numbers have non-negative squares)
- \\(\exists x \in \mathbb{Q}, x^2 = 2\\) is false (no rational number squares to 2)
- \\(\exists! x \in \mathbb{R}, x^3 = 8\\) (exactly one real cube root of 8)

### Logical Connectives

**Conjunction**: \\(P \land Q\\) means "\\(P\\) and \\(Q\\)"

**Disjunction**: \\(P \lor Q\\) means "\\(P\\) or \\(Q\\)"

**Negation**: \\(\neg P\\) means "not \\(P\\)"

**Implication**: \\(P \rightarrow Q\\) means "if \\(P\\) then \\(Q\\)"

**Biconditional**: \\(P \leftrightarrow Q\\) means "\\(P\\) if and only if \\(Q\\)"

## Understanding Complex Set Expressions

Reading complex set-theoretic statements requires understanding how notation combines.

### Parsing Complex Statements

**Multiple operations**: \\(A \cup (B \cap C)\\) means "\\(A\\) union with the intersection of \\(B\\) and \\(C\\)."

**Quantified statements**: \\(\{x \in \mathbb{R} : \forall \epsilon > 0, \exists \delta > 0, |x| < \delta \rightarrow |f(x)| < \epsilon\}\\) describes points where function \\(f\\) approaches 0.

**Nested operations**: \\(\bigcup_{n=1}^{\infty} \bigcap_{k=n}^{\infty} A_k\\) represents the limit superior of a sequence of sets.

### Common Patterns

**Characterizing elements**: Statements like \\(x \in A \leftrightarrow P(x)\\) define set membership by properties.

**Set equality proofs**: To show \\(A = B\\), prove both \\(A \subseteq B\\) and \\(B \subseteq A\\).

**Distributive laws**: \\(A \cap (B \cup C) = (A \cap B) \cup (A \cap C)\\)

This comprehensive guide provides the essential notation for understanding set theory concepts in mathematical literature, from basic membership to advanced topics in modern set theory.