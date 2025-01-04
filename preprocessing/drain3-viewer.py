from os.path import dirname

from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
from drain3.file_persistence import FilePersistence

persistence = FilePersistence(
    f"{dirname(__file__)}/drain3_state.bin")

config = TemplateMinerConfig()
config.load(f"{dirname(__file__)}/drain3.ini")
config.profiling_enabled = False
template_miner = TemplateMiner(persistence, config)

print("Cluster count: ", template_miner.drain.clusters_counter)

for cluster in template_miner.drain.clusters:
    print(cluster)

# sorted_clusters = sorted(template_miner.drain.clusters,
#                          key=lambda it: it.size, reverse=True)
# for cluster in sorted_clusters:
#     print(cluster)
