import sys
from util import *

mapping_path = sys.argv[1]
output_path = sys.argv[2]
mappingSep = sys.argv[3]
outputSep = sys.argv[4]

mappingSep = validDelimiter(mappingSep)
outputSep = validDelimiter(outputSep)


file_line = ''
with open(mapping_path, 'r') as contig_file:
    contig_lines = contig_file.readlines()
    for i in contig_lines:
        line = i.split(mappingSep)
        if line[0][0] != '@':
            file_line += line[0] + outputSep + line[2] + '\n'

with open(output_path, 'w') as output_file:
    output_file.write(file_line)
