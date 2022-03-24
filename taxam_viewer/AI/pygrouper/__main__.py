from sklearn.cluster import KMeans
import pandas as pd

matrix = pd.read_csv(
    './src/saida-reino-no-one.taxam',
    delimiter = '\t',
    index_col= 'TaxAM'
)
print('Original Matrix:')
print(matrix)

transposed_matrix = matrix.transpose()

print('\nTransposed Matrix:')
print(transposed_matrix)

model = KMeans(n_clusters=2)

groups = model.fit_predict(transposed_matrix)

print('\nNumber of groups: 2.')
print('Groups:')
print(groups)