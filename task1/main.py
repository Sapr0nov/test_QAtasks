# task1 start program and get information about it
import os
import csv
import time
import psutil
import subprocess
import configparser
from pathlib import Path
from datetime import datetime


def get_and_check(check=1, default_value='', ask='Enter some Number',
                  hint='The value must be positive Number e.g. [10]'):
    """
    :param default_value: value used if pressed [Enter] with empty string
    :param check: Number of revise option: 1 checked Integer > 0; 2 checked file exist; 4 checked smt more
    :param ask: String with asked text
    :param hint: String with hint if parameter was entering incorrect
    """

    result: str = ''
    data_correct: bool = False

    while not data_correct:
        data_correct = True
        result = input(ask + ' default = [' + default_value + '] ' + ':')
        if result == "":
            result = default_value

        if check == 1:
            if (not result.isdigit()) or (int(result) < 0):
                data_correct = False
                print(hint)
        if check == 2:
            if not os.path.isfile(result):
                data_correct = False
                print(hint)

    return result


dir_path_self = os.path.dirname(os.path.realpath(__file__))
Path(dir_path_self + "\\log").mkdir(parents=True, exist_ok=True)

config = configparser.ConfigParser()
dir_ini_file = dir_path_self + '\\settings.ini'

if not os.path.isfile(dir_ini_file):
    print('create settings file')
    ini_file = open(dir_ini_file, "w")  # create if no ini file
    ini_file.close()
else:

    config.read(dir_ini_file)

if not config.has_option(None,'interval'):
    print('loading default settings')
    config['DEFAULT']['interval'] = "1"
    config['DEFAULT']['path'] = ""



interval_get_stat = int(get_and_check(1, config['DEFAULT']['interval'], 'Enter a Interval in seconds',
                                      'The interval must be a positive Number'))
path_file_process = get_and_check(2, config['DEFAULT']['path'], 'Enter a path to file',
                                  'The path must be a full path for a file')

config['DEFAULT']['interval'] = str(interval_get_stat)
config['DEFAULT']['path'] = path_file_process
ini_file = open(dir_ini_file, "w")
config.write(ini_file)
ini_file.close()

# log file format YYMMDD-nameApp.csv
name_log_file = datetime.now().strftime('%y%m%d') + '_' + os.path.basename(path_file_process)
output_file = open(dir_path_self + '/log/' + name_log_file + '.csv', 'w', encoding='UTF8')
writer = csv.writer(output_file, dialect='unix')

testing_app = subprocess.Popen(path_file_process)
p = psutil.Process(testing_app.pid)

while psutil.pid_exists(testing_app.pid):

    mem = p.memory_info()
    try:
        files = p.num_fds()
    except AttributeError:  # windows system
        files = p.num_handles()

    row = [p.cpu_percent(), mem.rss, mem.vms, files]
    print(row)
    writer.writerow(row)
    time.sleep(interval_get_stat)

output_file.close()
print("finish")
