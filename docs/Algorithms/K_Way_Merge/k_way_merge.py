"""
The same problem but with a different signature :
https://www.geeksforgeeks.org/problems/merge-k-sorted-arrays/1
"""
#User function Template for python3
from typing import List
from heapq import heapify, heappop, heappush
class Solution:
    #Function to merge k sorted arrays.
    def mergeKArrays(self, arr : List[List[int]]) -> List[int]:
        """
        Given k sorted arrays, return a single merged array.
        Input :
         arr : a list of integer arrays
        """
        # return merged list
        len_res = 0
        
        #Priority Queue- min heap
        pq = []
        #Assume that arrays can be of unequal length
        #Initialize min heap
        for array in arr :
            len_res += len(array)
            #Store the current index and a reference to the array for getting the next value in the array
            pq.append((array[0] , 0 , array))

        #heapify pq
        heapify(pq)
        
        #allocate result array
        res = [None] * len_res
        
        #write pointer
        write_ptr = 0 
        #Pick the lowest value from the current choices and write it to res
        while pq :
            curr_val, curr_ptr, curr_arr = heappop(pq)
            res[write_ptr] = curr_val
            if curr_ptr < len(curr_arr) -1  : 
                heappush(pq, (curr_arr[curr_ptr+1] , curr_ptr+1,curr_arr ))
            write_ptr+=1
        return res

if __name__ == "__main__" :
    print( Solution().mergeKArrays([[1,2,3] , [5,6] , [9,9,10]]) )