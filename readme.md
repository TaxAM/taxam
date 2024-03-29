# Taxam

[pt-br](doc/docs/readme-pt_br.md)

Taxam is a platform for aid to areservation and environmental recovery of Amazon areas aubject to mining through microbiological taxonomic analysis.

## Files anatomy
To run the application, you should inform the path to the folder containing the files of each sample. All the files have to be a `txt file` (.txt), and each sample must have, at least, a `Mapping file` and a `Contigs File`, and as optional, a `Reads File`. The files names must follow the pattern `<file_type>_<sample_name>.txt`, using just one `_` (underscore) in the name, for instance `mapping_sample1.txt`.

1. `mapping_<sample_name>.txt`:
```txt
READ143941	CONTIG92596
READ1451406	CONTIG25083
READ459980	CONTIG92303
READ990460	CONTIG87412
READ1725384	CONTIG73062
READ432496	CONTIG76055
READ606934	CONTIG2041
READ1669633	CONTIG36603
READ1904814	CONTIG41944
```
2. `contigs_<sample_name>.txt`:
```txt
C	CONTIG16688	0	RE5; FI4; CL3; OR1; FA8; GE3; ES7
C	CONTIG42069	0	RE6; FI7; CL7; OR5; FA2; GE4; ES6
C	CONTIG80615	0	RE8; FI7; CL8; OR7; FA4; GE1; ES6
C	CONTIG65467	0	RE4; FI8; CL1; OR7; FA2; GE7; ES3
C	CONTIG33318	0	RE3; FI6; CL4; OR4; FA4; GE6; ES8
C	CONTIG22821	0	RE4; FI6; CL6; OR7; FA2; GE9; ES8
C	CONTIG73208	0	RE7; FI5; CL1; OR5; FA4; GE1; ES2
C	CONTIG65070	0	RE9; FI4; CL6; OR8; FA7; GE3; ES6
```

3. `reads_<sample_name>.txt`:
```txt
C	READ464462	0	RE4; FI2; CL6; OR1; FA1; GE8; ES1
C	READ456664	0	RE6; FI9; CL1; OR6; FA2; GE3; ES5
C	READ1690299	0	RE6; FI5; CL6; OR4; FA8; GE1; ES2
C	READ1977403	0	RE6; FI2; CL6; OR2; FA7; GE8; ES7
C	READ157676	0	RE6; FI6; CL7; OR3; FA5; GE6; ES3
C	READ339503	0	RE8; FI2; CL4; OR7; FA5; GE2; ES7
C	READ1274910	0	RE2; FI9; CL1; OR7; FA5; GE6; ES9
C	READ1500832	0	RE3; FI6; CL5; OR2; FA5; GE3; ES1
C	READ71623	0	RE2; FI6; CL6; OR9; FA7; GE1; ES7
```

## Output
The output will be a Matrix with all the samples and the taxonomic information. This file will be saved in a folder called `output_taxam` in the folder `taxam`.
- Absolute Matrix:
```txt
TaxAM	A	B
CL1	204116	233579
CL2	191162	194468
CL3	231485	194407
CL4	222267	227716
CL5	185036	204729
CL6	201188	204705
CL7	188883	207653
CL8	224408	223635
CL9	233962	191896
```
- Relative Matrix:
```txt
TaxAM	A	B
CL1	0.13607733333333333	0.15571933333333332
CL2	0.12744133333333332	0.12964533333333333
CL3	0.15432333333333334	0.12960466666666667
CL4	0.148178	0.15181066666666668
CL5	0.12335733333333333	0.136486
CL6	0.13412533333333335	0.13647
CL7	0.125922	0.13843533333333333
CL8	0.14960533333333334	0.14909
CL9	0.15597466666666668	0.12793066666666666
```


## How to use Taxam
```sh
python taxam <flag_1> <value_1> <flag_2> <value_2> ...
```

