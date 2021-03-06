from typing import List
from collections import Counter

# https://leetcode.com/problems/permutations-ii/

class Permutation:
    """
    Class representing a single permutation of a collection
    of integers that may contain duplicates.
    """
    def __init__(self, L: List, R: Counter):
        """
        Constuctor. L is the permutation and R is
        a counter of remaining digits. 
        """
        self.L = L
        self.R = R

    def extend(self):
        """
        Create a set of new permutations by extending 
        the existing permutation by each of the remaining
        letters separately.
        """
        perms = []
        R = self.R.copy()
        for letter in R:
            Rn = R.copy()
            Rn[letter] -= 1
            if not Rn[letter]:
                del Rn[letter]
            Ln = self.L + [letter]
            perms += [Permutation(Ln, Rn)]
        return perms

    def permLen(self):
        """
        Get length of permutation. 
        """
        return len(self.L)

def permute(nums: List[int]) -> List[List[int]]:
    """
    Given a collection of distinct integers, return
    all possible permutations.
    """
    L = []
    N = len(nums)
    R = Counter(nums)
    perms = [Permutation(L, R)]
    # Continue to extend each permutation until no letters
    # are left.
    while perms[0].permLen() < N:
        permsn = []
        for perm in perms:
            permsn += perm.extend()
        perms = permsn
    # Represent each permutation as list of int 
    perms = [perm.L for perm in perms]
    return perms

class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        return permute(nums)
