import numpy as np
from sklearn.linear_model import LinearRegression

datos_entrada = np.array([
    [15, 10],
    [22, 5],
    [9, 9],
    [12, 4],
    [18, 7]
], dtype=float)

objetivo = np.array([100, 65, 82, 60, 91], dtype=float)

regresion = LinearRegression(fit_intercept=True)
regresion.fit(datos_entrada, objetivo)

sesgo = regresion.intercept_
peso1, peso2 = regresion.coef_

print(sesgo, peso1, peso2)
print("y =", round(sesgo, 2), "+", round(peso1, 2), "* x1 +", round(peso2, 2), "* x2")

parametros = np.array([0.0, 0.0, 0.0])
tasa_aprendizaje = 0.0001

matriz_diseno = np.column_stack((np.ones(len(datos_entrada)), datos_entrada))

prediccion = matriz_diseno @ parametros
residuo = prediccion - objetivo

derivada = matriz_diseno.T @ residuo

parametros_actualizados = parametros - tasa_aprendizaje * derivada

print(parametros_actualizados)
print("theta0 =", round(parametros_actualizados[0], 4),
      "theta1 =", round(parametros_actualizados[1], 4),
      "theta2 =", round(parametros_actualizados[2], 4))