from typing import List

def merge_two(arr1 :  List[int], arr2 : List[int]) -> List[int] :
    """
    Given two arrays sorted in non decreasing order, return a merged array 
    """

    m, n = len(arr1) , len(arr2)

    res = [0]*(m+n)

    p1,p2,p3 = 0,0,0

    while p1 < m  and p2 < n  :

        if arr1[p1] < arr2[p2] : 
            res[p3] = arr1[p1]
            p3+=1
            p1+=1
        else :
            res[p3] = arr2[p2]
            p3+=1
            p2+=1
        
        
    while p1 < m :
        res[p3] = arr1[p1]
        p1+=1
        p3+=1

    while p2 < n :
        res[p3] = arr2[p2]
        p2+=1
        p3+=1

    return res


if __name__ == "__main__" :
    print(merge_two([4,5,7] , [3,6,7,8]))
    print(merge_two([4,5,7] , [3,6]))
    print(merge_two([] , [1,2,3]))
    print( merge_two( [1, 2, 2, 5] , [2, 3, 4, 4] ) ) # [1, 2, 2, 2, 3, 4, 4, 5]
    print( merge_two( [1, 3, 5, 7] , [2, 4, 6, 8] ) ) # [1, 2, 3, 4, 5, 6, 7, 8]


            
