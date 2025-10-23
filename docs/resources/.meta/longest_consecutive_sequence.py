def longest_consecutive_sequence(nums):
    """
    Find the length of the longest consecutive elements sequence in an unsorted array.
    
    Args:
        nums: List of integers (unsorted)
        
    Returns:
        Length of the longest consecutive sequence
    """
    # Handle empty input
    if not nums:
        return 0
    
    # Create a set for O(1) lookups
    num_set = set(nums)
    
    max_length = 0
    
    # Check each number that could be the start of a sequence
    for num in num_set:
        # Only process numbers that could be the start of a sequence
        # (i.e., num-1 is not in the set)
        if num - 1 not in num_set:
            current_num = num
            current_streak = 1
            
            # Count how long this sequence extends
            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1
            
            # Update the max length if necessary
            max_length = max(max_length, current_streak)
    
    return max_length

# Test cases
print(longest_consecutive_sequence([100, 4, 200, 1, 3, 2]))  # Expected: 4 (the sequence 1,2,3,4)
print(longest_consecutive_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # Expected: 9 (the sequence 0,1,2,3,4,5,6,7,8)
print(longest_consecutive_sequence([]))  # Expected: 0
print(longest_consecutive_sequence([5,6,7,8]))  # Expected: 1