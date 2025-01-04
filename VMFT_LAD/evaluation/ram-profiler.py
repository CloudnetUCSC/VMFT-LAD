import psutil
import os
from os.path import dirname
import pandas as pd
from pympler import asizeof

from vmft_lad.BaseDetector import BaseDetector
from heap_providers.SubsequenceMaxHeap import SubsequenceMaxHeap
from log_inference_providers.FakeLogInferenceProvider import FakeLogInferenceProvider

window_size = 4
anomaly_threshold = 0.15
subsequence_match_threshold = 0.05
probationary_period = 150

dataset_path = (
    f"{dirname(__file__)}/../../../data/buffer-io/2024-03-03_01_buffer_io.csv"
)
dataset_df = pd.read_csv(dataset_path, header=0)
data = dataset_df["value"].tolist()

# process = psutil.Process(os.getpid())

# start_ram = process.memory_info().rss

inference_provider = FakeLogInferenceProvider()
max_heap_provider = SubsequenceMaxHeap()
model = BaseDetector(
    inferenceProvider=inference_provider,
    maxHeapProvider=max_heap_provider,
    data=data,
    windowSize=window_size,
    probationaryPeriod=probationary_period,
    subsequenceMatchThreshold=subsequence_match_threshold,
    anomalyThreshold=anomaly_threshold,
)
for i in range(len(data)):
    model.handleRecord(i)

# end_ram = process.memory_info().rss
# ram_cost = end_ram - start_ram

print(f"RAM cost: {asizeof.asizeof(model)/1024} Mb")
