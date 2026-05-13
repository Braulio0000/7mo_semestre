import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

# Datos: primera columna, 100 instancias
diabetes = load_diabetes()
X = diabetes.data[:100, 0:1]
y = diabetes.target[:100]

# Línea de valores posibles para predicción
X_line = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)

# Configuración
K_VALUES = [1, 5, 15]
COLORES  = {1: '#E74C3C', 5: '#2ECC71', 15: '#3498DB'}
METRICAS = [('euclidean', 'Euclidiana'), ('manhattan', 'Manhattan')]

# Una sola figura: fila 1 = Euclidiana | fila 2 = Manhattan
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
fig.patch.set_facecolor('#F8F9FA')
fig.suptitle('KNN Regresión — Dataset Diabetes | 100 instancias · Primera columna',
             fontsize=14, fontweight='bold', color='#2C3E50', y=1.01)

for row, (metrica, nombre) in enumerate(METRICAS):

    # Etiqueta lateral por fila
    fig.text(0.01, 0.75 - row * 0.5, f'Distancia\n{nombre}',
             fontsize=11, fontweight='bold', color='#2C3E50',
             va='center', ha='left', rotation=90)

    for col, k in enumerate(K_VALUES):
        ax = axes[row][col]

        # Entrenar y predecir
        knn = KNeighborsRegressor(n_neighbors=k, metric=metrica)
        knn.fit(X, y)
        mse = mean_squared_error(y, knn.predict(X))

        # Estilo del panel
        ax.set_facecolor('white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#DEE2E6')
        ax.grid(True, linestyle='--', alpha=0.5, color='#DEE2E6')
        ax.tick_params(colors='#6C757D', labelsize=8)

        # Datos reales y línea de predicción
        ax.scatter(X, y, color='#ADB5BD', s=25, alpha=0.6, zorder=2, label='Datos reales')
        ax.plot(X_line, knn.predict(X_line), color=COLORES[k], linewidth=2.5,
                zorder=3, label=f'Predicción K={k}')

        # Título de columna solo en la primera fila
        if row == 0:
            ax.set_title(f'K = {k}', fontsize=13, fontweight='bold',
                         color=COLORES[k], pad=10)

        ax.set_xlabel('BMI normalizado', fontsize=9, color='#6C757D')
        ax.set_ylabel('Progresión Diabetes', fontsize=9, color='#6C757D')
        ax.legend(fontsize=8, framealpha=0.9, loc='upper left')

        # MSE en esquina inferior derecha
        ax.text(0.97, 0.05, f'MSE = {mse:,.0f}',
                transform=ax.transAxes, fontsize=8, ha='right', va='bottom',
                color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORES[k], alpha=0.85))

# Línea divisoria entre filas
fig.add_artist(plt.Line2D([0.05, 0.98], [0.5, 0.5],
               transform=fig.transFigure, color='#DEE2E6', linewidth=1.5))

plt.subplots_adjust(hspace=0.35, wspace=0.3, left=0.07)
plt.savefig('knn_resultado.png', dpi=150, bbox_inches='tight', facecolor='#F8F9FA')
plt.show()