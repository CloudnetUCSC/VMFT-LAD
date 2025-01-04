from abc import ABC, abstractmethod
from typing import Iterator

from .Subsequence import Subsequence


class IMaxHeapProvider(ABC):
    """
    Interface for max heap provider.
    The max heap provider is responsible for providing a max heap to store unique subsequences in the order of their hits.
    """

    @abstractmethod
    def initialise(self):
        """
        Code to initialise the max heap provider.
        This is invoked once before the detection process starts.
        """
        pass

    @abstractmethod
    def push(self, subsequence: Subsequence):
        """
        Pushes a subsequence into the max heap if it is not already present.
        @param subsequence: Subsequence to be pushed into the max heap
        """
        pass

    @abstractmethod
    def incrementHits(self, subsequence: Subsequence):
        """
        Increments the hits of the given subsequence in the max heap and update the heap accordingly to ensure the heap property is maintained.
        @param subsequence: Subsequence whose hits are to be incremented.
        """
        pass

    @abstractmethod
    def remove(self, subsequence: Subsequence):
        """
        Remove the given subsequence from the max heap.
        @param subsequence: Subsequence to be removed from the max heap.
        """
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[Subsequence]:
        """
        Returns an iterator for the max heap.
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """
        Returns the number of elements in the max heap.
        """
        pass