### Flags:
- `-tl` or `--tax_level`: Level of taxonomy to use. Taxonomy levels: 1-Kingdom, 2-Phylum, 3-Class, 4-Order, 5-Family, 6-Genus, 7-Species. **[Required | Default: 1]**
- `-fp` or `--folder_path`: Folder where are the file to be used. **[Required]**
- `-rs` or `--reads_sep`: Separator used to part each collumn in read file. **[Optional | Default: "\t"]**
- `-cs` or `--contigs_sep`: Separator used to part each collumn in contigs file. **[Optional | Default: "\t"]**
- `-ms` or `--mapping_sep MAPPING_SEP`: Separator used to part each collumn in mapping file. **[Optional | Default: "\t"]**
- `-os` or `--output_sep`: Separator used to part each collumn in output file generated by TaxAM. **[Optional | Default: "\t"]**
- `-op` or `--output_name`: Name of output file generated by TaxAM. **[Optional | Default: "tx_matrix"]**
- `-fu` or `--file_to_use`: In case of conflict, which file to be used .1-Reads, 2-Contigs, 3-No one. **[Required | Default: 3]**
- `-th` or `--thread_number`: Number of threads to be used. **[Optional | Default: 1]**
- `-mm` or `--matrix_mode`: Mode to create the matrix. 1-Absolute, 2-Relative. **[Optional | Default: 1]**
- `-rq` or `--reads_quantity`: Quantity of reads for each sample. If there are 3 samples: spa,spb, spc, use spa:100,spb:150,spc:275 that is 100 reads for spa, 150 reads for spb, 275 reads for spc. If you want that program calculate automatically for specific sample, informe it as 0, for instance spa:0,spb:125,spc:0 that is 0 reads for spa, 125 reads for spb, 0 reads for spc. **[Required only if matrix mode was 2]**


## Getting Started
### **Generating fake data**
First, you can download the TaxAM module that generate fake taxa data, just [click here](https://github.com/TaxAM/taxamTestGenerator).
After this, let's create some fake data to play a little bit. Run the following commad:
```sh
python taxamTestGenerator -n pool_esc_a -s A,B -nt 9,9,9,9,9,9,9 -pt 0 -nr 100 -nc 100 -pm 0.85 -tr 3000 -tc 1000 -cr 0.75 -cc 0.90 -mc 0.65
```
This will generate some samples in the directory `pool_esc_a/samples/`.

### **Mininum TaxAM command**
After this, copy the samples folder absolute path and go back to TaxAM. Let's try run the minimum taxam command:
```sh
python taxam -tl 1 -fp <samples_folder_path>
```
This command will create a taxam file in the path `taxam/output_taxam/` classifying the samples based in its first taxa level.

### **Changing the taxon level**
But, what it you want to classify it based in other level? Like the third level. Just change the flag `-tl 1` to `-tl 3`. Changing just this will replace your last file. Use the flag `-op` to change the output filename. Like:
```sh
python taxam -tl 3 -fp <samples_folder_path> -op "poolEscA_level3"
```

### Using a diferent separator
In default mode, TaxAM uses "\t"(tab) as a separator. Let's change it to see how it goes. For this, let's change the separator to the output file and use `-` as a separator, but you can use any one-character as separator, we recommmend that you keep using the default value. Follow the command:
```sh
python taxam -tl 3 -fp <samples_folder_path> -os "-" -op "poolEscA_with_a_different_separator"
```

### **What to do in a tie?**
When TaxAM is classifying a sample, it might happen that a read and a contig matched points to differents animals. So what was TaxAM supposed to do? By default, TaxAM will discard both animals, but you can change it paramter through flag `-fu`. If you want that it uses the animal from read, use the value `1`, if you want that it uses the animal from contig, uses value `2`. Run the following commands to see its differences:
```sh
python taxam -tl 1 -fp <samples_folder_path> -fu 1 -op "poolEscA_using_read_when_tie"
```
```sh
python taxam -tl 1 -fp <samples_folder_path> -fu 2 -op "poolEscA_using_contig_when_tie"
```
```sh
python taxam -tl 1 -fp <samples_folder_path> -op "poolEscA_using_no_one_when_tie"
```

### **Using more than 1 thread to run**
In this pool, we have two samples. By default, TaxAM will process each sample at a time. To increase its performance, you can specify it to run it in 2 threads at the same time. Just add the flag `-th 2`, according the number threads you need. Run the following command:
```sh
python taxam -tl 1 -fp <samples_folder_path> -th 2 -op "poolEscA_with_two_threads"
```

### **Changing the output matrix mode**
By default, TaxAM generate an absolute matrix, if you want to change this behavior, give it the flag `-mm 2`. Like:
```sh
python taxam -tl 1 -fp <samples_folder_path> -mm 2 -op "poolEscA_as_absolute_matrix"
```
TaxAM will count the classified reads to calculate the porcentage for each sample, but yourself can informe these values. Let's use our example: samples A e B use `A:100,B:150` as argument in the flag `-rq`, that is 100 reads for A, 150 reads for B. If you want that program calculate automatically for a specific sample, informe it as 0, for instance `A:0,B:125` that is 0 reads for A, 125 reads for B. Run the follow command to see it:
```sh
python taxam -tl 1 -fp <samples_folder_path> -mm 2 -rq "A:100,B:150" -op "poolEscA_as_manual_absolute_matrix"
```