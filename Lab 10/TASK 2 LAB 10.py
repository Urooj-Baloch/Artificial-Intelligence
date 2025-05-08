import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder, StandardScaler

data = {
    'vehicle_serial_no': [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
    'mileage': [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000, 75000, 280000],
    'fuel_efficiency': [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
    'maintenance_cost': [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
    'vehicle_type': ['SUV', 'Sedan', 'Truck', 'Hatchback', 'Sedan', 'Truck', 'SUV', 'Truck', 'Hatchback', 'SUV']
}

df = pd.DataFrame(data)

numeric_features = ['mileage', 'fuel_efficiency', 'maintenance_cost']
categorical_features = ['vehicle_type']

preprocessor_unscaled = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

preprocessor_scaled = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

X = df[numeric_features + categorical_features]

X_unscaled = preprocessor_unscaled.fit_transform(X)
X_scaled = preprocessor_scaled.fit_transform(X)

kmeans_unscaled = KMeans(n_clusters=3, random_state=42)
kmeans_scaled = KMeans(n_clusters=3, random_state=42)

df['cluster_unscaled'] = kmeans_unscaled.fit_predict(X_unscaled)
df['cluster_scaled'] = kmeans_scaled.fit_predict(X_scaled)

print("Clustering Results:")
print(df[['vehicle_serial_no', 'vehicle_type', 'cluster_unscaled', 'cluster_scaled']])

def plot_clusters(X, clusters, title):
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X)
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=clusters, cmap='viridis')
    plt.title(title)
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.colorbar(scatter, label='Cluster')
    plt.show()

plot_clusters(X_unscaled, df['cluster_unscaled'], 'Clusters Without Feature Scaling')
plot_clusters(X_scaled, df['cluster_scaled'], 'Clusters With Feature Scaling')

print("\nCluster Characteristics (Unscaled):")
print(df.groupby('cluster_unscaled')[numeric_features].mean())

print("\nCluster Characteristics (Scaled):")
print(df.groupby('cluster_scaled')[numeric_features].mean())