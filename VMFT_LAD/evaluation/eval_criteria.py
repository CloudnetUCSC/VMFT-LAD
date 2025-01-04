from typing import Literal

Region = Literal["BENIGN", "ANOMALOUS", "FAILURE"]
EvalResult1 = Literal["TP", "TN", "FP", "FN"]
EvalResult2 = Literal["TP", "TN", "FP", "FN", "TP_LATE"]


def get_criteria1(
    region: Region, threshold: float, anomaly_score: float
) -> EvalResult1:
    """
    Criteria 1
    TP: Model identified an anomaly in the anomalous region (pre-failure) or the failure region of the dataset
    TN: Model did not identify an anomaly in the benign region of the dataset
    FP: Model identified an anomaly in the benign region of the dataset
    FN: Model did not identify an anomaly in the anomalous region or the failure region of the dataset
    """
    positivePrediction = anomaly_score >= threshold
    if region == "BENIGN":
        if positivePrediction:
            return "FP"
        else:
            return "TN"
    else:  # region is ANOMALOUS or FAILURE
        if positivePrediction:
            return "TP"
        else:
            return "FN"


def get_criteria2(
    region: Region, threshold: float, anomaly_score: float
) -> EvalResult2:
    """
    Criteria 2
    TP: Model identified an anomaly only in the anomalous region (pre-failure) of the dataset
    TN: Model did not identify an anomaly in the benign region of the dataset
    FP: Model identified an anomaly in the benign region of the dataset
    FN: Model did not identify an anomaly in the anomalous region or the failure region of the dataset
    TP_LATE: Model identified an anomaly in the failure region of the dataset
    """
    positivePrediction = anomaly_score >= threshold
    if region == "BENIGN":
        if positivePrediction:
            return "FP"
        else:
            return "TN"
    elif region == "ANOMALOUS":
        if positivePrediction:
            return "TP"
        else:
            return "FN"
    else:  # region is FAILURE
        if positivePrediction:
            return "TP_LATE"
        else:
            return "FN"
