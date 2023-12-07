# 2023-2024-Information_Retrieval_Project

A repo for the group project for the course Information Retrieval (Master Computer Science 2001WETINR) at the University of Antwerp in the academic year of 2023-2024. The team consists of Zlatko Ristic (s0191855), Bas Tobback (s0194105) and Thomas Gueutal (s0195095).

## Requirements

Note that the **disk space requirements** of this project are currently in the order of **Gigabytes**.

- Python 3.8
- pip
- pip install -r requirements.txt

## Setup

This section details the steps to set up before running.

You may want to set up a virtual environment to contain the project's dependencies and requirements. For this, make sure `python3.8` and the related `python3.8-venv` are installed.

```sh
# Create virtual env
python3.8 -m venv venv

# Activate the venv
# Windows
venv/Scripts/activate
# Ubuntu
source venv/bin/activate

# Install requirements
python3.8 -m pip install -r requirements.txt
```

## Datasets

This section describes which datasets have been used for developing this project. We also note which ones are provided within this repository, and where they are located.

DATASET | USED? | PROVIDED?
-|-|-
FEVER | yes | [train.jsonl](/train.jsonl)