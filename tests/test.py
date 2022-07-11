from os import system

FOLDER_SAMPLES = r'C:\Users\Mateus\Documents\PAINTER\#02_TaxAM\#01_REPS\taxamTestGenerator\samples'
TAXAM_PATH = '../taxam'
TIES = {
    1: 'reads',
    2: 'contigs',
    3: 'discard'
}

for taxon_level in range(1, 8):
    for tie in range(1, 4):
        tie_name = TIES[tie]
        command = f'python "{TAXAM_PATH}" -fp "{FOLDER_SAMPLES}" -tl {taxon_level} -fu {tie} -op "output_level{taxon_level - 1}_tie-{tie_name}" > "output_level{taxon_level - 1}_tie-{tie_name}.txt"'

        try:
            # print(command)
            # print('-'*80)
            # print()
            system(command)
        except Exception as excpection:
            print(excpection)

# python "../taxam" -fp "../../taxamTestGenerator/samples" -tl 7 -fu 3 -op "output_level7_tie-tie"

# python "C:/Users/Mateus/Documents/PAINTER/#02_TaxAM/#01_REPS/taxam/taxam" -fp "2M samples/pool_esc_a/espec_folder" -tl 1 -fu 1 -op "a_output_level0_tie-reads"