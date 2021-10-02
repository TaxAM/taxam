import sys
import csv

if len(sys.argv) != 7:
    print("Usage: python main.py <taxonomy_level> <reads_taxonomy_file.tax> <ref_taxonomy_file.tax> <mapping_file_reads_to_ref.mma> <output_file_name.csv> <file_to_use>\n")
    print("Taxonomy levels: 0-Kingdom, 1-Phylum, 2-Class, 3-Order, 4-Family, 5-Genus, 6-Species\n")
    print("File to use: 0-Reads, 1-Contigs, 2-No one\n")
    print("Example: python main.py 5 reads.tax cds.tax mapping.mma output.csv\n")
    sys.exit("System aborted")


titles = ('tax_level', 'reads_taxon_path', 'ref_taxon_path', 'mapping_reads_ref_path', 'output_path', 'file_to_use')

args = {}
for key, arg in enumerate(sys.argv[1:]):
    try:
        arg = int(arg)
    except:
        pass
    args[titles[key]] = arg

debug = True
debug_counter = 0
print("Loading taxonomy of reads...")

counter = {}
taxon_ref = {}

files_path_ref = {'reads_taxon_path': counter, 'ref_taxon_path': taxon_ref}

for file_path_ref, t_file in files_path_ref.items():
    with open(args[file_path_ref]) as csvfile:
        reader = csv.reader(csvfile, delimiter = '\t')
        for taxonomies in reader:
            
            if taxonomies[0] != 'C':
                continue

            id_line = taxonomies[1]
            taxon_pos = args['tax_level'] - 1
            taxon = taxonomies[3].split()[taxon_pos].replace(';','')
            if taxon == 'NA':
                continue
            else:
                if file_path_ref == 'reads_taxon_path':
                    t_file[id_line] = {taxon : 1}
                elif file_path_ref == 'ref_taxon_path':
                    t_file[id_line] = taxon
                    
print(files_path_ref)

# with open(args['reads_taxon_path']) as csvfile:
#     reader = csv.reader(csvfile, delimiter = '\t')
#     for taxonomies in reader:
        
#         if taxonomies[0] != 'C':
#             continue

#         id_read = taxonomies[1]
#         taxon_pos = args['tax_level'] - 1
#         taxon = taxonomies[3].split()[taxon_pos].replace(';','')
#         if taxon == 'NA':
#             continue
#         else:
#             counter[id_read] = {taxon : 1}

# for a, b in counter.items():
#     print(a, b)

# print("Loading taxonomy of reference sequences...")

# with open(args['ref_taxon_path']) as csvfile:
#     reader = csv.reader(csvfile, delimiter = '\t')
#     for taxonomies in reader:
        
#         if taxonomies[0] != 'C':
#             continue

#         id_read = taxonomies[1]
#         taxon_pos = args['tax_level'] - 1
#         taxon = taxonomies[3].split()[taxon_pos].replace(';','')
#         if taxon == 'NA':
#             continue
#         else:
#             taxon_ref[id_read] = taxon

# for a, b in taxon_ref.items():
#     print(a, b)

print("Mapping reads on references...")
dic_map = {}
with open(args['mapping_reads_ref_path']) as csvfile:
    reader = csv.reader(csvfile, delimiter = '\t')
    for map_line in reader:

        id_read = map_line[0]
        id_contig = map_line[1]
        dic_map[id_read] = id_contig

# for a, b in dic_map.items():
#     print(a, b)