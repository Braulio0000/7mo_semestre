import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

wine = load_wine()
X = wine.data
y = wine.target
feature_names = wine.feature_names
class_names = wine.target_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

profundidades = [3, 5, 10]

for depth in profundidades:
    arbol = DecisionTreeClassifier(criterion='entropy', max_depth=depth, random_state=42)
    arbol.fit(X_train, y_train)
    
    plt.figure(figsize=(20, 10))
    plot_tree(arbol,
              feature_names=feature_names,
              class_names=class_names,
              filled=True,
              fontsize=10,
              rounded=True)
    plt.title(f'Árbol de Decisión - Profundidad Máxima: {depth}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()