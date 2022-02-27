import argparse
import os
import sys
import time

parse = argparse.ArgumentParser(description='File to get scripts.', usage='python ./script_report.py -fs "./testset1a_mateus.sh"')

parse.add_argument(
                    '-fs', 
                    '--file_scripts', 
                    help = 'File with all the scripts to run.', 
                    type = str, 
                    action = 'store', 
                    default = '')

args: parse = parse.parse_args()
args: dict = args.__dict__.copy()
executions: str = ''
try:
    with open(args['file_scripts'], 'r') as file:
        executions = file.readlines()
except FileNotFoundError:
    sys.exit('File not found.')

list_of_times: list = []
for execution in executions:
    # Float value of time in seconds
    start = time.perf_counter()
    os.system(execution)
    end = time.perf_counter()
    list_of_times.append(end - start)

list_of_times.sort()

if not os.path.isdir('./TIMMING/'):
    os.mkdir('./TIMMING/')

with open('./TIMMING/' + 'TIMMING_' + args['file_scripts'].split('.')[-2] + '.txt', 'w') as txt_file:
    txt_file.write(','.join([str(list_of_times[0]),
                            str(sum(list_of_times)/len(list_of_times)),
                            str(list_of_times[-1])]))