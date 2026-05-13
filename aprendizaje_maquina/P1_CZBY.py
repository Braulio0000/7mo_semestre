import numpy as np
import matplotlib.pyplot as plt

x_datos = [30, 40, 40, 50, 50, 50, 60, 70, 70]
y_datos = [70, 90, 100, 120, 130, 150, 160, 190, 200]

while True:
    n = len(x_datos)
    x = np.array(x_datos)
    y = np.array(y_datos)
    m = (n*np.sum(x*y)-np.sum(x)*np.sum(y))/(n*np.sum(x**2)-np.sum(x)**2)
    b = (np.sum(y)-m*np.sum(x))/n
    print(f"\nModelo: y = {m:.4f}x + ({b:.4f})")
    prediccion_15v = m * 15 + b
    print(f"Predicción a 15V: {prediccion_15v:.2f} RPM")
    # Gráficas 
    plt.scatter(x, y, color='blue', label='Datos medidos')
    plt.plot(x, m*x+b, color='red', label=f'Regresión (m={m:.2f})')
    # Etiquetas 
    plt.title(f'Motor DC (n={n})')
    plt.xlabel('V')
    plt.ylabel('RPM')
    plt.grid(True, linestyle='--', alpha=0.7) 
    plt.legend()
    plt.show() 

    continuar = input("Deseas agregar otro dato? (s/n): ")
    if continuar.lower() == 's':
        try:
            nuevo_x = float(input("Ingresa X: "))
            nuevo_y = float(input("Ingresa Y: "))
            x_datos.append(nuevo_x)
            y_datos.append(nuevo_y)
        except ValueError:
            print("Error: Debes ingresar números válidos.")
    else:
        break