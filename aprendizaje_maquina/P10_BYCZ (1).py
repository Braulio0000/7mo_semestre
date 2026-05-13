import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.compose import ColumnTransformer

data_frutas = {
    'Peso':     [150, 160, 170, 145, 155,
                 180, 190, 185, 200, 195,
                 100, 105, 110,  95, 115],
    'Diametro': [7.1, 7.3, 7.5, 7.0, 7.2,
                 8.1, 8.3, 8.0, 8.5, 8.2,
                 5.1, 5.3, 5.5, 5.0, 5.4],
    'pH':       [4.5, 4.4, 4.6, 4.5, 4.3,
                 3.8, 3.7, 3.9, 3.6, 3.8,
                 2.2, 2.3, 2.1, 2.4, 2.2],
    'Fruta':    ['Manzana', 'Manzana', 'Manzana', 'Manzana', 'Manzana',
                 'Naranja', 'Naranja', 'Naranja', 'Naranja', 'Naranja',
                 'Limon',   'Limon',   'Limon',   'Limon',   'Limon']
}

df = pd.DataFrame(data_frutas)

print("--- Dataset Original (Primeras filas) ---")
print(df.head(3))

X = df[['Peso', 'Diametro', 'pH']]
y = df['Fruta']

modelo = GaussianNB()
modelo.fit(X, y)

nuevo_dia = pd.DataFrame({
    'Peso':     [175],
    'Diametro': [7.8],
    'pH':       [4.0]
})

prediccion    = modelo.predict(nuevo_dia)
probabilidades = modelo.predict_proba(nuevo_dia)

print(f"¿Qué fruta es?: {prediccion[0]}")
print(f"Probabilidades: {dict(zip(modelo.classes_, probabilidades[0].round(6)))}")