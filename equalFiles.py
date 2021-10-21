import sys
import os

file_01 = sys.argv[1]
file_02 = sys.argv[2]
out_file_name = sys.argv[3]
equal = True
file_line = 'Aquivo 1: ' + file_01 + '\nArquivo 2: ' + file_02 + '\n\n'
with open(file_01, 'r') as f1:
    with open(file_02, 'r') as f2:
        # print(f1.readlines(), f2.readlines())
        txt1, txt2 = f1.readlines(), f2.readlines()

        if len(txt1) > len(txt2):
            txt1, txt2 = txt2, txt1
        
        # [+] equals, [-] differents, [*] doubled
        for pointer, line in enumerate(txt1):
            file_line += '[' + line.replace('\n', '') + '] - [+]\n' if line == txt2[pointer] else '[' + line.replace('\n', '') + ']['+ txt2[pointer].replace('\n', '') + '] - [-]\n'
            if line != txt2[pointer]:
                equal = False
            # print(pointer, line == txt2[pointer])
        
        for i in range(pointer + 1, len(txt2)):
            file_line += '[][' + txt2[i].replace('\n', '') + '] - [*]\n'
            equal = False

if equal:
    header = '[FILES ARE EQUALS!]\n'
else:
    header = '[FILES ARE NOT EQUALS!]\n'

if(not os.path.isdir('equals_test/')):
    os.mkdir('equals_test/')

with open('equals_test/' + out_file_name + '.txt', 'w') as file:
    file.write(header)
    file.write(file_line)
