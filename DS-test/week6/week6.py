#Data and plotting imports
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

#Machine learning imports
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree

#Loading the breast cancer dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# A Function to plot decision boundarys
def plot_decision(X,y,model,n_classes=2):
    min1, max1 = X[:, 0].min()-1, X[:, 0].max()+1
    min2, max2 = X[:, 1].min()-1, X[:, 1].max()+1
    x1grid = np.arange(min1, max1, 0.1)
    x2grid = np.arange(min2, max2, 0.1)
    xx, yy = np.meshgrid(x1grid, x2grid)
    grid = np.c_[xx.ravel(), yy.ravel()]
    model.fit(X, y)
    yhat = model.predict(grid)
    zz = yhat.reshape(xx.shape)
    plt.contourf(xx, yy, zz, cmap='coolwarm', alpha=0.8)
    plt.scatter(X[:,0], X[:,1], c=y, cmap='coolwarm', edgecolors='k')

#Pick two features
feature1 = 'mean radius'
feature2 = 'mean texture'
X = df[[feature1, feature2]].values
y = df['target'].values

#Comparison of different k values(3/5/10)
plt.figure(figsize=(15,5))
for i, k in enumerate([3, 5, 10]):
    plt.subplot(1, 3, i+1)
    model = KNeighborsClassifier(n_neighbors=k)
    plot_decision(X, y, model)
    plt.title(f'KNN (k={k}) Decision Boundary')
    plt.xlabel(feature1)
    plt.ylabel(feature2)
plt.tight_layout()
plt.show()

#Comparison of different depth values(2/4/6)
plt.figure(figsize=(15,5))
for i, depth in enumerate([2, 4, 6]):
    plt.subplot(1, 3, i+1)
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    plot_decision(X, y, model)
    plt.title(f'Decision Tree (max_depth={depth})')
    plt.xlabel(feature1)
    plt.ylabel(feature2)
plt.tight_layout()
plt.show()

feature_pairs = [
    ('mean radius', 'mean texture'),
    ('worst radius', 'worst texture'),
    ('mean concave points', 'mean symmetry')
]

plt.figure(figsize=(15,5))
for i, (p1, p2) in enumerate(feature_pairs):
    X = df[[p1, p2]].values
    model = DecisionTreeClassifier(max_depth=3)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    
    plt.subplot(1, 3, i+1)
    plot_decision(X, y, model)
    plt.title(f'{p1} / {p2}\nAccuracy: {acc:.2%}')
    plt.xlabel(p1)
    plt.ylabel(p2)
plt.tight_layout()
plt.show()

#Use all features
X = df.drop('target', axis=1).values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Fit model
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
print("\nAccuracy:", model.score(X_test, y_test))

plt.figure(figsize=(20,10))
my_plot = plot_tree(model, feature_names=data.feature_names,fontsize=10,class_names = ["Malignant","Benign"]) 

plt.show()