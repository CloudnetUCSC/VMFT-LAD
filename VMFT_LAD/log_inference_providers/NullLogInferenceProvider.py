from vmft_lad.ILogInferenceProvider import ILogInferenceProvider


class NullLogInferenceProvider(ILogInferenceProvider):
    """
    Always returns false.
    For every log, this provider will return false (false positive).
    """

    def __init__(self):
        super().__init__()

    def initialise(self):
        return

    def infer(self, log: str) -> bool:
        return False
