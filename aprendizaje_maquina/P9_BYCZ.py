import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import KMeans
from scipy.sparse.csgraph import minimum_spanning_tree

np.random.seed(42)

CLASS_NAMES = ["T-shirt", "Pantalón", "Suéter", "Vestido", "Abrigo",
               "Sandalia", "Camisa", "Zapatilla", "Bolso", "Botín"]

def make_data(n=3000):
    X, y = [], []
    for cls in range(10):
        center = np.random.randn(784) * 0.5
        samples = center + np.random.randn(n // 10, 784) * 0.3
        X.append(samples)
        y.extend([cls] * (n // 10))
    return np.vstack(X), np.array(y)

X, y = make_data()
print(f"Dataset: {X.shape}")

def tmap(X, n_pca=30, k=15, n_iter=60):
    X_pca = PCA(n_components=n_pca, random_state=42).fit_transform(X)
    graph = kneighbors_graph(X_pca, k, mode='distance')
    mst   = minimum_spanning_tree(graph).toarray()

    pos = X_pca[:, :2].copy().astype(float)
    pos = (pos - pos.mean(0)) / (pos.std() + 1e-8)
    rows, cols = np.where(mst > 0)
    lr = 0.12
    for _ in range(n_iter):
        F = np.zeros_like(pos)
        for i in range(0, len(pos), 10):
            d = pos[i] - pos + 1e-6
            F += (d / (np.linalg.norm(d, axis=1, keepdims=True)**2 + 1e-6)).mean(0)
        for r, c in zip(rows, cols):
            f = 0.3 * (pos[c] - pos[r])
            F[r] += f; F[c] -= f
        pos += lr * F
        lr  *= 0.97
    return (pos - pos.mean(0)) / (pos.std() + 1e-8), mst

print("Calculando TMAP global...")
layout, mst = tmap(X)


colors = plt.cm.tab10(np.linspace(0, 1, 10))

fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#111')
for ax in axes:
    ax.set_facecolor('#111')

ax = axes[0]
for cls in range(10):
    m = y == cls
    ax.scatter(layout[m, 0], layout[m, 1], s=8, c=[colors[cls]],
               alpha=0.7, label=CLASS_NAMES[cls])

ri, ci = np.where(mst > 0)
for i in np.random.choice(len(ri), min(500, len(ri)), replace=False):
    ax.plot([layout[ri[i],0], layout[ci[i],0]],
            [layout[ri[i],1], layout[ci[i],1]], 'w-', alpha=0.04, lw=0.4)
ax.legend(fontsize=7, labelcolor='white', facecolor='#222', framealpha=0.5)
ax.set_title("TMAP – Fashion-MNIST", color='white', fontsize=13)
ax.tick_params(colors='gray')


ax2 = axes[1]
for cls in range(10):
    m = y == cls
    cx, cy = layout[m, 0].mean(), layout[m, 1].mean()
    ax2.scatter(cx, cy, s=250, c=[colors[cls]], zorder=5, edgecolors='w', lw=1)
    ax2.annotate(CLASS_NAMES[cls], (cx, cy), xytext=(5, 3),
                 textcoords='offset points', color='white', fontsize=7)
ax2.set_title("Centroides por clase", color='white', fontsize=13)
ax2.set_facecolor('#111'); ax2.tick_params(colors='gray')

plt.tight_layout()
plt.savefig('fig1_global.png', dpi=130, bbox_inches='tight', facecolor='#111')
plt.show()

mask = np.isin(y, [5, 7, 9])
X_fw, y_fw = X[mask], y[mask]

print("Calculando TMAP calzado...")
layout_fw, mst_fw = tmap(X_fw, n_pca=20, k=10, n_iter=50)

sub = KMeans(n_clusters=5, random_state=42, n_init=10).fit_predict(
      PCA(n_components=20, random_state=42).fit_transform(X_fw))

fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#111')
fw_col = {5: '#F4A261', 7: '#2A9D8F', 9: '#E76F51'}
sub_col = plt.cm.Set2(np.linspace(0, 1, 5))

for ax in axes: ax.set_facecolor('#111')

ax = axes[0]
for cls, name in zip([5,7,9], ["Sandalia","Zapatilla","Botín"]):
    m = y_fw == cls
    ax.scatter(layout_fw[m,0], layout_fw[m,1], s=12, c=fw_col[cls], alpha=0.8, label=name)
ax.legend(fontsize=9, labelcolor='white', facecolor='#222')
ax.set_title("TMAP – Calzado", color='white', fontsize=13)
ax.tick_params(colors='gray')

ax2 = axes[1]
for s in range(5):
    m = sub == s
    ax2.scatter(layout_fw[m,0], layout_fw[m,1], s=12, c=[sub_col[s]],
                alpha=0.8, label=f"Subcluster {s+1}")
ax2.legend(fontsize=9, labelcolor='white', facecolor='#222')
ax2.set_title("Subclusters en Calzado", color='white', fontsize=13)
ax2.tick_params(colors='gray')

plt.tight_layout()
plt.savefig('fig2_calzado.png', dpi=130, bbox_inches='tight', facecolor='#111')
plt.show()
from scipy.spatial.distance import cdist
X_pca_fw = PCA(n_components=20, random_state=42).fit_transform(X_fw)
centers   = np.array([X_pca_fw[sub==s].mean(0) for s in range(5)])

fig, axes = plt.subplots(5, 5, figsize=(9, 9), facecolor='#111')
fig.suptitle("Imágenes por Subcluster", color='white', fontsize=13)

for s in range(5):
    m = sub == s
    dists = cdist([centers[s]], X_pca_fw[m])[0]
    top5  = np.argsort(dists)[:5]
    imgs  = X_fw[m][top5]
    for j in range(5):
        ax = axes[s][j]
        ax.imshow(imgs[j].reshape(28, 28), cmap='Blues_r')
        ax.set_xticks([]); ax.set_yticks([])
        if j == 0:
            ax.set_ylabel(f"SC {s+1}", color='white', fontsize=9)
        for sp in ax.spines.values():
            sp.set_color(sub_col[s]); sp.set_linewidth(1.5)

plt.tight_layout()
plt.savefig('fig3_imagenes.png', dpi=130, bbox_inches='tight', facecolor='#111')
plt.show()

print("✅ Listo. Figuras guardadas: fig1_global.png, fig2_calzado.png, fig3_imagenes.png")