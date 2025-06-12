"""
Solution for : https://leetcode.com/problems/find-k-pairs-with-smallest-sums/

The problem statement is confusing. Key informations is that all possible pairs are formed by 
taking one number from first array and combining it with a second number from the second array.
        [1,7,11]
        [2,4,6]
 [ (1,2) , (1,4) (1,6) ,(7,2) , (7,4) , (7,6) , (11,1), (11,2) , (11,7) ]

The problem is asking us , if we sort the above list of tuples by their sum, what would be the first k tuples.

Thoughts :

Do we have to enumerate all pairs? Maybe. If we do that, we can maintain a max heap fo size k. 
In the max heap, keep tuples ( (sum of two elements), (el1, el2))

We can do this :

from heapq import heappop, heappush, heapify 
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        res = []
        ## Quadratic Time Complexity.
        for n1 in nums1 :
            for n2 in nums2 :
                heappush(res,(-1*(n1+n2),(n1,n2)))
                if len(res) > k :
                    heappop(res)
        
        ans = []
        while res : 
            ans.append(heappop(res)[1])
        return ans

But this has a  quadratic run time and will give TLE.

Can we do better ? 
Why yes we can!


Consider :
[1,1,2], nums2 = [1,2,3], k = 3

Isn't this how we are enumerating pairs?
1,1 -> 1,2 -> 1,3
*
1,1 -> 1,2 -> 1,3
*
2,1 -> 2,2 -> 2,3
* 

These look an awful lot like three linked lists. 
We know how to get the next element for each linked list. 
To get the n smallest pairs we just need to run a k-way merge n times. 
(Lets call the number of pairs required n to avoid confusion with the concept of k-way merge.
In k-way merge, k refers to the number of linked lists we are merging )

Lets implement the solution. 
"""

from heapq import heappop,heappush

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        n = k # rename k to n to avoid confusion with out mental model
        pq = []
        #Init pq 
        #In each linked list the first elelement is fixed and from the first array, we take second element from the second array.
        #We will use the index of the first element as tie breaker
        #store the index of second element to get the next element in the same linked list

        for idx, val in enumerate(nums1) :
            heappush(pq,( ( nums1[idx] + nums2[0] ,idx_1,  0) 
            )#  (sum of two elements, index of first element, index of second element )   

        res = []
        
        # Pick the next smallest tuple k times
        while pq and n :
            n-=1
            _,idx_1,idx_2 = heappop(pq) # i is the index of element2 in the tuple
            res.append((nums1[idx_1],nums2[idx_2])
            )
            if idx_2 < len(nums2)-1 :
                heappush(pq,( ( nums1[idx] + nums2[i+1] ,idx_1, idx_2 ) )
                 ) #  (sum of two elements, index of first element, index of second element) 
        return res
