tx_level_names = ['reads', 'contig', 'discard']
tx_level_roof = 7
a_tie_roof = 3
for pool in ['d']:
    row = ''
    for tx_level in range(tx_level_roof):
        for a_tie in range(a_tie_roof):
            row += f'python "C:/Users/Mateus/Documents/PAINTER/#02_TaxAM/#01_REPS/first_model/taxam/execTaxam.py" -fp "5M samples/pool_esc_{pool}/espec_folder" -tl {tx_level + 1} -fu {a_tie + 1} -op "{pool}_output_level{tx_level}_tie-{tx_level_names[a_tie]}" -th 2'
            row += '\n' if tx_level * a_tie != (tx_level_roof - 1) * (a_tie_roof - 1) else ''

    with open(f'windows_testset1{pool}_mateus_th_2.sh', 'w') as f:
        f.write(row)