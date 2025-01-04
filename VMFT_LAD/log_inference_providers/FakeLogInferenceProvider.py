from vmft_lad.ILogInferenceProvider import ILogInferenceProvider


class FakeLogInferenceProvider(ILogInferenceProvider):
    """
    Always returns true.
    For every log, this provider will return true (true positive).
    """

    def __init__(self):
        super().__init__()

    def initialise(self):
        return

    def infer(self, log: str) -> bool:
        return True
