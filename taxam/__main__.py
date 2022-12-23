# PYTHON IMPORTS
import decimal
import shutil
import os
import sys
from threading import Thread

# LOCAL IMPORTS
from execTaxam import execTaxam
from utils import getPrefix, getSuffix, returnIntegerList, ROOT_PATH, validDelimiter
from utils.local_parses import local_parses

# Local parsers
args = local_parses()

type_files = ['contigs', 'mapping',  'reads']
terminal = args.__dict__.copy()
# IT STORES A LIST WITH A QUANTITY OF READS FOR EACH SAMPLE
if terminal['reads_quantity'] != None:
    terminal['reads_quantity'] = returnIntegerList(terminal['reads_quantity'])

# SEEING IF THIS DIRECTORY EXISTS
if(os.path.isdir(terminal["folder_path"] + '/')) and terminal['folder_path'] != None:
    files = sorted(os.listdir(terminal['folder_path']))
else:
    sys.exit(terminal["folder_path"] + ' does not exists')

# CHECKING IF ALL SEPARATORS ARE VALID
terminal['contigs_sep'] = validDelimiter(terminal['contigs_sep'])        
terminal['mapping_sep'] = validDelimiter(terminal['mapping_sep'])        
terminal['reads_sep'] = validDelimiter(terminal['reads_sep'])        
terminal['output_sep'] = validDelimiter(terminal['output_sep'])

file_names = {}
type, key = 'None', 'None'
wrong_files = ''

print('Checking if all files are valid.')
# CHECKING IF ALL FILES ARE VALID AND STORING THEM IN A DICTIONARY
# SORTED IN ALPHABETICAL ORDER
for file in files:
    if len(file.split('_')) == 2:    
        type = getPrefix(file, '_')
        key = getSuffix(file, '_')
        if type in type_files:
            try:
                file_names[key][type] = terminal['folder_path'] + '/' + file
            except:
                file_names[key] = {type : terminal['folder_path'] + '/' + file}
        else:
            wrong_files += file + '\n'
    else:
        wrong_files += file + '\n'
    type, key = 'None', 'None'

# SEEING IF EACH FILE IS WRITTEN IN OUR PROTOCOL
if wrong_files != '':
    print('\nBad files:\n' + wrong_files)
    sys.exit('''
    You used bad files. Your files should be:

    reads_<read_id>.txt
    contigs_<contigs_id>.txt
    mapping_<mapping_id>.txt
    ''')

# SEEING IF NUMBER OF FILES IS CORRECT FOR EACH GROUP
wrong_files = ''
for name, file in file_names.items():
    if sorted(list(file.keys())) != ['contigs', 'mapping'] and sorted(list(file.keys())) != ['contigs', 'mapping', 'reads']:
        wrong_files += name + ' has [' + ', '.join(list(sorted(file.keys()))) + ']. It should have [contigs, mapping] or [contigs, mapping, reads]\n'
# IF wrong_files IS NOT EMPTY THAT MEANS THERE ARE ANY BAD FILE
if wrong_files != '':
    sys.exit('\nBad material:\n' + wrong_files)
print('[Finished!]')


# GETTING NUMBER OF READS FOR EACH SAMPLE IF WE'RE USING RELATIVE MODE IN THE TABLE
if terminal['matrix_mode'] == 2 and terminal['reads_quantity'] != None:
    print('Counting reads informed to relative mode.')
    wrong_keys = []
    if len(file_names) == len(terminal['reads_quantity']):
        for key in terminal['reads_quantity'].keys():
            if key not in file_names:
                wrong_keys.append(key)
        if len(wrong_keys) > 0:
            sys.exit('You informed some wrong keys: ' + ','.join(wrong_keys))

    else:
        sys.exit('You informed more or less number of reads for each sample.')
    print('[Finished!]')

print('Creating Threads.')
# CREATING PARAMETERS TO PASS FOR THREADS FOR execTaxam FUNCTION
box = []
my_args = []

