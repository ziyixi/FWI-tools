#==================
# This script is not in parallel, should modify to a slurm script
#==================

# activate conda env
. activate seismology

# set directories' paths
sacpz="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED.garbage/sacpz"
seed="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED.garbage/seed"
data="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED.structed"
rawdata="/mnt/research/seismolab2/japan_slab/data/upload_temp_ziyi/20190325.SEED"

# python post_structure.py
python ../../data/process/handle_cea_directory_structure/post_structure.py --old_path $rawdata --new_path $data

# python process_seed.py
python ../../data/process/process_seed.py --main_path $data

# python after_structure.py
python ../../data/process/handle_cea_directory_structure/after_structure.py --processedurl $data --seedurl $seed --sacpzurl $sacpz