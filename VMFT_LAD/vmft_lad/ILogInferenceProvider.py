from abc import ABC, abstractmethod


class ILogInferenceProvider(ABC):
    """
    Interface for log inference provider.
    The log inference provider is responsible for inferring whether the given log is anomalous or not.
    """

    @abstractmethod
    def initialise(self):
        """
        Code to initialise the inference provider.
        This is invoked once before the detection process starts.
        """
        pass

    @abstractmethod
    def infer(self, log: str) -> bool:
        """
        Infers whether the given log is anomalous or not.
        @param log: The log line to infer.
        @return: True if the log is anomalous, False otherwise.
        """
        pass
