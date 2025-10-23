import string

def find_non_repeated_words(sentence1, sentence2):
    """
    Find words that appear in only one of the two sentences, not in both.
    
    Args:
        sentence1: A string representing the first sentence
        sentence2: A string representing the second sentence
        
    Returns:
        A list of words that appear in only one of the sentences
    """
    # Create a translation table to remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    
    # Remove punctuation from sentences (preserving case)
    clean_sentence1 = sentence1.translate(translator)
    clean_sentence2 = sentence2.translate(translator)
    
    # Split the cleaned sentences into words
    words1 = clean_sentence1.split() if clean_sentence1 else []
    words2 = clean_sentence2.split() if clean_sentence2 else []
    
    # Create sets for efficient comparison
    set1 = set(words1)
    set2 = set(words2)
    
    # Find words that appear in only one sentence
    unique_to_s1 = set1 - set2
    unique_to_s2 = set2 - set1
    
    # Collect non-repeated words in order of appearance
    result = []
    
    # Add words from sentence1 that are not in sentence2
    for word in words1:
        if word in unique_to_s1 and word not in result:
            result.append(word)
    
    # Add words from sentence2 that are not in sentence1
    for word in words2:
        if word in unique_to_s2 and word not in result:
            result.append(word)
    
    return result

# Test cases
test_case_1 = ["The cat in the hat", "A cat in a mat"]
test_case_2 = ["Innovation distinguishes between a leader and a follower", 
               "Creativity is thinking up new things, Innovation is doing new things"]
test_case_3 = ["", "The quick brown fox jumps over the lazy dog"]

print(find_non_repeated_words(test_case_1[0], test_case_1[1]))
# Expected: ["The", "hat", "A", "a", "mat"]

print(find_non_repeated_words(test_case_2[0], test_case_2[1]))
# Expected: ["distinguishes", "between", "leader", "and", "follower", "Creativity", "is", "thinking", "up", "new", "things", "doing"]


print(find_non_repeated_words(test_case_3[0], test_case_3[1]))
# Expected: ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]