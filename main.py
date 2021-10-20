import os
import sys
import csv
from typing import Counter

def verifyParamters(pmtsList):
    if len(sys.argv[1:]) == 6:
        extensions = ['tax', 'tax', 'txt']
        # print(pmtsList[1:4])
        for k, v in enumerate(pmtsList[1:4]):
            # print(v)
            v = v.replace('.\\', '')
            # Find where the extension starts
            index = v.index('.')
            # print(v[index + 1:], k)
            # Verify if this file is with the right extension
            if extensions[k] != v[index + 1 :]:
                return False

    elif len(sys.argv[1:]) == 4:
        extensions = ['tax', 'txt']
        # print(pmtsList[1:3])
        for k, v in enumerate(pmtsList[1:3]):
            # print(v)
            v = v.replace('.\\', '')
            # Find where the extension starts
            index = v.index('.')
            # print(v[index + 1:], k)
            # Verify if this file is with the right extension
            if extensions[k] != v[index + 1 :]:
                return False

    return True

def printDict(dict):
    for k, v in dict.items():
        print(k, v)

# if len(sys.argv) != 7:
#     print("Usage: python main.py <taxonomy_level> <reads_taxonomy_file.tax> <ref_taxonomy_file.tax> <mapping_file_reads_to_ref.mma> <output_file_name.csv> <file_to_use>\n")
#     print("Taxonomy levels: 0-Kingdom, 1-Phylum, 2-Class, 3-Order, 4-Family, 5-Genus, 6-Species\n")
#     print("File to use: 0-Reads, 1-Contigs, 2-No one\n")
#     print("Example: python main.py 5 reads.tax cds.tax mapping.mma output.csv\n")
#     sys.exit("System aborted")


# titles = ('tax_level', 'reads_taxon_path', 'ref_taxon_path', 'mapping_reads_ref_path', 'output_path', 'file_to_use')

# JUST TEST
# print(len(sys.argv[1:]))
# print(sys.argv[1:])
# print(verifyParamters(sys.argv[1:]))

# Verifying if there are just necessary items in the terminal
if not(verifyParamters(sys.argv[1:])):
    sys.exit("Wrong paramters")
else:
    if len(sys.argv[1:]) == 6:
        with_reads = True
        titles = ('tax_level', 'reads_taxon_path', 'ref_taxon_path', 'mapping_reads_ref_path', 'output_path', 'file_to_use')

    elif len(sys.argv[1:]) == 5:
        with_reads = False
        titles = ('tax_level','ref_taxon_path', 'mapping_reads_ref_path', 'output_path', 'file_to_use')

    elif len(sys.argv[1:]) == 4:
        with_reads = False
        titles = ('tax_level','ref_taxon_path', 'mapping_reads_ref_path', 'output_path')
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
# print(args['tax_level'])
if args['tax_level'] not in [int(i) for i in range(1, 8)]:
    sys.exit("tax_level informed is wrong!")
if with_reads:
    if args['file_to_use'] not in [int(i) for i in range(1, 4)]:
        sys.exit("file_to_use informed is wrong!")

debug = True
debug_counter = 0
# print("Loading taxonomy of reads...")

counter = {}
taxon_ref = {}

# Seeing if it using reads
if with_reads:
    files_path_ref = {'reads_taxon_path': counter, 'ref_taxon_path': taxon_ref}
else:
    files_path_ref = {'ref_taxon_path': taxon_ref}

# Couting taxon for each read
with open(args['reads_taxon_path']) as tax_file:
    reader = csv.reader(tax_file, delimiter = '\t')
    for line in reader:
        # print(line)
        # if this read is classified
        if line[0] == 'C':
            read_id = line[1]
            taxon_pos = args['tax_level'] - 1
            taxon = line[3].split()[taxon_pos].replace(';','')
            # EX {'READA': {'R2': 1}}
            counter[read_id] = [taxon]

# printDict(counter)

# Stores which taxon is each contig
contig_tax = {}
with open(args['ref_taxon_path']) as tax_file:
    reader = csv.reader(tax_file, delimiter = '\t')
    for line in reader:
        # print(line)
        # if this read is classified
        if line[0] == 'C':
            contig_id = line[1]
            taxon_pos = args['tax_level'] - 1
            taxon = line[3].split()[taxon_pos].replace(';','')
            # EX {'READA': {'R2': 1}}
            contig_tax[contig_id] = taxon

# printDict(contig_tax)
# print(contig_tax)
# Adds contigs from the mapping to counting
with open(args['mapping_reads_ref_path']) as tax_file:
    reader = csv.reader(tax_file, delimiter = '\t')
    for line in reader:
        # print(line)
        try:
            taxon = contig_tax[line[1]]
            read = line[0]

            if read in counter.keys():
                counter[read].append(taxon)
            else:
                counter[read] = [taxon]
                
        except Exception as e:
            # print(f'-> {e} <-')
            pass
# print()
# printDict(counter)
matrix = {}
ctrl = args['file_to_use'] # 1, 2 or 3
# Cleaning process
for read, taxons in counter.items():
    # Conflit situation
    # Does something if contig and read pointed to different bichos
    if len(taxons) == 2 and taxons[0] != taxons[1]:
        # If use reads
        if ctrl == 1:
            try:
                matrix[taxons[0]] += 1
            except:
                matrix[taxons[0]] = 1

        elif ctrl == 2:
            # print('o/')
            try:
                matrix[taxons[1]] += 1
            except:
                matrix[taxons[1]] = 1
        
        # If use contigs

        # If dicarting
    else:
        try:
            matrix[taxons[0]] += 1
        except:
            matrix[taxons[0]] = 1

printDict(matrix)


