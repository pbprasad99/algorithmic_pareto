"""For a given list of numbers, find n consecutive numbers whose sum equals a given value.

Constraints
The input variable numbers is a list of integers.
The input variable target_sum is an integer.
The input variable n is an integer.
The length of the list numbers is greater than or equal to n.
The integers in the list numbers can be positive, negative, or zero.

est Case #1
Input: {"n": 3, "numbers": [1, 2, 3, 4, 5, 6, -1, -2, 3, 9, 0], "target_sum": 9}
Output: [[2, 3, 4]]
Description: The function is tested with a list that includes positive, negative, and zero values. It finds one sub-array that fulfills the condition.
Test Case #2
Input: {"n": 4, "numbers": [-5, 4, 2, -3, 7, 10, -2, 1], "target_sum": 7}
Output: []
Description: This test case challenges the function with a mixed list of small positive and large negative integers. However, no sub-array of 4 numbers sums to the target value.
Test Case #3
Input: {"n": 3, "numbers": [-10, -20, -30, -40, -50, -60, -70, -80], "target_sum": -150}
Output: [[-40, -50, -60]]
Description: A challenging test with only negative numbers. The function finds one sequence of three numbers whose sum equals the negative target.
"""

def find_consecutive_sum_subarray(numbers, n, target_sum):
    """
    Find all consecutive subarrays of length n in the given list that sum to target_sum.
    
    Args:
        numbers: List of integers
        n: Length of consecutive subarray
        target_sum: Target sum to achieve
        
    Returns:
        List of lists, where each inner list is a subarray of n consecutive elements that sum to target_sum
    """
    result = []
    
    # Check if the list is too short
    if len(numbers) < n:
        return result
    
    # Use sliding window approach
    # First calculate the sum of the first window
    current_sum = sum(numbers[:n])
    
    # Check if the first window matches the target sum
    if current_sum == target_sum:
        result.append(numbers[:n])
    
    # Slide the window through the rest of the array
    for i in range(n, len(numbers)):
        # Update the current sum by removing the element going out of the window
        # and adding the new element coming into the window
        current_sum = current_sum - numbers[i - n] + numbers[i]
        
        # Check if the current window sum matches the target
        if current_sum == target_sum:
            result.append(numbers[i - n + 1:i + 1])
    
    return result

# Test cases
test1 = find_consecutive_sum_subarray([1, 2, 3, 4, 5, 6, -1, -2, 3, 9, 0], 3, 9)
print(test1)  # Expected: [[2, 3, 4]]

test2 = find_consecutive_sum_subarray([-5, 4, 2, -3, 7, 10, -2, 1], 4, 7)
print(test2)  # Expected: []

test3 = find_consecutive_sum_subarray([-10, -20, -30, -40, -50, -60, -70, -80], 3, -150)
print(test3)  # Expected: [[-40, -50, -60]]