tx_level_names = ['reads', 'contig', 'discard']
tx_level_roof = 7
a_tie_roof = 3
for pool in ['a', 'b', 'c', 'd', 'e']:
    row = ''
    for tx_level in range(tx_level_roof):
        for a_tie in range(a_tie_roof):
            row += f'python "C:/Users/Mateus/Documents/PAINTER/#02_TaxAM/#01_REPS/first_model/taxam/execTaxam.py" -fp "C:/Users/Mateus/Documents/PAINTER/#02_TaxAM/#01_REPS/first_model/tests/tmp/inputs/feb-03/pool_{pool}/espec_folder" -tl {tx_level + 1} -fu {a_tie + 1} -op "{pool}_output_level{tx_level}_tie-{tx_level_names[a_tie]}"'
            row += '\n' if tx_level * a_tie != (tx_level_roof - 1) * (a_tie_roof - 1) else ''

    with open(f'testset1{pool}_mateus.sh', 'w') as f:
        f.write(row)