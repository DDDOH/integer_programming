#!/bin/bash
# Job name:
#SBATCH --job-name=test
#
# Account:
#SBATCH --account=zyzheng
#
# Partition:
#SBATCH --partition=savio2
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
python python_script.py 15 100 25 25 > output K_15_M_100_n_anchor_25_n_sensor_25.txt
python python_script.py 5 100 25 25 > output K_5_M_100_n_anchor_25_n_sensor_25.txt
python python_script.py 10 100 25 25 > output K_10_M_100_n_anchor_25_n_sensor_25.txt
python python_script.py 20 100 25 25 > output K_20_M_100_n_anchor_25_n_sensor_25.txt
python python_script.py 23 100 25 25 > output K_23_M_100_n_anchor_25_n_sensor_25.txt