import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.preprocessing import StandardScaler


wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)

hac_final = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')

etiquetas_hac = hac_final.fit_predict(X_scaled) 

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
etiquetas_kmeans = kmeans.fit_predict(X_scaled)

df_comparacion = pd.DataFrame({
    'K-Means': etiquetas_kmeans,
    'HAC': etiquetas_hac 
})

tabla_contingencia = pd.crosstab(df_comparacion['HAC'], df_comparacion['K-Means'])

plt.figure(figsize=(10, 8))
sns.heatmap(tabla_contingencia, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Contingencia: HAC vs K-means (Wine Dataset)')
plt.xlabel('Etiquetas K-means')
plt.ylabel('Etiquetas HAC')
plt.show()