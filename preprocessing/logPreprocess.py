# Preprocess the logs by sorting the logs and converting them to log key and time representation

import os
from os.path import dirname
import pandas as pd
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.file_persistence import FilePersistence
from utils import *
from env import LOG_DIRECTORY


persistence = FilePersistence(f"{dirname(__file__)}/drain3_state.bin")
config = TemplateMinerConfig()
config.load(f"{dirname(__file__)}/drain3.ini")
config.profiling_enabled = False
template_miner = TemplateMiner(persistence, config)

log_directory = LOG_DIRECTORY

###
# Joining log files, Converting to log keys, and sorting the log lines according to timestamp
###

# For each log directory (there is a directory with collected log files for each day)
for day_log_directory in os.scandir(log_directory):
    if not day_log_directory.is_dir():
        continue

    directoryName = day_log_directory.name.split("_")
    if len(directoryName[1]) == 1:
        directoryName[1] = "0" + directoryName[1]

    directoryName = "_".join(directoryName)

    print(f"\nScanning log directory: {day_log_directory.name}")
    raw_out_file = (
        f"{dirname(__file__)}/raw-preprocessed/{day_log_directory.name}_unlabelled.csv"
    )

    final_out_file = f"{dirname(__file__)}/final-output/buffer-io/{directoryName}.csv"

    if os.path.isfile(raw_out_file) and os.path.isfile(final_out_file):
        print("   Preprocessing done for log dir. Output files exists.")
        continue

    day_log_df = pd.DataFrame(columns=["timestamp", "value"])

    # For each application log file in log directory.
    # Get the log line -> separate timestamp and log line -> get log key id using drain3
    # -> save the timestamp and log key in out csv
    for log_file in os.scandir(day_log_directory):
        if not log_file.is_file() or log_file.name.rsplit(".")[-1] != "log":
            continue

        print(f"Scanning log file: {log_file.name}")
        log_file_descriptor = open(log_file.path, "r")
        for line in log_file_descriptor:
            line = line.rstrip()
            line = line.partition(": ")
            log_line = line[2].rstrip()
            if log_line.__len__() == 0:
                continue
            log_metadata_split = line[0].strip().split(" ")
            timestamp = (
                logTimestampToDateTime(
                    log_metadata_split[0], log_metadata_split[1], log_metadata_split[2]
                )
                if log_metadata_split[1] != ""
                else logTimestampToDateTime(
                    log_metadata_split[0], log_metadata_split[2], log_metadata_split[3]
                )
            )

            cluster = template_miner.match(log_line)
            cluster_id = -1
            if cluster is None:
                result = template_miner.add_log_message(log_line)
                cluster_id = result["cluster_id"]
            else:
                cluster_id = cluster.cluster_id

            day_log_df.loc[len(day_log_df)] = [timestamp, cluster_id]

        log_file_descriptor.close()

    # Sorting and saving file
    day_log_df.set_index("timestamp", inplace=True, append=False, drop=True)
    day_log_df.sort_values("timestamp", axis=0, inplace=True)
    day_log_df.to_csv(raw_out_file, index=True)

    ##
    # Removing unnecessary logs
    ##

    unwanted_log_keys = [128, 129, 130, 305, 306, 307]  # CRON-related logs
    day_log_df = day_log_df[~day_log_df["value"].isin(unwanted_log_keys)]
    day_log_df.to_csv(final_out_file, index=True)
