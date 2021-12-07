reads_path = "/users/mateus/downloads/kaiju_dbs/viruses_data_01/final_01/reads/out_viruses_single_names.tax"
contigs_path = "/users/mateus/downloads/kaiju_dbs/viruses_data_01/final_01/contigs/contigs_named.tax"
mapping_path = "/users/mateus/downloads/kaiju_dbs/viruses_data_01/final_01/mapping/final_mapping_01.txt"
out_path = "g2/"
test_name = "test_bash_generator.bat"
sep = '"\\t"'
tx = ['kingdom', 'phylum', 'class', 'order', 'family', 'genre', 'specie']

line = ''
for key, value in enumerate(tx):
    for i in range(1, 7):
        name = '#0' + str(key + 1) + '_' + tx[key] + '_test_mat_' + str(i) + '.taxam'
        if i <= 3:
            line += 'python main.py ' + str(key + 1) + ' "' + reads_path + '" "' + contigs_path + '" "' + mapping_path + '" ' + str((sep + ' ') * 4) + '"' + out_path + name + '" ' + str(i) + '\n'
        else:
            line += 'python main.py ' + str(key + 1) + ' "' + contigs_path + '" "' + mapping_path + '" ' + str((sep + ' ') * 3) + '"' + out_path + name + '" ' + str(i - 3) + '\n'

with open('test_bash_generator.bat', 'w') as f:
    f.write(line)