# Introduction

Array partitioning is the problem of rearranging the elements of an array according to some predicate. 

We are interested here in array partitioning schemes usually applied in quicksort, particularly Hoare's and Lomuto's partitioning schemes. These are ***two way partitioning*** schemes, which is to say that they have a binary predicate which could place elements in either left or right partitions based on comparison with a pivot value. There are different ways of implementing two way paritioning based on how you define the predicate. We will see this in some depth while understanding Hoare Partitioning.

If we instead define a ternary predicate which puts an element in one of three partitions : left , middle or right based on comparison with a pivot value, it is called ***three way partitioning***. All the duplicates are grouped into a middle partition. 
Three way partitioning is also called the Dutch National Flag Problem, because the flag has three color bands. There are again different algorithms for doing this, one of which is Djikstra's, who was the one to name this as the Dutch National Flag problem. On the same pattern, the two way partitioning problem is sometimes called the Polish National Flag problem, because that flag has two color bands.


Once you understand Partitioning you get two other Algorithms for free : Quicksort and Quickselect.

Paritioning Schemes are the actual meat of the Quicksort (and Quickselect)  algorithms. What makes Quicksort so interesting is that it can be implemented in slightly different ways with very different performance characteritics using any of these partitioning schemes. This is why Quicksort is not really a single algorithm but a family of algorithms and is a research area by itself in Computer Science.
