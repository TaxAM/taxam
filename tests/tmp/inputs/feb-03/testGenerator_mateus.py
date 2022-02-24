tx_level_names = ['contig', 'reads', 'discard']
row = ''
tx_level_floor = 7
a_tie_floor = 3
for sample in ['a', 'b', 'c', 'd', 'e']:
    for tx_level in range(tx_level_floor):
        for a_tie in range(a_tie_floor):
            row += f'python "C:/Users/Mateus/Documents/PAINTER/#02_TaxAM/#01_REPS/first_model/taxam/execTaxam.py" -fp "C:/Users/Mateus/Documents/PAINTER/#02_TaxAM/#01_REPS/first_model/tests/tmp/inputs/feb-03/pool_{sample}/espec_folder" -tl {tx_level + 1} -fu {a_tie + 1} -op "output_level{tx_level}_tie-{tx_level_names[a_tie]}"'
            row += '\n' if tx_level * a_tie != (tx_level_floor - 1) * (a_tie_floor - 1) else ''

    with open(f'testset1{sample}_mateus.sh', 'w') as f:
        f.write(row)