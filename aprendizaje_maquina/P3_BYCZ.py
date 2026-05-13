import numpy as np
import matplotlib.pyplot as plt

X = np.array([
    [1, 2],
    [2, 3],
    [3, 2],
    [4, 4],
    [5, 5],
    [6, 4],
    [7, 6],
    [8, 8],
    [9, 9],
    [10, 8]
])

Y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

w = np.array([0.6, 1.2])
b = -8.0

z = np.dot(X, w) + b
probabilidad = 1 / (1 + np.exp(-z))
prediccion = (probabilidad >= 0.5).astype(int)

print("z:", z)
print("Probabilidades:", probabilidad)
print("Predicción:", prediccion)

plt.figure(figsize=(10, 5))
z_limites = np.linspace(z.min() - 2, z.max() + 2, 200)
sigmoide = 1 / (1 + np.exp(-z_limites))

plt.plot(z_limites, sigmoide)
plt.scatter(z, probabilidad, s=100)
plt.grid(True)
plt.title("Sigmoide")
plt.show()

x_vals = np.linspace(0, 12, 100)
y_vals = (8 - 0.6 * x_vals) / 1.2

plt.figure(figsize=(6,6))
plt.plot(x_vals, y_vals)

for i in range(len(X)):
    plt.scatter(X[i,0], X[i,1])

plt.xlabel("Horas de Estudio (x1)")
plt.ylabel("Promedio en Tareas (x2)")
plt.title("Frontera de Decisión")
plt.grid(True)
plt.show()
