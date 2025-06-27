"""Given a 2D array of user IDs, find the number of friends a user has. Note that users can have none or multiple friends.

Constraints
The input variable user_ids is a 2D array of user IDs.
Each element in the user_ids array is a list of integers representing the user IDs.
The user IDs can be any positive or negative integer value.
The user_ids array can have any number of rows and columns.
The user IDs within each row can be in any order.
The user_ids array can contain duplicate user IDs.
The output variable is a dictionary (Dict[int, int]) where the keys are the user IDs and the values are the count of friends for each user.
Test Case #1
Input: [[4, -3, 15], [15, 22, 4], [-3, 4, 22]]
Output: {"4": 3, "-3": 2, "15": 2, "22": 2}
Description: This test case checks the function"s ability to count the frequency of user IDs in a 2D array with both positive and negative integers and repeated elements.
Test Case #2
Input: [[3, 7, 8, 7], [8, 3], [7, 8, 7, 3]]
Output: {"3": 3, "7": 4, "8": 3}
Description: The function is tested against a 2D array containing multiple duplicate values and varying row lengths to ensure accurate counting.
Test Case #3
Input: [[-10, 20], [30, -10], [20, 30], [20, -10]]
Output: {"20": 3, "30": 2, "-10": 3}
Description: This case provides mixed positive and negative user IDs with certain IDs repeating across different rows to examine if the function can correctly tally the occurrences.

Can you xplain what the question is asking for?"""

def count_friends(user_ids):
    """
    Count the number of friends each user has based on the given 2D array.
    
    Args:
        user_ids: A 2D array where each inner array represents a friend group
        
    Returns:
        A dictionary mapping each user ID to their number of unique friends
    """
    # Dictionary to store each user's set of friends
    friends = {}
    
    # Process each friend group
    for group in user_ids:
        # Create a set of unique users in this group
        unique_users = set(group)
        
        # Update each user's friend list
        for user in unique_users:
            if user not in friends:
                friends[user] = set()
            
            # Add all other users in this group as friends
            for friend in unique_users:
                if friend != user:  # Don't count self as friend
                    friends[user].add(friend)
    
    # Convert sets of friends to counts
    friend_counts = {str(user): len(friend_set) for user, friend_set in friends.items()}
    
    return friend_counts

# Test cases
print(count_friends([[4, -3, 15], [15, 22, 4], [-3, 4, 22]]))
print(count_friends([[3, 7, 8, 7], [8, 3], [7, 8, 7, 3]]))
print(count_friends([[-10, 20], [30, -10], [20, 30], [20, -10]]))