# STORING ARGUMENTS LIST IN A BIGGEST LIST
i = 0
for key, value in file_names.items():
    box.append(terminal['tax_level'])
    for type in type_files:
        if type in value.keys():
            box.append(value[type])
        else:
            box.append(None)
    box.append(terminal['reads_sep'])
    box.append(terminal['contigs_sep'])
    box.append(terminal['mapping_sep'])
    box.append(terminal['output_sep'])
    box.append(terminal['output_name'])
    box.append(terminal['file_to_use'])
    box.append(terminal['matrix_mode'])
    if terminal['reads_quantity'] != None:
        # IF USER DIDN'T INFORME READS QUANTITY, THERE IS NO READ FILE AND IT WANTS TO DO RELATIVE CALCULATE, THAN
        # box[3] IS READS PATH
        if box[3] == None and terminal['matrix_mode'] == 2 and terminal['reads_quantity'][key] == 0:
            sys.exit('Expected reads quantity.')
        box.append(terminal['reads_quantity'][key])
        i += 1
    else:
        if box[3] == None and terminal['matrix_mode'] == 2 and terminal['reads_quantity'] == None:
            sys.exit('Expected reads quantity.')
        box.append(terminal['reads_quantity'])

    my_args.append(box[:])
    box = []
tmp_folder = ROOT_PATH + r'/tmp/'
if(not os.path.isdir(tmp_folder)):
        os.mkdir(tmp_folder)

threads = []
# Number of samples
samples_number = len(file_names)
# Number of threads
threads_number = terminal['thread_number']
if threads_number > samples_number:
    sys.exit('There are more threads than samples.')
elif threads_number < 1:
    sys.exit('Informe a number of threads valid.')

qtt_min = int(samples_number / threads_number)
rest = samples_number % threads_number
# BEGGINING OF CUT IN THE LIST
beginning = 0
for i in range(threads_number):
    # CURRENT QUANTITY PER LINE
    current_qtt = qtt_min + (1 if rest > 0 else 0)
    rest -= 1
    # END OF CUT IN THE LIST
    end = beginning + current_qtt
    # CREATING THREAS LIST FOR EACH THREAD
    threads.append(Thread(target=execTaxam, args=[my_args[beginning : end], i+1]))
    beginning = end
print('[Finished!]')

print('Starting threads.')
# IT STARTS THREADS
for thread in threads:
    thread.start()

# IT WAITS FOR THREADS TO FINISH
for thread in threads:
    thread.join()
print('[Finished!]')

print('Getting data out of threads.')
# SEEING IF THIS DIRECTORY EXISTS
if (os.path.isdir(tmp_folder)):
    files = sorted(os.listdir(tmp_folder))
else:
    sys.exit(tmp_folder + ' directory doesnt exist.')

# GETTING AND STORING DICTIONARY FROM TXT FILES
data = {}
terminal['reads_quantity'] = {}
for file in files:
    with open(tmp_folder + file, 'r') as f:
        line, terminal['reads_quantity'][getSuffix(file,'_')] = f.readline().split(';;')
        data[getSuffix(file,'_')] = eval(line.strip())

# DELETE FOLDER
shutil.rmtree(tmp_folder)
print('[Finished!]')

print('Sorting final matrix.')
# SORTING SAMPLE KEYS IN ASCENDING ORDER
samples = sorted(list(data.keys()), key=lambda x: x.lower())
wights = []
# STORING WIGHT KEYS
for sample in samples:
    for key in data[sample].keys():
        if key not in wights:
            wights.append(key)

# SORTING WIGHT KEYS IN ASCENDING ORDER
wights = sorted(wights, key=lambda x: x.lower())
header = 'TaxAM' + terminal['output_sep'] + terminal['output_sep'].join(samples) + '\n'
tmp_list = []
rows = ''
for j in range(len(wights)):
    tmp_list.append(wights[j])
    for i in range(len(samples)):
        try:
            # IF WE'RE USING ABSOLUTE MODE
            if terminal['matrix_mode'] == 1:
                # Getting each absolute value of each animal from each sample
                tmp_list.append(str(data[samples[i]][wights[j]]))
            # IF WE'RE USING RELATIVE MODE
            else:
                tmp_list.append(
                        f"{decimal.Decimal(data[samples[i]][wights[j]] / int(terminal['reads_quantity'][samples[i]])):.20f}"
                )
        except:
            tmp_list.append('0')
    rows += terminal['output_sep'].join(tmp_list) + '\n'
    tmp_list = []
print('[Finished!]')

# CHECKING IF OUTPUT FILE EXISTS
OUT_PUT_FOLDER = ROOT_PATH + r'/output_taxam/'
if(not os.path.isdir(OUT_PUT_FOLDER)):
        os.mkdir(OUT_PUT_FOLDER)

# WRITTING OUTPUT
print('Writing final matrix.')
with open(OUT_PUT_FOLDER + terminal['output_name'] + '.taxam', 'w') as f:
    f.write(header)
    f.write(rows)
print('[Finished!]')