from os.path import dirname
import pandas as pd
from vmft_lad.ILogInferenceProvider import ILogInferenceProvider


class FastCyrax7BFewShotLogInference(ILogInferenceProvider):
    """
    Fast log inference provider for Cyrax7B few-shot using pre-computed output for all the logs.
    """

    def __init__(self):
        self.result_df = pd.read_csv(
            f"{dirname(__file__)}/Cyrax_7B_out.csv", index_col="log_template"
        )

    def initialise(self):
        return

    def infer(self, log: str) -> bool:
        return self.result_df.loc[log]["label"]