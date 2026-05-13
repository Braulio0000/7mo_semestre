import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score, 
                             recall_score, f1_score, roc_curve, auc)

X, y = load_wine(return_X_y=True)
y = (y == 0).astype(int) # Convertir a clasificación binaria

X_ent, X_pru, y_ent, y_pru = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

escalador = StandardScaler()
X_ent = escalador.fit_transform(X_ent)
X_pru = escalador.transform(X_pru)

iteraciones = [1, 15, 50, 100]
resultados = {}

for it in iteraciones:
    modelo = LogisticRegression(max_iter=it, solver="lbfgs")
    modelo.fit(X_ent, y_ent)
    y_pred = modelo.predict(X_pru)
    y_prob = modelo.predict_proba(X_pru)[:, 1]
    
    cm = confusion_matrix(y_pru, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    acc = accuracy_score(y_pru, y_pred)
    prec = precision_score(y_pru, y_pred, zero_division=0)
    rec = recall_score(y_pru, y_pred, zero_division=0)
    esp = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = f1_score(y_pru, y_pred, zero_division=0)
    
    fpr, tpr, _ = roc_curve(y_pru, y_prob)
    roc_auc = auc(fpr, tpr)
    
    resultados[it] = {
        "cm": cm, "acc": acc, "prec": prec, "rec": rec, 
        "esp": esp, "f1": f1, "fpr": fpr, "tpr": tpr, "auc": roc_auc
    }
    
    print(f"\niteraciones: {it}")
    print(f"Matriz de confusion (tn fp / fn tp):\n{cm}")
    print(f"Accuracy: {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall: {rec:.4f}")
    print(f"Especificidad: {esp:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")

plt.figure()
for it in iteraciones:
    plt.plot(resultados[it]["fpr"], resultados[it]["tpr"], 
             label=f"{it} it (AUC={resultados[it]['auc']:.3f})")

plt.plot([0, 1], [0, 1], linestyle="--", linewidth=1)
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.title("ROC-AUC")
plt.legend()
plt.grid(True)
plt.show()