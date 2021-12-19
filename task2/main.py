#   ATTENTION use CTRL + C for stopped program
# --master_dir [-md] catalog source data
# --slave_dir [-sd] catalog-mirror master
# --log [-l] path to log file - default script's directory
# --interval [-t] time interval between snapshots in seconds - default 3600

import os
import sys
import time
import logging
import argparse
from dirsync import sync


def create_parser():
    dir_path_self = os.path.dirname(os.path.realpath(__file__))
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument('-md', '--master_dir')
    parser_arg.add_argument('-sd', '--slave_dir')
    parser_arg.add_argument('-l', '--log', default=dir_path_self)
    parser_arg.add_argument('-t', '--interval', nargs='?', default='3600')

    return parser_arg


def sync_files(logger):

    print('log file: ' + namespace.log)
    print('next synchronization after ' + namespace.interval + 's')
    sync(namespace.master_dir, namespace.slave_dir, 'sync', logger=logger, verbose=True, purge=True)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger


def get_file_handler():
    _log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"
    file_handler = logging.FileHandler(namespace.log + '\\sync.log', 'a', 'utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    _log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.master_dir and namespace.slave_dir:
        if os.path.isdir(namespace.master_dir) and os.path.isdir(namespace.slave_dir):

            logger_sync = get_logger(__name__)
            try:
                print("Press CTRL + C to stop synchronization")
                while True:
                    sync_files(logger_sync)
                    time.sleep(int(namespace.interval))
            except KeyboardInterrupt:
                print("synchronization stopped")
            pass

        else:
            print('Error directories not founded')
    else:
        print("Please input necessary params --master_dir and --slave_dir")
