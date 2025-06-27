def find_unique_values(input_list):
    """
    Find unique values in a list of integers while preserving the original order.
    
    Args:
        input_list: A list of integers, possibly containing duplicates
        
    Returns:
        A list of unique integers in the same order as they first appear in the input list
    """
    # Create a set to track seen values (for O(1) lookups)
    seen = set()
    # Create a result list to maintain order
    result = []
    
    for num in input_list:
        # If we haven't seen this number before
        if num not in seen:
            # Add it to our result list
            result.append(num)
            # Mark it as seen
            seen.add(num)
    
    return result

# Test cases
test_case_1 = [5, 1, -1, 2, 5, 1, 2]
test_case_2 = [0, -1, 0, 0, 2, 2, -3, -3, -3]
test_case_3 = [-100, 100, 200, -100, 500, 100]

print(find_unique_values(test_case_1))  # [5, 1, -1, 2]
print(find_unique_values(test_case_2))  # [0, -1, 2, -3]
print(find_unique_values(test_case_3))  # [-100, 100, 200, 500]