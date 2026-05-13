import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

# Cargar el conjunto de datos Wine
wine = load_wine()
X = wine.data
y = wine.target
class_names = wine.target_names

# Normalizar los datos
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Reducir a 2 componentes para visualización 
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)

# Euclidiana (p=2)
knn_euc = KNeighborsClassifier(n_neighbors=5, p=2, weights='uniform')
knn_euc.fit(X_train, y_train)
y_pred_euc = knn_euc.predict(X_test)

print("=== Distancia Euclidiana ===")
print(f"Precisión: {accuracy_score(y_test, y_pred_euc):.4f}")
print(classification_report(y_test, y_pred_euc, target_names=class_names))

# Manhattan (p=1) 
knn_man = KNeighborsClassifier(n_neighbors=5, p=1, weights='uniform')
knn_man.fit(X_train, y_train)
y_pred_man = knn_man.predict(X_test)

print("=== Distancia Manhattan ===")
print(f"Precisión: {accuracy_score(y_test, y_pred_man):.4f}")
print(classification_report(y_test, y_pred_man, target_names=class_names))

x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05),
                     np.arange(y_min, y_max, 0.05))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, model, title in zip(axes,
                             [knn_euc, knn_man],
                             ["Euclidiana (p=2)", "Manhattan (p=1)"]):
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y, edgecolor='k', marker='o', s=50, cmap='viridis')
    ax.set_title(f"KNN Wine — {title}")
    ax.set_xlabel("Componente 1 (PCA)")
    ax.set_ylabel("Componente 2 (PCA)")

plt.tight_layout()
plt.show()