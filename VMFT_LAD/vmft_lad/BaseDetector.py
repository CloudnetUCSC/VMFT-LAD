from typing import List, Tuple
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.file_persistence import FilePersistence
from os.path import dirname

from .ILogInferenceProvider import ILogInferenceProvider
from .IMaxHeapProvider import IMaxHeapProvider
from .Subsequence import Subsequence

drain_config_base_path = f"{dirname(__file__)}/../../preprocessing"
persistence = FilePersistence(f"{drain_config_base_path}/drain3_state.bin")
config = TemplateMinerConfig()
config.load(f"{drain_config_base_path}/drain3.ini")
config.profiling_enabled = False
template_miner = TemplateMiner(persistence, config)


class BaseDetector:
    """
    Base detector class implementing core detection algorithm
    Need to inject the inference provider and max heap provider dependencies
    """

    def __init__(
        self,
        inferenceProvider: ILogInferenceProvider,
        maxHeapProvider: IMaxHeapProvider,
        data: List[int],
        windowSize: int,
        probationaryPeriod: int,
        subsequenceMatchThreshold: float,
        anomalyThreshold: float,
    ):
        self.inferenceProvider = inferenceProvider
        self.data = data
        self.windowSize = windowSize
        self.probationaryPeriod = probationaryPeriod
        self.subsequenceMatchThreshold = subsequenceMatchThreshold
        self.anomalyThreshold = anomalyThreshold

        # Max heap to store unique benign subsequences
        self.comparisonMaxHeap = maxHeapProvider

        self.inferenceProvider.initialise()
        self.comparisonMaxHeap.initialise()

        # Adding all the probationary (benign) windows to the max heap
        for i in range(self.probationaryPeriod - self.windowSize + 1):
            self.comparisonMaxHeap.push(
                Subsequence(tuple(self.data[i : i + self.windowSize]))
            )

    def relativeDistance(self, a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
        abs_distance = sum(abs(a[i] - b[i]) for i in range(len(a)))
        cmp = sum(abs(b[i]) for i in range(len(b)))
        if cmp == 0:
            return 1  # Infinite distance if cmp is 0
        rd = abs_distance / cmp
        if rd > 1:  # Relative distance may be greater than 1
            return 1
        return rd

    def handleRecord(self, current_time_step: int) -> float:
        if current_time_step < self.probationaryPeriod:
            return 0

        current_subsequence = tuple(
            self.data[current_time_step - self.windowSize + 1 : current_time_step + 1]
        )

        matched_subsequence = None
        anomaly_score = 1
        for comparison_subsequence in self.comparisonMaxHeap:
            cur_dist = self.relativeDistance(
                current_subsequence, comparison_subsequence.data
            )
            if cur_dist < anomaly_score:
                anomaly_score = cur_dist
            if cur_dist <= self.subsequenceMatchThreshold:
                matched_subsequence = comparison_subsequence
                break

        if matched_subsequence:
            # If a matched subsequence is found, increment its hits
            self.comparisonMaxHeap.incrementHits(matched_subsequence)
            return anomaly_score

        if anomaly_score <= self.anomalyThreshold:
            return anomaly_score

        # Anomaly detected, check the log templates to see if it is  TP or FP
        tp = False
        # print(
        #     "Anomaly detected at window ",
        #     current_time_step,
        #     " with score ",
        #     anomaly_score,
        # )
        # print("Log templates: ")
        for log_key in current_subsequence:
            log_template = template_miner.drain.id_to_cluster[log_key].get_template()
            if self.inferenceProvider.infer(log_template):
                tp = True
                # print("TP_FOUND: ", end=" ")
            # print(log_template)

        if tp:
            # print("**** TP *****")
            return 1
        else:
            # print("**** FP *****")
            # print("Updating the comparison heap...")
            # self.comparisonMaxHeap.push(Subsequence(current_subsequence))
            return 0
