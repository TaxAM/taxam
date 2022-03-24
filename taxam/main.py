import csv
import os
from util import *

def execTaxam(my_args_lists, number_of_thread = 0):
    import time
    for my_args_list in my_args_lists:
        tmp_list = my_args_list
        # Verifying if there are just necessary items in the terminal
        if not(verifyExtension(tmp_list[1:4], 'txt')):
            print('Wrong parameters')
            sys.exit()
        else:
            if tmp_list[3] != None:
                with_reads = True
            else:
                with_reads = False
            titles = ('tax_level', 'ref_taxon_path', 'mapping_reads_ref_path', 'reads_taxon_path', 'reads_sep', 'contigs_sep', 'mpp_sep', 'output_sep', 'output_path', 'file_to_use', 'matrix_mode', 'reads_quantity')

        args = {}
        # ASSOCIATING THE VALUES TO THE KEYS
        for key, arg in enumerate(tmp_list):
            try:
                arg = int(arg)
            except:
                pass
            args[titles[key]] = arg
            
        # Verify if tax_level and file_to_use are correct
        if args['tax_level'] not in [int(i) for i in range(1, 8)]:
            print('<tax_leve> information is wrong')
            sys.exit()
        if with_reads:
            if args['file_to_use'] not in [int(i) for i in range(1, 4)]:
                print("<file_to_use> informed is wrong!")
                sys.exit()

        debug = True
        debug_counter = 0

        # Counter of reads and contigs by taxon
        counter = {}
        taxon_ref = {}

        # Seeing if it using reads
        if with_reads:
            files_path_ref = {'reads_taxon_path': counter, 'ref_taxon_path': taxon_ref}
        else:
            files_path_ref = {'ref_taxon_path': taxon_ref}

        # Seeing if this delimiter is valid
        args['contigs_sep'] = validDelimiter(args['contigs_sep'])        
        args['mpp_sep'] = validDelimiter(args['mpp_sep'])        
        args['output_sep'] = validDelimiter(args['output_sep'])
        #STATUS
        print('th: ' + str(number_of_thread) +  ' -> All fields as valid ' + args['mapping_reads_ref_path'])

        # COUNTING TIME OF READING READS
        min_time = 5
        av_time = []
        max_time = 0

        # Couting taxon for each read
        if with_reads:
            print('th: ' + str(number_of_thread) +  ' -> Reads: ' + args['reads_taxon_path'])
            ctrl = args['file_to_use'] # 1, 2 or 3
            args['reads_sep'] = validDelimiter(args['reads_sep'])
            print('Opening read file...')        
            with open(args['reads_taxon_path']) as tax_file:
                print('Reading read file...')
                reader = csv.reader(tax_file, delimiter = args['reads_sep'])
                print('Read stored')
                qtt_read_lines_counter = 0
                print('Reading lines')
                lines_counter = 0
                for line in reader:
                    # start = time.clock()
                    # print(line)
                    # if user wants that the program counts reads number for this sample
                    if args['matrix_mode'] == 2:
                        print('Matrix mode 2')
                        if line[0] in ['C', 'U']:
                            if args['reads_quantity'] in [0, None]:
                                qtt_read_lines_counter += 1
                            else:
                                qtt_read_lines_counter = args['reads_quantity']
                    # if this read is classified
                    if line[0] == 'C':
                        read_id = line[1]
                        taxon_pos = args['tax_level'] - 1
                        try:
                            if line[3].split(';')[taxon_pos].replace(' ','') != '':
                                taxon = line[3].split(';')[taxon_pos].strip()
                            else:
                                taxon = 'NA'
                        except:
                            taxon = 'NA'
                        if taxon == 'NA':
                            continue
                        # EX {'READA': ['R2']}
                        if read_id in counter.keys():
                            counter[read_id].append(taxon)
                        else:
                            counter[read_id] = [taxon]
                    # lines_counter += 1
                    # print(lines_counter)
                    # end = time.clock()
                    # VERIFYING TIMES
                    # my_time = end - start
                    # if my_time < min_time:
                    #     min_time = my_time
                    # if my_time > max_time:
                    #     max_time = my_time
                    # av_time.append(my_time)
            args['reads_quantity'] = qtt_read_lines_counter
        print('Reads read!')
        # with open('./reads_counter_time_LINUX.txt', 'w') as file:
        #     file.write('Minimum time: ' + str(min_time) + '\nAverage time: ' + str(sum(av_time)/len(av_time)) + '\nMaximum time: ' + str(max_time) + '\nTotal read: ' + str(len(av_time)))
            # file.write(f'Minimum time: {min_time}\nAverage time: {sum(av_time)/len(av_time)}\nMaximum time: {max_time}\nTotal read: {len(av_time)}')
            


        # Stores which taxon is each contig
        contig_tax = {}
        print('th: ' + str(number_of_thread) +  ' -> Contigs: ' + args['ref_taxon_path'])
        with open(args['ref_taxon_path']) as tax_file:
            reader = csv.reader(tax_file, delimiter = args['contigs_sep'])
            for line in reader:
                # if this read is classified
                if line[0] == 'C':
                    contig_id = line[1]
                    taxon_pos = args['tax_level'] - 1
                    try:
                        if line[3].split(';')[taxon_pos].replace(' ','') != '':
                            taxon = line[3].split(';')[taxon_pos].strip()
                        else:
                            taxon = 'NA'
                    except:
                        taxon = 'NA'

                    if taxon == 'NA':
                        continue

                    # EX {'READA': {'R2': 1}}
                    contig_tax[contig_id] = taxon
        print('Contigs read!')

        print('th: ' + str(number_of_thread) +  ' -> Mapping: ' + args['mapping_reads_ref_path'])
        # Adds contigs from the mapping to counting
        with open(args['mapping_reads_ref_path']) as tax_file:
            reader = csv.reader(tax_file, delimiter = args['mpp_sep'])
            for line in reader:
                try:
                    taxon = contig_tax[line[1]]
                    read_id = line[0]

                    if taxon == 'NA':
                            continue

                    if read_id in counter.keys():
                        counter[read_id].append(taxon)
                    else:
                        counter[read_id] = [taxon]
                        
                except Exception as e:
                    pass
        print('Mapping read!')

        matrix = {}
        print('Cleaning process and final counting process.')
        # Cleaning process and final counting process
        for read, taxons in counter.items():
            # Conflict situation
            # Does something if contig and read pointed to different bichos
            if len(taxons) == 2 and taxons[0] != taxons[1]:
                # If use reads
                if ctrl == 1:
                    addInMatrix(matrix, taxons, 0)
                # If use contigs
                elif ctrl == 2:
                    addInMatrix(matrix, taxons, 1)
            else:
                addInMatrix(matrix, taxons, 0)
        print('[Finished]')

        if(not os.path.isdir('out_files/')):
            os.mkdir('out_files/')
        print('Sorting animals.')
        sorted_keys = sorted(matrix)
        print('[Finished]')
        line = ''
        tmp_folder = './tmp/'
        for key in sorted_keys:
            line += str(key) + args['output_sep'] + str(matrix[key]) + '\n'
        print('Writing data out of thread.')
        with open(tmp_folder + 'tx_' + getSuffix(args['ref_taxon_path'], '_') + '.txt', 'w') as file:
            file.write(str(matrix) + ';' + str(args['reads_quantity']))
        print('[Finished]')