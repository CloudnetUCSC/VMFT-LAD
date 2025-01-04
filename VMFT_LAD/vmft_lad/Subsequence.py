from typing import Tuple
from functools import total_ordering


@total_ordering
class Subsequence:
    """
    Stores subsequences (a tuple of integers) and their hits.
    Subsequences are sorted/compared using the number of hits.
    The number of hits is stored as a negative number to help in sorting (for max heap).
    Hits can only be accessed or incremented.
    """

    def __init__(self, data: Tuple[int, ...]):
        self.data = data
        self._hits = -1  # A subsequence should at least have 1 hit

    # Get hits return the positive value of hits
    def getHits(self):
        return -self._hits

    def incrementHits(self):
        self._hits -= 1

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return self._hits == other.getHits() * (-1)

    def __lt__(self, other):
        return self._hits < other.getHits() * (-1)

    def __str__(self):
        return str(self.data) + " : " + str(self.getHits())
