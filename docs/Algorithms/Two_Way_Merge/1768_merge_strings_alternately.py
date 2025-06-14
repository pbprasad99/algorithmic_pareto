"""
A simpler version of the two way merge problem.
All you have to do is pick the next element alternately among the two choices.
The EFFECT can be achieved by simply picking a letter from each array one after the other.
Wrap this up in s while loop runs until either one of the arrays have not finished being read. 
"""
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        
        res = []
        p1,p2 =0,0

        while p1 < len(word1) or p2 < len(word2) :
            if p1 < len(word1) : 
                res.append(word1[p1]) 
                p1+=1
            if p2 < len(word2) : 
                res.append(word2[p2])
                p2+=1
        return "".join(res)