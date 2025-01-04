from typing import Tuple
from drain3 import TemplateMiner

from Subsequence import Subsequence


class OnlineDetector:
    """
    Online detector class implementing core detection algorithm that run in an online manner
    Need to inject the template miner, inference provider, and max heap provider dependencies
    """

    def __init__(
        self,
        template_miner: TemplateMiner,
        inferenceProvider,
        maxHeapProvider,
        windowSize: int,
        similarityThreshold: float,
        anomalyThreshold: float,
    ):
        self.template_miner = template_miner
        self.inferenceProvider = inferenceProvider
        self.windowSize = windowSize
        self.similarityThreshold = similarityThreshold
        self.anomalyThreshold = anomalyThreshold

        # Max heap to store unique benign subsequences
        self.comparisonMaxHeap = maxHeapProvider

        self.inferenceProvider.initialise()
        self.comparisonMaxHeap.initialise()

    def relativeDistance(self, a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
        abs_distance = sum(abs(a[i] - b[i]) for i in range(len(a)))
        cmp = sum(abs(b[i]) for i in range(len(b)))
        if cmp == 0:
            return 1  # Infinite distance if cmp is 0
        rd = abs_distance / cmp
        if rd > 1:  # Relative distance may be greater than 1
            return 1
        return rd

    def learnRecord(self, subsequence: Subsequence):
        # Learn only dissimilar subsequences
        for comparison_subsequence in self.comparisonMaxHeap:
            cur_dist = self.relativeDistance(
                subsequence.data, comparison_subsequence.data
            )
            if cur_dist <= self.similarityThreshold:
                return

        self.comparisonMaxHeap.push(subsequence)

    def handleRecord(self, subsequence: Subsequence) -> float:
        matched_subsequence = None
        anomaly_score = 1
        for comparison_subsequence in self.comparisonMaxHeap:
            cur_dist = self.relativeDistance(
                subsequence.data, comparison_subsequence.data
            )
            if cur_dist < anomaly_score:
                anomaly_score = cur_dist
            if cur_dist <= self.similarityThreshold:
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
        for log_key in subsequence.data:
            log_template = self.template_miner.drain.id_to_cluster[
                log_key
            ].get_template()
            log_template = (
                log_template.replace("<:*:>", "")
                .replace("<:ID:>", "")
                .replace("<:IP:>", "")
                .replace("<:SEQ:>", "")
                .replace("<:CMD:>", "")
                .replace("<:NUM:>", "")
                .replace("<:HEX:>", "")
            )

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
