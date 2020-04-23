#!/bin/bash
# Job name:
#SBATCH --job-name=test
#
# Account:
#SBATCH --account=account_name
#
# Partition:
#SBATCH --partition=partition_name
#
# Quality of Service:
#SBATCH --qos=qos_name
#
# Wall clock limit:
#SBATCH --time=50:00:30
#
## Command(s) to run:
# echo "hello world"
conda activate py3
python python_script.py 5 100 25 25
python python_script.py 10 100 25 25
python python_script.py 15 100 25 25
python python_script.py 20 100 25 25
python python_script.py 23 100 25 25