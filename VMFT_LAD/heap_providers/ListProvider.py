from typing import Iterator, List

from vmft_lad.Subsequence import Subsequence
from vmft_lad.IMaxHeapProvider import IMaxHeapProvider


class ListMaxHeapProvider(IMaxHeapProvider):
    """
    A simple list based implementation of the max heap provider.
    Does not store unique subsequences.
    Does not order the heap based on subsequence hits.
    """

    def __init__(self):
        self.max_heap: List[Subsequence] = []

    def initialise(self):
        return

    def push(self, subsequence: Subsequence):
        self.max_heap.append(subsequence)

    def incrementHits(self, subsequence: Subsequence):
        for i in range(len(self.max_heap)):
            if self.max_heap[i].data == subsequence.data:
                self.max_heap[i].incrementHits()
                break

    def remove(self, subsequence: Subsequence):
        for i in range(len(self.max_heap)):
            if self.max_heap[i].data == subsequence.data:
                self.max_heap.pop(i)
                break

    def __iter__(self) -> Iterator[Subsequence]:
        return iter(self.max_heap)

    def __len__(self) -> int:
        return len(self.max_heap)
