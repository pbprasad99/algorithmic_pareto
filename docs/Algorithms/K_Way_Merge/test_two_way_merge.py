"""
Unit Tests for Two way merge.

# Aside : See these for an introduction to pytest : https://realpython.com/pytest-python-testing/
              https://gist.github.com/kwmiebach/3fd49612ef7a52b5ce3a
"""
import pytest
from two_way_merge import merge_two 


# --- Test Cases ---

def test_merge_basic():
    """Tests merging two non-empty lists."""
    arr1 = [1, 3, 5, 7]
    arr2 = [2, 4, 6, 8]
    expected = [1, 2, 3, 4, 5, 6, 7, 8]
    # Note: The original buggy code might return [1, 2, 3, 4, 5, 6, 7, 9]
    assert merge_two(arr1, arr2) == expected

def test_merge_empty_first():
    """Tests merging when the first list is empty."""
    arr1 = []
    arr2 = [2, 4, 6]
    expected = [2, 4, 6]
    assert merge_two(arr1, arr2) == expected
    # Test swap logic too
    assert merge_two(arr2, arr1) == expected

def test_merge_empty_second():
    """Tests merging when the second list is empty."""
    arr1 = [1, 3, 5]
    arr2 = []
    expected = [1, 3, 5]
    assert merge_two(arr1, arr2) == expected
    # Test swap logic too
    assert merge_two(arr2, arr1) == expected

def test_merge_both_empty():
    """Tests merging when both lists are empty."""
    arr1 = []
    arr2 = []
    expected = []
    assert merge_two(arr1, arr2) == expected

def test_merge_duplicates():
    """Tests merging lists with duplicate numbers."""
    arr1 = [1, 2, 2, 5]
    arr2 = [2, 3, 4, 4]
    expected = [1, 2, 2, 2, 3, 4, 4, 5]
    # Note: Original buggy code might return [1, 2, 2, 2, 3, 4, 4, 9]
    assert merge_two(arr1, arr2) == expected

def test_merge_duplicates_across_lists():
    """Tests merging lists where duplicates exist between lists."""
    arr1 = [1, 3, 5]
    arr2 = [1, 3, 5]
    expected = [1, 1, 3, 3, 5, 5]
    # Note: Original buggy code might return [1, 1, 3, 3, 5, 9]
    assert merge_two(arr1, arr2) == expected

def test_merge_interleaved():
    """Tests merging lists with highly interleaved numbers."""
    arr1 = [1, 4, 5, 8]
    arr2 = [2, 3, 6, 7]
    expected = [1, 2, 3, 4, 5, 6, 7, 8]
    # Note: Original buggy code might return [1, 2, 3, 4, 5, 6, 7, 9]
    assert merge_two(arr1, arr2) == expected

def test_merge_one_list_much_shorter():
    """Tests merging when one list is significantly shorter."""
    arr1 = [1, 2, 10, 11, 12]
    arr2 = [3, 4]
    expected = [1, 2, 3, 4, 10, 11, 12]
    # Note: Original buggy code might return [1, 2, 3, 4, 10, 11, 9]
    assert merge_two(arr1, arr2) == expected
    # Test swap logic too
    assert merge_two(arr2, arr1) == expected # Should give same result

def test_merge_all_elements_smaller():
    """Tests merging when all elements of one list are smaller than the other."""
    arr1 = [1, 2, 3]
    arr2 = [4, 5, 6]
    expected = [1, 2, 3, 4, 5, 6]
    # Note: Original buggy code might return [1, 2, 3, 4, 5, 9]
    assert merge_two(arr1, arr2) == expected
    # Test swap logic too
    assert merge_two(arr2, arr1) == expected # Should give same result

def test_merge_negative_numbers():
    """Tests merging lists with negative numbers."""
    arr1 = [-5, -1, 0, 10]
    arr2 = [-3, -2, 8, 12]
    expected = [-5, -3, -2, -1, 0, 8, 10, 12]
    # Note: Original buggy code might return [-5, -3, -2, -1, 0, 8, 10, 9]
    assert merge_two(arr1, arr2) == expected

def test_merge_single_element_lists():
    """Tests merging lists with single elements."""
    arr1 = [5]
    arr2 = [2]
    expected = [2, 5]
    # Note: Original buggy code might return [2, 9] due to off-by-one loop
    assert merge_two(arr1, arr2) == expected
    assert merge_two(arr2, arr1) == expected