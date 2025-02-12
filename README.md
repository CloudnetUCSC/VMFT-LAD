﻿## VMFT-LAD: Virtual Machine Proactive Fault Tolerance using Log-based Anomaly Detection

This repository contains the Python implementation of VMFT-LAD, a semi-supervised machine learning model designed to avert Virtual Machine failures in the Cloud utilizing the host and the Virtual Machine Manager log data.

VMFT-LAD is a semi-supervised, real-time log anomaly detection model capable of detecting failures ahead of time to provide effective VM fault tolerance via Live Migration.

VMFT-LAD's core anomaly detection module is powered by a modified Matrix Profile and it leverages a Large Language Model for log inference, effectively minimizing false positives.

### Architecture of VMFT-LAD

![vmft-lad-architecture](https://github.com/user-attachments/assets/51818fd5-a120-4227-9dce-98959e0a6d5a)

Please refer the [paper](https://ieeexplore.ieee.org/document/10767421) for more details on algorithms.

```bib
@ARTICLE {
  pratheeks2024vmft-lad,
  author={Senevirathne, Pratheek and Cooray, Samindu and Dinal Herath, Jerome and Fernando, Dinuni},
  journal={IEEE Access},
  title={Virtual Machine Proactive Fault Tolerance Using Log-Based Anomaly Detection},
  year={2024},
  volume={12},
  number={},
  pages={178951-178970},
  doi={10.1109/ACCESS.2024.3506833}
}
```

### Prerequisites

- Python 3.8
- Python Poetry package manager ([install poetry](https://python-poetry.org/docs/#installation))

### Get started

To get started, simply clone this repo,

```bash
git clone https://github.com/CloudnetUCSC/VMFT-LAD.git
```

and install the dependencies using Poetry,

```bash
cd VMFT-LAD/VMFT_LAD
poetry install
```

This will create a new python virtual environment and install all required dependencies.
This virtual environment can be used to run all the python scripts and jupyter notebooks in this project.

To do a test run using a sample dataset, go to `VMFT_LAD/tests` directory and run `hdd-test` or `benign-test` jupyter notebooks.

### Datasets

Click [here](https://mega.nz/folder/jAYlRKDZ#27eFsbSqFuE_VwKiMvP1BA) to download all raw and pre-processed log datasets

### License

This project is licensed under a [Creative Commons License](https://creativecommons.org/licenses/by/4.0/).

<hr>

With ❤️ Cloudnet Research Group, University of Colombo School of Computing.
