import argparse
import os
import sys

def getPrefix(file, sep):
    return file.split('.')[0].split(sep)[-2]

def getSuffix(file, sep):
    return file.split('.')[0].split(sep)[-1]

parse = argparse.ArgumentParser(description='Creates files to do a manual tracking.', usage='python ./manualTest_generator.py -sf "./pool_a/espec_folder" -of "./manual_test_poo_a" -pn "Pool A"')

parse.add_argument(
                    '-sf', 
                    '--start_folder', 
                    help = 'Folder where are contigs, mappings and/or reads.', 
                    type = str, 
                    action = 'store', 
                    default = None)

parse.add_argument(
                    '-of', 
                    '--out_folder', 
                    help = 'Folder to store files to manual tracking.', 
                    type = str, 
                    action = 'store', 
                    default = None)

parse.add_argument(
                    '-pn', 
                    '--pool_name', 
                    help = 'Name of the pool.', 
                    type = str, 
                    action = 'store', 
                    default = 'pool')

args: parse = parse.parse_args()
args: dict = args.__dict__.copy()

can_continue: bool = True
if args['start_folder'] == None:
    print('You should informe "start folder".')
    can_continue = False
if args['out_folder'] == None:
    print('You should informe "out folder".')
    can_continue = False

if not can_continue:
    sys.exit()

if not os.path.isdir(args['start_folder']):
    sys.exit('This directory doesnt exists.')
else:
    list_files: list = os.listdir(args['start_folder'])

files: dict = {}
suffix: str = ''
wrong_files: str = ''
type_files: list = ['contigs', 'mapping',  'reads']
for file in list_files:
    if len(file.split('_')) == 2:    
        type = getPrefix(file, '_')
        key = getSuffix(file, '_')
        if type in type_files:
            try:
                files[key][type] =  file
            except:
                files[key] = {type: file}
        else:
            wrong_files += file + '\n'
    else:
        wrong_files += file + '\n'
    type, key = 'None', 'None'

if wrong_files != '':
    sys.exit('You cannot continue. Bad files:\n' + wrong_files)
keys: list = list(files.keys())
if os.path.isdir(args['out_folder']):
    sys.exit(args['out_folder'] + ' already exists.')
else:
    os.mkdir(args['out_folder'])

for key in keys:
    row: str = ''
    with open(args['start_folder'] + '/' + files[key]['reads'], 'r') as f_reads:
        with open(args['start_folder'] + '/' + files[key]['contigs'], 'r') as f_contigs:
            with open(args['start_folder'] + '/' + files[key]['mapping'], 'r') as f_mapping:
                with open(args['out_folder'] + '/manual_test_' + args['pool_name'] + '_sample_' + key + '.txt', 'w') as f_pool:
                    row +=   f'{args["pool_name"]}\nReads\n{f_reads.read()}\n\nContigs\n{f_contigs.read()}\n\nMapping\n{f_mapping.read()}\n\n'
                    f_pool.write(row)