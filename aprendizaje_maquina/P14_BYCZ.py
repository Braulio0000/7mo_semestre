import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import dendrogram 
from sklearn.datasets import load_wine
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X = wine.data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

def plot_dendrogram(model, **kwargs):
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0 
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    dendrogram(linkage_matrix, **kwargs)

hac_model = AgglomerativeClustering(distance_threshold=0, n_clusters=None,
                                    metric='euclidean', linkage='ward')
hac_model = hac_model.fit(X_scaled)

plt.figure(figsize=(15, 7))
plt.title('Dendrograma de Clustering Jerárquico (Dataset Wine)')
plt.xlabel('Índice de la Muestra')
plt.ylabel('Distancia de Ward')

plot_dendrogram(hac_model, truncate_mode='level', p=5)

plt.axhline(y=15, color='r', linestyle='--')
plt.show()