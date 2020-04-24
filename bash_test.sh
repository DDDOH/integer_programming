#!/bin/bash
# Job name:
#SBATCH --job-name=test
#
# Account:
#SBATCH --account=fc_nonsta
#
# Partition:
#SBATCH --partition=savio2
#
# Quality of Service:
#SBATCH --qos=savio_normal
#
# Wall clock limit:
#SBATCH --time=50:00:30

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=yufeng_zheng@berkeley.edu
#
## Command(s) to run:
# echo "hello world"
conda init bash
conda activate py3
python -u python_script.py 15 100 25 25 > K_15_M_100_n_anchor_25_n_sensor_25.txt
python -u python_script.py 5 100 25 25 > K_5_M_100_n_anchor_25_n_sensor_25.txt
python -u python_script.py 20 100 25 25 > K_20_M_100_n_anchor_25_n_sensor_25.txt
python -u python_script.py 23 100 25 25 > K_23_M_100_n_anchor_25_n_sensor_25.txt