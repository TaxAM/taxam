import os
import sys
from utils import validDelimiter, verifyExtension
from utils.matrix_tools import  cleaningProcess, readContigs, readMapping, readReads, storeMatrix

def execTaxam(my_args_lists, number_of_thread = 0):
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

        '''
        //////////////////////////////////
        Couting taxon for each read.
        //////////////////////////////////
        '''
        if with_reads:
            print('th: ' + str(number_of_thread) +  ' -> Reads: ' + args['reads_taxon_path'])
            args['reads_sep'] = validDelimiter(args['reads_sep'])
            
            print('Opening read file...')        
            counter, args['reads_quantity']  = readReads(args)
            print('Reads read!')

        '''
        //////////////////////////////////
        Stores which taxon is each contig.
        //////////////////////////////////
        '''
        print('th: ' + str(number_of_thread) +  ' -> Contigs: ' + args['ref_taxon_path'])
        contig_tax = readContigs(args)
        print('Contigs read!')


        '''
        //////////////////////////////////
        Adds contigs from the mapping to counters.
        //////////////////////////////////
        '''
        print('th: ' + str(number_of_thread) +  ' -> Mapping: ' + args['mapping_reads_ref_path'])
        readMapping(args, counter, contig_tax)
        print('Mapping read!')

        '''
        //////////////////////////////////
        Cleaning process and final counting process.
        //////////////////////////////////
        '''
        matrix = {}
        ctrl = args['file_to_use'] # 1, 2 or 3
        print('Cleaning process and final counting process.')
        cleaningProcess(counter, matrix, ctrl)

        print('[Finished]')

        storeMatrix(args, matrix)