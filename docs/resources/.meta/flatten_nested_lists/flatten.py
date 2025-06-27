def flatten_list(nested_list):
    """
    Flatten a nested list of any depth into a 1D list.
    
    Args:
        nested_list: A list that may contain nested lists as elements
        
    Returns:
        A flattened 1D list containing all elements in the nested list
    """
    res = []
    for item in nested_list :
        if isinstance(item, list) :
            res.extend(flatten_list(item))
        else :
            res.append(item)
    return res
test_case_1 = [[1, 2, [3, 4], 5], [6], [7, [8, [9, 10]]]]
test_case_2 = [[1, "a", [3.1415, [True, 0]], "b"], [None, [2, [3, "text"]]]]
test_case_3 = [[[[]]], [], [[], [[], [[]]]]]

print(flatten_list(test_case_1))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(flatten_list(test_case_2))  # [1, 'a', 3.1415, True, 0, 'b', None, 2, 3, 'text']
print(flatten_list(test_case_3))  # []