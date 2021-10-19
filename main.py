import sys
import csv

def verifyParamters(pmtsList):
    if len(sys.argv[1:]) == 6:
        extensions = ['kaiju', 'kaiju', 'mma']
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
        extensions = ['kaiju', 'mma']
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

    elif len(sys.argv[1:]) == 4:
        with_reads = False
        titles = ('tax_level','ref_taxon_path', 'mapping_reads_ref_path', 'output_path')


args = {}
# Don't useing the first element cause it's file.py
for key, arg in enumerate(sys.argv[1:]):
    try:
        arg = int(arg)
    except:
        pass
    args[titles[key]] = arg
    

# Verify if tax_level and file_to_use are correct
print(args['tax_level'])
if args['tax_level'] not in [int(i) for i in range(1, 8)]:
    sys.exit("tax_level informed is wrong!")
if with_reads:
    if args['file_to_use'] not in [int(i) for i in range(1, 3)]:
        sys.exit("file_to_use informed is wrong!")

debug = True
debug_counter = 0
print("Loading taxonomy of reads...")

counter = {}
taxon_ref = {}

# Seeing if it using reads
if with_reads:
    files_path_ref = {'reads_taxon_path': counter, 'ref_taxon_path': taxon_ref}
else:
    files_path_ref = {'ref_taxon_path': taxon_ref}


for file_path_ref, t_file in files_path_ref.items():
    with open(args[file_path_ref]) as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        for line in reader:
            
            if line[0] != 'C':
                continue

            id_line = line[1]
            taxon_pos = args['tax_level'] - 1
            taxon = line[3].split()[taxon_pos].replace(';','')
            if taxon == 'NA':
                continue
            else:
                if file_path_ref == 'reads_taxon_path':
                    # Setting up files to counter
                    t_file[id_line] = {taxon : 1}
                elif file_path_ref == 'ref_taxon_path':
                    # Setting up files to taxon_ref
                    t_file[id_line] = taxon
                    

# for a, b in counter.items():
#     print(a, b)

# for a, b in taxon_ref.items():
#     print(a, b)
# print(counter)
counter_reads = {}
for read in counter.values():
    for key, value in read.items():
        try:
            counter_reads[key] += 1
        except:
            counter_reads[key] = 1

# We don't need to count contigs
# counter_contigs = {}
# for key, value in taxon_ref.items():
#     try:
#         counter_contigs[value] += 1
#     except:
#         counter_contigs[value] = 1

print("Mapping reads on references...")
dic_map = {}
ctrl = args['file_to_use'] # 1 or 2
print(ctrl)
with open(args['mapping_reads_ref_path']) as csvfile:
    reader = csv.reader(csvfile, delimiter = '\t')
    for map_line in reader:
        id_read = map_line[0]
        id_contig = map_line[1]
        if id_read in counter.keys():
            tx_read = list(counter[id_read])[0]
            # print(tx_contig)
            # print(tx_read, end='')
        else:
            tx_read = -1
            # print(f'{tx_read} ', end='')
        if id_contig in taxon_ref:
            tx_contig = taxon_ref[id_contig]
            # print(tx_contig)
            # print(f' {tx_contig}', end='')
        else:
            tx_contig = -1
            # print(f' {tx_contig}', end='')
        # print(f' - {(tx_read == tx_contig and (tx_read and tx_contig != -1))}')

        # If it is using reads
        if with_reads:
            # -1 indica que aquele read não se relacionou a nenhum taxon
            # Vendo se os taxons são iguais e diferentes de -1
            if tx_read == tx_contig and (tx_read and tx_contig != -1):
                try:
                    dic_map[tx_contig] += 1
                except:
                    dic_map[tx_contig] = 1
            # Se os taxos são diferentes e nenhum é == -1
            elif tx_read != tx_contig and (tx_read != -1 and tx_contig != -1):
                # Se o controle for 1 usa os valor de read
                if ctrl == 1:
                    try:
                        dic_map[tx_read] += 1
                    except:
                        dic_map[tx_read] = 1
                # Se o controle for 1 usa os valor de contig
                elif ctrl == 2:
                    try:
                        dic_map[tx_contig] += 1
                    except:
                        dic_map[tx_contig] = 1
            # Se um dos taxons é igual a -1
            elif tx_read or tx_contig == -1:
                if tx_read != -1 and tx_contig == -1:
                    try:
                        dic_map[tx_read] += 1
                    except:
                        dic_map[tx_read] = 1
                elif tx_read == -1 and tx_contig != -1:
                    try:
                        dic_map[tx_contig] += 1
                    except:
                        dic_map[tx_contig] = 1
        # If it is using just contigs
        else:
            if tx_contig != -1:
                try:
                    dic_map[tx_contig] += 1
                except:
                    dic_map[tx_contig] = 1
            
                    
print(f'Counting reads:      {counter_reads}')
# print(f'Counting contigs:    {counter_contigs}')
print(f'Counting by mapping: {dic_map}')

sorted_keys = sorted(dic_map)

print('\nMatrix de contagem by mapping')
print(f'Bicho\tQuantidade')
for k in sorted_keys:
    print(f'{k}\t{dic_map[k]}')
if with_reads:
    print('+using reads')
print(dic_map)
# print('\nMatrix de contagem by reads')
# print(f'Bicho\tQuantidade')
# for k, v in counter_reads.items():
#     print(f'{k}\t{v}')

# for a, b in dic_map.items():
#     print(a, b)

# Linha teste commit