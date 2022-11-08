# Taxam

[en](../../readme.md)

Taxam é uma plataforma de auxílio à preservação e recuperação ambiental de áreas Amazônicas sujeitas à mineração através de análise taxonômica microbiológica

## Anatomia dos arquivos
Para rodar o programa, você deve informar o caminho para o diretório contendo os arquivos de cada amostra. Todos os arquivos devem ser um arquivo `txt` (.txt), e cada amostra deve ter, pelo menos, um `Aarquivo Mapping` e um `Aarquivo Contigs`, e como opcional, um `Arquivo Reads`. Os nomes dos arquivos devem seguir o padrão `<tipo_do_arquivo>_<nome_da_amostra>.txt`, usando apenas um `_` (underline) no nome, por exemplo `mapping_amostra1.txt`.

1. `mapping_<nome_da_amostra>.txt`:
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
2. `contigs_<arquivo>.txt`:
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

3. `reads_<arquivo>.txt`:
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

## Saída
O arquivo de saída será uma matriz com todas as amostras e as informações taxonômicas. Este arquivo será salvo em um diretório chamado `output_taxam` no diretório `taxam`.
- Matriz Absoluta:
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
- Matriz Relativa:
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


## Como utilizar o Taxam
```sh
python taxam <flag_1> <valor_1> <flag_2> <valor_2> ...
```

### Flags:
- `-tl` ou `--tax_level`: Nível de taxonomia a ser usado. Níveis de taxonomia: 1-Reino, 2-Filo, 3-Classe, 4-Ordem, 5-Família, 6-Gênero, 7-Espécie. **[Obrigatório | Padrão: 1]**
- `-fp` ou `--folder_path`: Diretório onde estão os arquivos a serem usados. **[Obrigatório]**
- `-rs` ou `--reads_sep`: Separador usado para separar cada coluna no arquivo de reads. **[Opcional | Padrão: "\t"]**
- `-cs` ou `--contigs_sep`: Separador usado para separar cada coluna no arquivo de contigs. **[Opcional | Padrão: "\t"]**
- `-ms` or `--mapping_sep MAPPING_SEP`: Separator used to part each collumn in mapping file. **[Opcional | Padrão: "\t"]**
- `-ms` ou `--mapping_sep MAPPING_SEP`: Separador usado para separar cada coluna no arquivo de mapping. **[Opcional | Padrão: "\t"]**
- `-os` ou `--output_sep`: Separador usado para separar cada coluna no arquivo de saída gerado pelo TaxAM. **[Opcional | Padrão: "\t"]**
- `-op` ou `--output_name`: Nome do arquivo de saída gerado pelo TaxAM. **[Obrigatório | Padrão: "tx_matrix"]**
- `-fu` ou `--file_to_use`: Em caso de conflito, qual arquivo será usado. 1-Reads, 2-Contigs, 3-Nenhum. **[Obrigatório | Padrão: 3]**
- `-th` ou `--thread_number`: Número de threads a serem usadas. **[Opcional | Padrão: 1]**
- `-mm` ou `--matrix_mode`: Modo para criar a matriz. 1-Absoluta, 2-Relativa. **[Opcional | Padrão: 1]**
- `-rq` ou `--reads_quantity`: Quantidade de reads para cada amostra. Se houver 3 amostras: spa,spb, spc, use spa:100,spb:150,spc:275 que são 100 reads para spa, 150 reads para spb, 275 reads para spc. Se você quiser que o programa calcule automaticamente para uma amostra específica, informe 0, por exemplo spa:0,spb:125,spc:0 que são 0 reads para spa, 125 reads para spb, 0 reads para spc. **[Obrigatório apenas se o _matrix mode_ for 2]**

## Primeiros passos

