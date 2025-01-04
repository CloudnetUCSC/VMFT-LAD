import heapq
from typing import List, Set, Tuple
from vmft_lad.IMaxHeapProvider import IMaxHeapProvider
from vmft_lad.Subsequence import Subsequence


class SubsequenceMaxHeap(IMaxHeapProvider):
    """
    Max heap to store benign subsequences in the order of their hits.
    This data structure is used to start matching subsequences from the most frequent ones.
    This also only stores unique subsequences.
    """

    def __init__(self):
        self._heap: List[Subsequence] = []  # Heap to store subsequences
        self._set: Set[Tuple[int, ...]] = (
            set()
        )  # Set to keep track of unique subsequences

    def initialise(self):
        return

    def push(self, subsequence: Subsequence):
        """
        Pushes a subsequence into the heap if it is not already present.
        @param subsequence: Subsequence to be pushed into the heap
        """
        if subsequence.data in self._set:
            return
        heapq.heappush(self._heap, subsequence)
        self._set.add(subsequence.data)

    def incrementHits(self, subsequence: Subsequence):
        """
        Increments the hits of the given subsequence in the heap and updates the heap accordingly to ensure the heap property is maintained.
        @param subsequence: Subsequence whose hits are to be incremented.
        """
        subsequence.incrementHits()
        heapq.heapify(self._heap)

    def remove(self, subsequence: Subsequence):
        """
        Remove the given subsequence from the heap.
        @param subsequence: Subsequence to be removed from the heap.
        """
        self._heap.remove(subsequence)
        heapq.heapify(self._heap)
        self._set.remove(subsequence.data)

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self._heap) + "]"

    def __iter__(self):
        return iter(self._heap)

    def __len__(self):
        return len(self._heap)


if __name__ == "__main__":
    # Test SubsequenceMaxHeap
    sHeap = SubsequenceMaxHeap()
    sHeap.push(Subsequence((1, 2, 3)))
    sHeap.push(Subsequence((1, 2, 3)))
    sHeap.push(Subsequence((1, 4, 4)))
    sHeap.push(Subsequence((1, 3, 5)))
    sHeap.push(Subsequence((1, 3, 4)))

    for i in sHeap:
        if i.data == (1, 3, 5):
            i.incrementHits()
            i.incrementHits()
            i.incrementHits()
            i.incrementHits()
        elif i.data == (1, 3, 4):
            i.incrementHits()
            i.incrementHits()
        elif i.data == (1, 2, 3):
            i.incrementHits()
            i.incrementHits()
            i.incrementHits()
        i.incrementHits()

    print(sHeap)

    for i in range(10):
        sHeap.push(Subsequence((i, i + 1, i + 2)))

    for i in range(10):
        for j in sHeap:
            if j.data == (i, i + 1, i + 2):
                sHeap.incrementHits(j)

    for i in range(10):
        for j in sHeap:
            if j.data == (5, 6, 7):
                sHeap.incrementHits(j)

    for i in range(8):
        for j in sHeap:
            if j.data == (4, 5, 6):
                sHeap.incrementHits(j)
    for i in range(8):
        for j in sHeap:
            if j.data == (9, 10, 11):
                sHeap.incrementHits(j)
    for i in range(7):
        for j in sHeap:
            if j.data == (1, 3, 4):
                sHeap.incrementHits(j)
    for i in range(4):
        for j in sHeap:
            if j.data == (1, 2, 3):
                sHeap.incrementHits(j)

    print(sHeap)

    for i in sHeap:
        print(i)
