"""Package to store functions to take care about the taxam matrix process"""
import csv
import os
from utils import addInMatrix, getSuffix

def cleaningProcess(counter, matrix, ctrl):
    """Check for each Read Id if there is more than one animal, if so, it
    checks if they are different animals, if so, it uses the ctrl variable
    to resolve the conflict, and then, adds it to the matrix, or not add, if
    the users have set ctrl variable as 3, to discart this Read Id. If there
    is just one animal, so it just adds to the matrix. 


    Parameters
    ----------
    counter : dict
        Each key is a Read Id, and its value is a list with one or two
        animals. Like:
        {'READ11': ['RE2', 'RE1'], 'READ8': ['RE4']}
    matrix : dict
        Each key is an Animal Name, and its value is a int representing how
        many times this animal appears. Like:
        {'RE2': 16, 'RE1': 1}
    ctrl : int
        Used to resolve conflicts if for a Read Id there are two different
        animals. 1-Animal from reads, 2-Animal from contigs, 3-No one animal.
    """
    for read, taxons in counter.items():
        # Conflict situation
        # Does something if contig and read pointed to different bichos
        if len(taxons) == 2 and taxons[0] != taxons[1]:
            # If use reads
            if ctrl == 1:
                addInMatrix(matrix, taxons, 0)
            # If use contigs
            elif ctrl == 2:
                addInMatrix(matrix, taxons, 1)
        else:
            addInMatrix(matrix, taxons, 0)

def readReads(args):
    counter = {}
    with open(args['reads_taxon_path']) as tax_file:
        print('Reading read file...')
        reader = csv.reader(tax_file, delimiter = args['reads_sep'])
        print('Read stored')
        qtt_read_lines_counter = 0
        print('Reading lines')
        for line in reader:
            # if user wants that the program counts reads number for this sample
            if args['matrix_mode'] == 2:
                if line[0] in ['C', 'U']:
                    if args['reads_quantity'] in [0, None]:
                        qtt_read_lines_counter += 1
                    else:
                        qtt_read_lines_counter = args['reads_quantity']
            # if this read is classified
            if line[0] == 'C':
                read_id = line[1]
                taxon_pos = args['tax_level'] - 1
                try:
                    if line[3].split(';')[taxon_pos].replace(' ','') != '':
                        taxon = line[3].split(';')[taxon_pos].strip()
                    else:
                        taxon = 'NA'
                except:
                    taxon = 'NA'
                if taxon == 'NA':
                    continue
                # EX {'READA': ['R2']}
                if read_id in counter.keys():
                    counter[read_id].append(taxon)
                else:
                    counter[read_id] = [taxon]

    return counter, qtt_read_lines_counter

def readContigs(args):
    contig_tax = {}
    with open(args['ref_taxon_path']) as tax_file:
        reader = csv.reader(tax_file, delimiter = args['contigs_sep'])
        for line in reader:
            # if this read is classified
            if line[0] == 'C':
                contig_id = line[1]
                taxon_pos = args['tax_level'] - 1
                try:
                    if line[3].split(';')[taxon_pos].replace(' ','') != '':
                        taxon = line[3].split(';')[taxon_pos].strip()
                    else:
                        taxon = 'NA'
                except:
                    taxon = 'NA'

                if taxon == 'NA':
                    continue

                # EX {'READA': {'R2': 1}}
                contig_tax[contig_id] = taxon

    return contig_tax

def readMapping(args, counter, contig_tax):
    with open(args['mapping_reads_ref_path']) as tax_file:
        reader = csv.reader(tax_file, delimiter = args['mpp_sep'])
        for line in reader:
            try:
                taxon = contig_tax[line[1]]
                read_id = line[0]

                if taxon == 'NA':
                        continue

                if read_id in counter.keys():
                    counter[read_id].append(taxon)
                else:
                    counter[read_id] = [taxon]
                    
            except Exception as e:
                pass

def storeMatrix(args, matrix):
    if(not os.path.isdir('out_files/')):
        os.mkdir('out_files/')
    print('Sorting animals.')
    sorted_keys = sorted(matrix)
    print('[Finished]')
    line = ''
    tmp_folder = './tmp/'
    for key in sorted_keys:
        line += str(key) + args['output_sep'] + str(matrix[key]) + '\n'
    print('Writing data out of thread.')
    with open(tmp_folder + 'tx_' + getSuffix(args['ref_taxon_path'], '_') + '.txt', 'w') as file:
        file.write(str(matrix) + ';' + str(args['reads_quantity']))
    print('[Finished]')