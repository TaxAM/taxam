import sys
import csv

if len(sys.argv) != 6:
    print("Usage: python main.py <taxonomy_level> <reads_taxonomy_file.tax> <ref_taxonomy_file.tax> <mapping_file_reads_to_ref.mma> <output_file_name.csv>")
    print()
    print("Taxonomy levels: 0-Kingdom, 1-Phylum, 2-Class, 3-Order, 4-Family, 5-Genus, 6-Species")
    print()
    print("Example: python main.py 5 reads.tax cds.tax mapping.mma output.csv")
    sys.exit("System aborted")


titles = ('tax_level', 'reads_taxon_path', 'ref_taxon_path', 'mapping_reads_ref_path', 'output_path')

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
with open(args['reads_taxon_path']) as csvfile:
    reader = csv.reader(csvfile, delimiter = '\t')
    for line in reader:
        # print(line)
        taxonomies = line[:3]

        if len(line) > 3:
            taxonomies += [line[3].replace(';','').split()]
        else:
            continue

        taxon_pos = args['tax_level']
        # print(taxonomies[3])
        taxon = taxonomies[3][taxon_pos]
        print(taxon)
