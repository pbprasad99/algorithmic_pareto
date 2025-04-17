# Defining the problem

Let us consider the simplaest case, that of an array of integers.

Given an array of integers, rearrange the elements such that the left part contains elements less than or equal to a pivot value and the right part contains values greater than the pivot value.

# The Algorithm

The Lomuto partition fixes uses two forward iterators to maintains two invariants :

[lo,s) contains only elements less than or equal to the pivot.  # Left closed Right open interval

[s,f) contains elements larger than the pivot.      # Left closed right open interval

Usually, pivot is fixed at hi. 

Initial conditions are :

s, f = 0,0

Both invariants are trivially true initially.

During execution :

```

[---<=pivot----|--->pivot------|---Unexamined---|pivot] 
lo              s               f                    hi 

```

s and f can be thought of as slow and fast pointers with s at the write position and f at the read position.

The algorithm is 

```
def partition(arr,lo,hi) :
    s = lo
    pivot = arr[hi]
    for f in range(lo,hi+1) : 
         if arr[f] <= pivot : 
              arr[s],arr[f] = arr[f],arr[s] #swap s and f
              s+=1
    return s-1      
```

Since [s,f] is a half closed interval, it is empty if  s and f are equal. If there is a gap, this interval is gauranteed to only contain elements greater than pivot, since a gap INCREASES as a result of f pointing to a value less than or equal to the pivot and s pointing to a value greater than pivot,  in the first place.

Dry Run :

```

General case :
     [ 1,  4,  7,  3,  1,  4 ]
0      sf                      # Initial condition, pivot = 4, arr[f] <= 4 is True,  s will be swapped with f and both will move ahead
1          sf                  # arr[f] <= 4 , swap s with f and move both ahead
2              sf              # arr[f] <=4 is False, s stays where it is and only f moves ahead
3              s  f            # arr[f] <=4 is True, swap s with f and move both ahead
4    [ 1,  4,  3,  7,  1,  4 ]
                   s   f       # arr[f] <=4 is True, swap s with f and move both ahead
5    [ 1,  4,  3,  1,  7,  4 ] # arr[f] <=4 is True, swap s with f and move both ahead
                       s   f
6    [ 1,  4,  3,  1,  4,  7 ] # arr[f] <=4 is True, swap s with f and move both ahead
                           s   # For loop ends
Return s -1

Only one element :
  [4]
0  sf      #arr[f] <= f is True, swap s with f and move both ahead
1    sf
Return s-1

Sorted array 
  [1,2,3]
0  sf           
1    sf
2      sf
3        s

return s-1

Reverse sorted array :
  [ 3, 2, 1 ]
0   sf               #Initial conditions, arr[s] <= 1 is False, only f will move ahead
1   s  f             #arr[s] <= 1 is False, only f will move ahead          
2   s     f          #arr[s] <= 1 is True, s and f will be swapped and both will move ahead 
3 [ 1, 2, 3 ]
       s     f       #for loop ends
return s -1 

Reverse sorted array with duplicate keys:
[3, 2 ,1, 1]
 s     f
[1, 2 ,3, 1]
    s     f
[1, 1 ,3, 2]
       s     f   # for loop ends, 
return s-1 

Duplicate keys :
[1 , 1, 1, 1]
             sf
return s-1
```


# Variant Implementation

We could redefine our problem statement slightly : Given an array of integers, rearrange the elements such that the left part contains elements less than or equal to a pivot value and the right part contains values greater than the pivot value.

[lo,s) only contains elements strictly less than pivot
[s,f)  contains elements equal to or greater than pivot.

Initial conditions are :

s, f = 0,0

Both invariants are trivially true initially.

During execution :

```

[---<=pivot----|--->pivot------|---Unexamined---|pivot] 
lo              s               f                    hi 

```
The algorithm is 

```
def partition(arr,lo,hi) :
    s = lo
    pivot = arr[hi]
    # The range might as well be range(lo,hi+1). It would make no difference except one extra redundant comparsion.
    for f in range(lo,hi) : 
         if arr[f] < pivot : 
              arr[s],arr[f] = arr[f],arr[s] #swap s and f
              s+=1
    arr[s],arr[hi] = arr[hi],arr[s]
    return s      
```

 
When for loop exits, s is positioned at the sorted position of pivot.
We swap pivot with s and return s.

```
[ 1,  4,  7,  3,  1,  4 ]
      s       f             # arr[f] < pivot is True, s and f will be swapped and both will move ahead.
[ 1,  3,  7,  4,  1,  4 ]    
          s       f
[ 1,  3,  1,  4,  7,  4 ]
              s       f
[ 1,  3,  1,  4,  7,  4 ]
                  s       f  # for loop ends
[ 1,  3,  1,  4,  4,  7 ]
                  s       f  # FInally Swap s with f
Return s 


Reverse sorted array :
  [ 3, 2, 1 ]
    s        f 
  [ 1, 2, 3 ]
    s        f
return s

Reverse sorted array with duplicate keys:
[3, 2 ,1, 1]
 s          f

return s 

Duplicate keys :
1  1  1  1 
s          f #swap s[0] with s[-1]
return s 

```

The two implementations behave differently when it comes to duplicate keys :

The first implementation puts one instance of the pivot value in the LAST sorted position.
The second implementation puts one instance of the pivot value in the FIRST sorted position.

# Additional Resources
https://www.cs.virginia.edu/~horton/cs4102/page4/files/06-ch6-sorting.ppt.pdf


https://iq.opengenus.org/lomuto-partition-scheme/


https://www.stepanovpapers.com/PAM3-partition_notes.pdf


https://dlang.org/blog/2020/05/14/lomutos-comeback/


https://nicholasvadivelu.com/2021/01/11/array-partition/


https://cs-notes.gitbook.io/algorithm-notes/outline/overview-2/quick-sort