### Gerando dados falsos
Primeiro, baixe o módulo do TaxAM que gera dados de taxa falsos, [clique aqui](https://github.com/TaxAM/taxamTestGenerator) para fazer o download. Em seguida, vamos criar alguns dados falsos para darmos uma brincada. Rode o seguinde comando:
```sh
python taxamTestGenerator -n pool_esc_a -s A,B -nt 9,9,9,9,9,9,9 -pt 0 -nr 100 -nc 100 -pm 0.85 -tr 3000 -tc 1000 -cr 0.75 -cc 0.90 -mc 0.65
```
Isso irá gerar algumas amostras no diretório `pool_esc_a/samples/`.

### Comando básico para o TaxAM
Em seguida, copie o caminho abosoluto da pasta das amostras e volte para o TaxAM. Vamos rodar o comando básico para o TaxAM funcionar:
```sh
python taxam -tl 1 -fp <samples_folder_path>
```
Esse comando irá criar arquivo do tipo taxam no diretório `taxam/output_taxam/` classificando as amostras com no primeiro level da taxa.

### Alterando o nível taxonômico
Mas e se você  quiser classificar suas amostras baseadas em outro nível taxonômico? Como o nível 3. É só alterar a flag `-tl 1` para `-tl 3`. Alterando apenas isso fazer com que seu arquivo anterior seja substituído pelo novo. Use a flag `-op` para mudar o nome do arquivo de saída. Como:
```sh
python taxam -tl 3 -fp <samples_folder_path> -op "poolEscA_level3"
```

### Usando um separador diferente
Por padrão, o TaxAM usa "\t"(tab) como separador. Vamos alterar isso e ver o que acontece. Para isso, vamos alterar o separador do arquivo de saída e usar `-` como um separador, mas você pode utilizar qualquer caractere singular como separador, nós recomendamos que você siga usando o valor padrão. Reproduza o comando abaixo:
```sh
python taxam -tl 3 -fp <samples_folder_path> -os "-" -op "poolEscA_with_a_different_separator"
```

### O que fazer em caso de empate?
Quando o TaxAM está cassificando uma amostra, pode acontecer de uma read e um contig mapeados juntos apontarem para diferentes bichos. O que o TaxAM deveria fazer nesse caso? Por padrão, o TaxAM irá descartar os dois bichos, mas é possível alterar esse parâmetro por meio da flag `-fu`. Se você quiser utilizar o bicho da read, use o valor `1`, se você quiser utilizar o bicho do contig, use o valor `2`. Execute os seguintes comandos para ver as diferenças:
```sh
python taxam -tl 1 -fp <samples_folder_path> -fu 1 -op "poolEscA_using_read_when_tie"
```
```sh
python taxam -tl 1 -fp <samples_folder_path> -fu 2 -op "poolEscA_using_contig_when_tie"
```
```sh
python taxam -tl 1 -fp <samples_folder_path> -op "poolEscA_using_no_one_when_tie"
```

### Utilizando mais do que uma thread na execução
Nesse conjunto de amostras, nós temos duas amostras. Por padrão, o TaxAM irá processar uma amostra por vez. Para melhorar sua performance, você pode rodá-lo em duas threads ao mesmo tempo. Basta acrescentar a flag `-th 2`, de acordo com o número de threads que você precise. Execute o seguinte comando:
```sh
python taxam -tl 1 -fp <samples_folder_path> -th 2 -op "poolEscA_with_two_threads"
```

### Alterando o mode de saída da matriz
Por padrão, o TaxAM gera uma matriz absoluta, se você quiser alterar esse comportamente, adicione a flag `-mm 2`. Por exemplo:
```sh
python taxam -tl 1 -fp <diretório_para_a_pasta_das_amostras> -mm 2 -op "poolEscA_as_absolute_matrix"
```
O TaxAM irá contar as reads classificadas para calcular a porcentagem para cada amostra, mas você pode informar esses valores. Vamos ver um exemplo: se houver as amostras A e B use A:100,B:150 que são 100 reads para A e  150 reads para B. Se você quiser que o programa calcule automaticamente para uma amostra específica, informe 0, por exemplo A:0,B:125 que são 0 reads para A, 125 reads para B.
```sh
python taxam -tl 1 -fp <diretório_para_a_pasta_das_amostras> -mm 2 -rq "A:100,B:150" -op "poolEscA_as_manual_absolute_matrix"
```