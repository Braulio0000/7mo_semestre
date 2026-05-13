import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load the Wine dataset
wine = load_wine()
X = wine.data
y = wine.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Name of the features and classes
feature_names = wine.feature_names
class_names = wine.target_names

# Train with 10, 50 and 100 trees
n_trees = [10, 50, 100]

for n in n_trees:
    # Create a Random Forest Classifier
    bosque = RandomForestClassifier(n_estimators=n, random_state=42)

    # Train the model
    bosque.fit(X_train, y_train)

    # Make predictions
    y_pred = bosque.predict(X_test)

    # Evaluate the model
    print(f"Precision del Bosque ({n} arboles): {accuracy_score(y_test, y_pred)*100:.2f}%")
    print("Reporte de clasificación:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    car_imp = bosque.feature_importances_

    # Visualize feature importance
    colores = ['red', 'green', 'blue', 'orange', 'purple', 'cyan',
               'magenta', 'yellow', 'brown', 'pink', 'gray', 'teal', 'navy']
    plt.figure(figsize=(10, 6))
    plt.bar(feature_names, car_imp, color=colores)
    plt.title(f'Importancia de las características ({n} árboles)')
    plt.xlabel('Características')
    plt.ylabel('Importancia')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()