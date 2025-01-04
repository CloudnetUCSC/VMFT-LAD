from os.path import dirname
import pandas as pd
from vmft_lad.ILogInferenceProvider import ILogInferenceProvider


class FastBartLargeZeroShotLogInference(ILogInferenceProvider):
    """
    Fast log inference provider for Bart Large zero-shot log classification using pre-computed output for all the logs.
    """

    def __init__(self):
        self.result_df = pd.read_csv(
            f"{dirname(__file__)}/Bart_Large_zero_shot_out.csv",
            index_col="log_template",
        )

    def initialise(self):
        return

    def infer(self, log: str) -> bool:
        return self.result_df.loc[log]["label"]
