#!/bin/bash --login
########## SBATCH Lines for Resource Request ##########
 
#SBATCH --time=06:00:00             # limit of wall clock time - how long the job will run (same as -t)
#SBATCH --ntasks=50                  # number of tasks - how many tasks (nodes) that you require (same as -n)
#SBATCH --mem-per-cpu=8G            # memory required per allocated CPU (or core) - amount of memory (in bytes)
#SBATCH --job-name process_seed      # you can give your job a name for easier identification (same as -J)
 
########## Command Lines to Run ##########

# prepare 
conda activate seismology
sacpz="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED.garbage/sacpz"
seed="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED.garbage/seed"
data="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED.structed"
rawdata="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED"
PY="/mnt/home/xiziyi/anaconda3/envs/seismology/bin/python"

# cd
cd /mnt/home/xiziyi/FWI-tools/examples/data                 ### change to the directory where your code is located

# python post_structure.py
# $PY ../../data/process/handle_cea_directory_structure/post_structure.py --old_path $rawdata --new_path $data

# python process_seed.py
srun -n 50 $PY ../../data/process/process_seed.py --main_path $data

# python after_structure.py
$PY ../../data/process/handle_cea_directory_structure/after_structure.py --processedurl $data --seedurl $seed --sacpzurl $sacpz

scontrol show job $SLURM_JOB_ID     ### write job information to output file