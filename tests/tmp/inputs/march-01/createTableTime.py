import os

path = r'C:\Users\Mateus\Documents\PAINTER\#02_TaxAM\#01_REPS\first_model\tests\tmp\inputs\march-01\TIMMING'


files = os.listdir(path)

md = '|File name|Min time (s)|Mean time (s)|Max time (s)|\n'
md += '|' + '---|' * 4
for file in files:
    with open(path + '/' + file, 'r') as f:
        md += '\n|' + file + '|' + f.readline().replace(',', '|')

with open(path + '/' + 'table.md', 'w') as tableMd:
    tableMd.write(md)