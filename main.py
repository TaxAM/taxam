import os
import csv
# from typing import Counter
from util import *

# if len(sys.argv) != 7:
#     print("Usage: python main.py <taxonomy_level> <reads_taxonomy_file.tax> <ref_taxonomy_file.tax> <mapping_file_reads_to_ref.mma> <output_file_name.csv> <file_to_use>\n")
#     print("Taxonomy levels: 1-Kingdom, 2-Phylum, 3-Class, 4-Order, 5-Family, 6-Genus, 7-Species\n")
#     print("File to use: 1-Reads, 2-Contigs, 3-No one\n")
#     print("Example: python main.py 5 reads.tax cds.tax mapping.mma output.csv\n")
#     sys.exit("System aborted")



# Verifying if there are just necessary items in the terminal
if not(verifyParamters(sys.argv[1:])):
    sys.exit("Wrong paramters")
else:
    if len(sys.argv[1:]) == 10:
        with_reads = True
        titles = ('tax_level', 'reads_taxon_path', 'ref_taxon_path', 'mapping_reads_ref_path', 'reads_sep', 'contigs_sep', 'mpp_sep', 'output_sep', 'output_path', 'file_to_use')
    elif len(sys.argv[1:]) == 8:
        with_reads = False
        titles = ('tax_level','ref_taxon_path', 'mapping_reads_ref_path',  'contigs_sep', 'mpp_sep', 'output_sep', 'output_path', 'file_to_use')
    elif len(sys.argv[1:]) == 7:
        with_reads = False
        titles = ('tax_level','ref_taxon_path', 'mapping_reads_ref_path',  'contigs_sep', 'mpp_sep', 'output_sep', 'output_path')
    else:
        exit('System aborted')


args = {}
# Don't useing the first element cause it's file.py
for key, arg in enumerate(sys.argv[1:]):
    try:
        arg = int(arg)
    except:
        pass
    # print(key, arg)
    args[titles[key]] = arg
    
# Verify if tax_level and file_to_use are correct
if args['tax_level'] not in [int(i) for i in range(1, 8)]:
    sys.exit("tax_level informed is wrong!")
if with_reads:
    if args['file_to_use'] not in [int(i) for i in range(1, 4)]:
        sys.exit("file_to_use informed is wrong!")

debug = True
debug_counter = 0

# Counter of reads and contigs by taxon
counter = {}
taxon_ref = {}

# Seeing if it using reads
if with_reads:
    files_path_ref = {'reads_taxon_path': counter, 'ref_taxon_path': taxon_ref}
else:
    files_path_ref = {'ref_taxon_path': taxon_ref}

# Se if this delimiter is valid
args['contigs_sep'] = validDelimiter(args['contigs_sep'])        
args['mpp_sep'] = validDelimiter(args['mpp_sep'])        
args['output_sep'] = validDelimiter(args['output_sep'])

# Couting taxon for each read
if with_reads:
    ctrl = args['file_to_use'] # 1, 2 or 3
    args['reads_sep'] = validDelimiter(args['reads_sep'])        
    with open(args['reads_taxon_path']) as tax_file:
        reader = csv.reader(tax_file, delimiter = args['reads_sep'])
        for line in reader:
            # if this read is classified
            if line[0] == 'C':
                read_id = line[1]
                taxon_pos = args['tax_level'] - 1
                taxon = line[3].split()[taxon_pos].replace(';','')
                if taxon == 'NA':
                    continue
                # EX {'READA': ['R2']}
                if read_id in counter.keys():
                    counter[read_id].append(taxon)
                else:
                    counter[read_id] = [taxon]


# Stores which taxon is each contig
contig_tax = {}
with open(args['ref_taxon_path']) as tax_file:
    reader = csv.reader(tax_file, delimiter = args['contigs_sep'])
    for line in reader:
        # print(line)
        # if this read is classified
        if line[0] == 'C':
            contig_id = line[1]
            taxon_pos = args['tax_level'] - 1
            taxon = line[3].split(';')[taxon_pos].replace(' ','')

            if taxon == 'NA':
                continue

            # EX {'READA': {'R2': 1}}
            contig_tax[contig_id] = taxon

# Adds contigs from the mapping to counting
with open(args['mapping_reads_ref_path']) as tax_file:
    reader = csv.reader(tax_file, delimiter = args['mpp_sep'])
    for line in reader:
        # print(line)
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

matrix = {}
# Cleaning process and final counting process
for read, taxons in counter.items():
    # Conflit situation
    # Does something if contig and read pointed to different bichos
    if len(taxons) == 2 and taxons[0] != taxons[1]:
        # If use reads
        if ctrl == 1:
            addInMatrix(matrix, taxons, 0)
        # If use contigs
        elif ctrl == 2:
            # print('o/')
            addInMatrix(matrix, taxons, 1)
    else:
        # print('here')
        addInMatrix(matrix, taxons, 0)

if(not os.path.isdir('out_files/')):
    os.mkdir('out_files/')

sorted_keys = sorted(matrix)
# line = 'Bicho\tQuandidade\n'
line = ''
with open('out_files/' + args['output_path'], 'w') as file:
    for key in sorted_keys:
        line += str(key) + args['output_sep'] + str(matrix[key]) + '\n'
    file.write(line)



