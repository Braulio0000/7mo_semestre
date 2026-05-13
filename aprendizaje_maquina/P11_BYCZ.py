import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine

wine_raw = load_wine()
wine = pd.DataFrame(wine_raw.data, columns=wine_raw.feature_names)
wine['clase'] = wine_raw.target
X = wine[['alcohol', 'flavanoids']]

def distancia_euclidiana(punto1, punto2):
    suma_cuadrados = 0
    for i in range(len(punto1)):
        suma_cuadrados += (punto1[i] - punto2[i]) ** 2
    return np.sqrt(suma_cuadrados)

k = 3
np.random.seed(42)
indices_aleatorios = np.random.choice(X.shape[0], k, replace=False)
centroides = X.iloc[indices_aleatorios].values
print(f"Índices iniciales: {indices_aleatorios}")
print(f"Centroides iniciales:\n{centroides}\n")

colores = ['#2196F3', '#4CAF50', '#F44336']   # azul, verde, rojo
num_iteraciones = 10
historial_centroides = [centroides.copy()]

for iteracion in range(num_iteraciones):
    asignaciones = []
    for idx, punto in X.iterrows():
        distancias = []
        for centroide in centroides:
            distancias.append(distancia_euclidiana(punto.values, centroide))
        cluster_asignado = np.argmin(distancias)
        asignaciones.append(cluster_asignado)
    asignaciones = np.array(asignaciones)
    conteo = [np.sum(asignaciones == i) for i in range(k)]
    print(f"Iteración {iteracion+1:2d} | Puntos por cluster: {conteo} | "
          f"Centroides: {np.round(centroides, 3).tolist()}")

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    for i in range(k):
        puntos_cluster = np.array([X.iloc[j].values
                                   for j in range(len(X)) if asignaciones[j] == i])
        if len(puntos_cluster) > 0:
            ax.scatter(puntos_cluster[:, 0], puntos_cluster[:, 1],
                       color=colores[i], label=f'Cluster {i+1} (n={len(puntos_cluster)})',
                       alpha=0.75, edgecolors='white', linewidths=0.6, s=70)

    ax.scatter(centroides[:, 0], centroides[:, 1],
               color='black', marker='X', s=280, zorder=6,
               label='Centroides', linewidths=1.2)

    if iteracion > 0:
        traj = np.array(historial_centroides)
        for ci in range(k):
            ax.plot(traj[:, ci, 0], traj[:, ci, 1],
                    color=colores[ci], linestyle='--', alpha=0.4, linewidth=1.5)

    ax.set_title(f'K-Means — Wine Dataset  |  Iteración {iteracion+1}/{num_iteraciones}',
                 fontsize=14, fontweight='bold', pad=14)
    ax.set_xlabel('Alcohol', fontsize=12)
    ax.set_ylabel('Flavanoides', fontsize=12)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.8)
    ax.grid(True, linestyle='--', alpha=0.35)
    plt.tight_layout()
    plt.show()

    nuevos_centroides = []
    for i in range(k):
        puntos_cluster = np.array([X.iloc[j].values
                                   for j in range(len(X)) if asignaciones[j] == i])
        if len(puntos_cluster) > 0:
            nuevo_x = np.mean(puntos_cluster[:, 0])
            nuevo_y = np.mean(puntos_cluster[:, 1])
            nuevos_centroides.append([nuevo_x, nuevo_y])
        else:
            nuevos_centroides.append(centroides[i])
    centroides = np.array(nuevos_centroides)
    historial_centroides.append(centroides.copy())