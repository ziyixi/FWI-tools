import sh
import click
from slurmpy import Slurm
from mpi4py import MPI
from loguru import logger

# set up MPI and loguru
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
logger.add("fdsn_downloader.log", format="{time} {level} {message}",
           filter="process_seed", level="INFO")


def start_obspyDMT_this_rank
