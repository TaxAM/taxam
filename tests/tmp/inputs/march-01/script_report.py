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
parse.add_argument(
                    '-fn', 
                    '--file_name', 
                    help = 'Name of the file.', 
                    type = str, 
                    action = 'store', 
                    default = 'without_name')

args = parse.parse_args()
args = args.__dict__.copy()
executions = ''
try:
    with open(args['file_scripts'], 'r') as file:
        executions = file.readlines()
except FileNotFoundError:
    sys.exit('File not found.')

list_of_times = []
out_start = time.time()
for execution in executions:
    # Float value of time in seconds
    start = time.time()
    os.system(execution)
    end = time.time()
    list_of_times.append(end - start)
out_end = time.time()
print('The time of the execution was: ' + str(out_end - out_start))

list_of_times.sort()

if not os.path.isdir('./TIMMING/'):
    os.mkdir('./TIMMING/')

with open('./TIMMING/' + 'TIMMING_' + args['file_name'] + '.txt', 'w') as txt_file:
    txt_file.write(
        ','.join(
            [str(list_of_times[0]),
            str(sum(list_of_times)/len(list_of_times)),
            str(list_of_times[-1])]
        )
    )