import os
import time
from os.path import dirname
from threading import Thread
import pandas as pd
from inputimeout import inputimeout, TimeoutOccurred

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.file_persistence import FilePersistence

from Falcon7BFewShotLogInference import Falcon7BFewShotLogInference
from SubsequenceMaxHeap import SubsequenceMaxHeap
from OnlineDetector import OnlineDetector
from Subsequence import Subsequence


drain_config_base_path = f"{dirname(__file__)}/drain-config"
persistence = FilePersistence(f"{drain_config_base_path}/drain3_state.bin")
config = TemplateMinerConfig()
config.load(f"{drain_config_base_path}/drain3.ini")
template_miner = TemplateMiner(persistence, config)


inference_provider = Falcon7BFewShotLogInference()
max_heap_provider = SubsequenceMaxHeap()
window_size = 4
similarity_threshold = 0.05
anomaly_threshold = 0.2

detector = OnlineDetector(
    template_miner,
    inference_provider,
    max_heap_provider,
    window_size,
    similarity_threshold,
    anomaly_threshold,
)


def follow(name):
    current = open(name, "r")
    curino = os.fstat(current.fileno()).st_ino
    while True:
        while True:
            line = current.readline()
            if not line:
                break
            yield line

        try:
            if os.stat(name).st_ino != curino:
                new = open(name, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                continue
        except IOError:
            print("ERROR: IOError")
        time.sleep(1)


print("Start listening to logs...")

log_queue = []


def listen_log_file(log_queue):
    log_file = "/var/log/messages"
    for line in follow(log_file):
        line = line.rstrip()
        line = line.partition(": ")
        log_line = line[2].rstrip()
        if len(log_line) == 0:
            continue
        log_metadata_split = line[0].strip().split(" ")
        timestamp = pd.to_datetime(log_metadata_split[0])

        cluster = template_miner.match(log_line)
        cluster_id = -1
        if cluster is None:
            result = template_miner.add_log_message(log_line)
            cluster_id = result["cluster_id"]
        else:
            cluster_id = cluster.cluster_id

        log_queue.append({"timestamp": timestamp, "log_key": cluster_id})


listen_log_thread = Thread(target=listen_log_file, args=(log_queue,))
listen_log_thread.start()

INFERENCE_MODE = False

while True:
    os.system("clear")
    if len(log_queue) < window_size:
        print(f"Logs: {log_queue}")
        print(f"Waiting for {window_size - len(log_queue)} more logs...")
        time.sleep(1)
        continue

    logs = log_queue[:window_size]
    del log_queue[:window_size]
    print(f"Log keys: {logs}")

    subsequence_data = []
    for log in logs:
        timestamp = log["timestamp"]
        log_key = log["log_key"]
        subsequence_data.append(log_key)

    subsequence = Subsequence(subsequence_data)

    if not INFERENCE_MODE:
        detector.learnRecord(subsequence)
        print(f"Added subsequence: {subsequence}")
        try:
            inputimeout(prompt="Press any key to enter inference mode: ", timeout=0.2)
            INFERENCE_MODE = True
        except TimeoutOccurred:
            continue
    else:
        anomaly_score = detector.detectAnomaly(subsequence)
        print(f"Anomaly score: {anomaly_score}")
        time.sleep(0.1)
