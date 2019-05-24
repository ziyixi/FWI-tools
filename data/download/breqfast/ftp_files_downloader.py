from ftplib import FTP
import sh
import click
from os.path import join, isfile, isdir
import numpy as np
from logbook import Logger, FileHandler
import multiprocessing


def get_ftp_file_list(username):
    ftp = FTP("ftp.iris.washington.edu")
    ftp.login()
    ftp.cwd(join("pub", "userdata", username))
    return ftp.nlst()


def get_download_urls(filelist):
    urls = []
    baseurl = "ftp://ftp.iris.washington.edu/pub/userdata/"
    for thefile in filelist:
        urls.append(baseurl + thefile)
    return urls


def get_files_to_download(main_directory, filelist_ftp):
    sh.mkdir("-p", main_directory)
    sh.mkdir("-p", join(main_directory, "data"))

    # ftp.filelist
    np.savetxt(join(main_directory, "ftp.filelist"), np.array(filelist_ftp))

    # local.filelist
    if isfile(join(main_directory, "local.filelist")):
        filelist_local = np.loadtxt(
            join(main_directory, "local.filelist"), dtype=np.str
        )
    else:
        filelist_local = np.array([], dtype=np.str)

    filelist_ftp = set(filelist_ftp)
    filelist_local = set(filelist_local)

    filelist_todownload = filelist_ftp - filelist_local

    return filelist_todownload


@click.command()
@click.option(
    "--thread_number",
    required=True,
    help="the thread number to download the data",
    type=str,
)
@click.option(
    "--username", required=True, help="the directory owner's name in ftp", type=str
)
@click.option(
    "--main_directory", required=True, help="the main downloading directory", type=str
)
def main(thread_number, username, main_directory):
    # set up logging
    log_handler = FileHandler(join(main_directory, "log"))
    log_handler.push_application()
    log = Logger("fdsn_log")

    def download_kernel(download_url):
        log_message = f"[thread: {multiprocessing.current_process()}] start to download {download_url} "
        log.info(log_message)
        sh.wget("-c", download_url)
        log_message = f"[thread: {multiprocessing.current_process()}] finish downloading {download_url} "
        log.info(log_message)

    filelist_ftp = get_ftp_file_list(username)
    files_to_download = get_files_to_download(main_directory, filelist_ftp)
    downloading_urls = get_download_urls(files_to_download)

    with multiprocessing.Pool(thread_number) as pool:
        pool.starmap(download_kernel, downloading_urls)

    log.info("success")
