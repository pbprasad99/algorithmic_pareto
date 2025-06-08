# External Sorting

## Defining the problem

Given limited RAM , sort a large file.

## One Solution

Suppose, we have an X GB file and only 2GB RAM where X > 2 

1. Divide the file into X//2  2GB chunks ( FILE_SZ//RAM ).

2. Read each chunk into memory . Sort it and write it back to disk as a part file.

3. Now we have k-way merge problem. You can either run a single k-way merge, or mutliple passes of two way merges to utlimately merge the part files into a single sorted file.


## Additional References
1. https://en.wikipedia.org/wiki/External_sorting