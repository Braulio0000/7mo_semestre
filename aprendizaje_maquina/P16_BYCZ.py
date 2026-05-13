import numpy as np
from sklearn.datasets import load_iris

# Funciones de activación
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def umbral(a):
    return 1 if a >= 0.5 else 0

# Cargar dataset Iris
iris = load_iris()
X_full = iris.data
y_full = iris.target

# Seleccionar solo las dos últimas clases (1: versicolor, 2: virginica)
mask = y_full >= 1
X_filtered = X_full[mask]
y_filtered = y_full[mask] - 1  # Reescalar etiquetas a 0 y 1

# Usar solo Largo y Ancho del Pétalo (columnas 2 y 3)
X = X_filtered[:, 2:4]

# Pesos: cada fila = pesos de esa neurona de entrada hacia las 5 neuronas ocultas
w_oculta = np.array([
    [5, 0, 0, 0, 0],   # Neurona 1 (Largo Pétalo)
    [2, 0, 0, 0, 0]    # Neurona 2 (Ancho Pétalo)
])

w_salida = np.array([10, 0, 0, 0, 0])

b_oculta = np.array([-12, 0, 0, 0, 0])
b_salida = -5

# Inferencia
print(f"{'#':<5} {'Largo Pét':>10} {'Ancho Pét':>10} {'y_real':>8} {'y_pred':>8} {'OK':>5}")
print("-" * 45)

correct = 0
for i, x in enumerate(X):
    z_oculta = np.dot(x, w_oculta) + b_oculta
    a_oculta = sigmoid(z_oculta)

    z_salida = np.dot(a_oculta, w_salida) + b_salida
    a_salida = sigmoid(z_salida)

    y_pred = umbral(a_salida)
    y_real = y_filtered[i]
    ok = "✓" if y_pred == y_real else "✗"
    if y_pred == y_real:
        correct += 1

    print(f"{i+1:<5} {x[0]:>10.2f} {x[1]:>10.2f} {y_real:>8} {y_pred:>8} {ok:>5}")

print("-" * 45)
print(f"Precisión: {correct}/{len(X)} = {correct/len(X)*100:.1f}%")