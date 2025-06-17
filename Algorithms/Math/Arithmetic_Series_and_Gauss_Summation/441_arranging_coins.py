"""
Solution for : https://leetcode.com/problems/arranging-coins/description/

Ref : https://mathbitsnotebook.com/Algebra2/Sequences/SSGauss.html

#Gauss summation
1 + 2 + 3 + 4
5 + 5  = (x+1)*x//2 = 4(5) //2 # x = 3
1+ 2 + 3 + 4 + 5
6 + 6 +3   = (6*5)//2 = 15 # x = 5        

Find x which is closest to n using bisect left
   Question : for this x is gauss summation less than n. 

lo could be equal to n -> return lo
else return lo -1
"""
class Solution:
    @staticmethod
    def is_less(x,n) :
        """
        Is gauss sum less than n 
        """
        return ( (x*(x+1))//2 ) < n

    def arrangeCoins(self, n: int) -> int:
        lo,hi = 1, n+1
        while lo < hi :
            mid = (lo+hi)//2
            #print(lo,hi,mid)
            if self.is_less(mid,n) :
                lo = mid+1
            else :  
                hi = mid 
        if lo*(lo+1)//2 == n :
            return lo
        else :
            return lo-1 
