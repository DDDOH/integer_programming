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
python python_script.py 15 100 25 25