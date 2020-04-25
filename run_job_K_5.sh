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
#SBATCH --time=72:00:00

#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=yufeng_zheng@berkeley.edu
#
## Command(s) to run:
# echo "hello world"
# conda init bash
# conda activate py3
python -u python_script.py 5 100 25 25 > K_5_M_100_n_anchor_25_n_sensor_25_2nd_try.txt