from sklearn.cluster import KMeans
import pandas as pd

matrix = pd.read_csv(
    './src/a_output_level0_tie-contig.taxam',
    delimiter = '\t',
    index_col= 'TaxAM'
)

model = KMeans(n_clusters=2)

groups = model.fit_predict(matrix)

print(matrix)
print(groups)