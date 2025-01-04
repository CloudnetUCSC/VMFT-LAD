from transformers import pipeline
from vmft_lad.ILogInferenceProvider import ILogInferenceProvider


class BartLargeZeroShotLogInference(ILogInferenceProvider):
    """
    Log inference provider using BART-Large model with zero-shot classification.
    """

    def __init__(self, bart_cache=None):
        """
        @param bart_cache: Cache to store the results of BART-Large model for logs. This is used to avoid redundant calls to the model.
        """
        self.bart_cache = {} if bart_cache == None else bart_cache
        self.candidate_labels = ["fault", "unsure", "normal"]
        self.bart = pipeline(model="facebook/bart-large-mnli")

    def initialise(self):
        # Initializing bart
        self.bart("Test", self.candidate_labels)

    def infer(self, log: str) -> bool:
        if not log in self.bart_cache:
            self.bart_cache[log] = self.bart(log, self.candidate_labels)["labels"][0]

        return self.bart_cache[log] == "fault"
