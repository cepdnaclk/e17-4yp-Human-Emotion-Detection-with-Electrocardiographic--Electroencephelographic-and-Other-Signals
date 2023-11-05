import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np

for i in range (23):
    for j in range (18):
        data = pd.read_csv(f'./DREAMER/EEG/{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv')
        X = data.iloc[:, :14]

        # scaler = StandardScaler()
        # X_scaled = scaler.fit_transform(X)

        pca = PCA(n_components=2)
        # X_pca = pca.fit_transform(X_scaled)
        X_pca = pca.fit_transform(X)

        pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
        output_directory = f'./DREAMER/PCA_EEG/{i+1}/{j+1}'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_csv_path = os.path.join(output_directory, f'{i+1}_{j+1}_stimuli.csv')
        pca_df.to_csv(output_csv_path, index=False, header=False)
