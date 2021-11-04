import sys
import os

my_path = sys.argv[1]
arr = os.listdir(my_path)
side_01 = my_path + '\\' + arr[0]
side_02 = my_path + '\\' + arr[1]
# print(os.listdir(side_01))
side_01_list = os.listdir(side_01)
side_02_list = os.listdir(side_02)
main_file = ''
if len(side_01_list) == len(side_02_list):
    for key, value in enumerate(side_01_list):

        file_01 = my_path + '\\' + arr[0] + '\\' + value
        file_02 = my_path + '\\' + arr[1] + '\\' + side_02_list[key]
        out_file_name = 'test' + str(key)
        # file_01 = sys.argv[1]
        # file_02 = sys.argv[2]
        # out_file_name = sys.argv[3]
        equal = True
        file_line = 'File 1: ' + file_01 + '\nFile 2: ' + file_02 + '\n\n'
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
            header = '[Identical files!]\n'
        else:
            header = '[Non-identical files!]\n'

        main_file += str(key) + header

        if(not os.path.isdir(my_path + '/z__equals_test/')):
            os.mkdir(my_path + '/z__equals_test/')

        with open(my_path + '/z__equals_test/' + out_file_name + '.txt', 'w') as file:
            file.write(header)
            file.write(file_line)
            
    with open(my_path + '/z__equals_test/#00_main_file.txt', 'w') as file:
            file.write(main_file)
else:
    print('Amount of files in each side is different!')
