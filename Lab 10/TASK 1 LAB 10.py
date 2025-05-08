import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('Wall_Customers.csv')
X_all = df.drop('customer_id', axis=1).values

wcss_list1 = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_all)
    wcss_list1.append(kmeans.inertia_)
    
plt.plot(range(1, 11), wcss_list1)
plt.title('Elbow Method - No Scaling')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans1 = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_predict1 = kmeans1.fit_predict(X_all)

scaler = StandardScaler()
cols_to_scale = [i for i, col in enumerate(df.columns) if col not in ['customer_id', 'age']]
X_scaled = X_all.copy()
X_scaled[:, cols_to_scale] = scaler.fit_transform(X_all[:, cols_to_scale])

wcss_list2 = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss_list2.append(kmeans.inertia_)
    
plt.plot(range(1, 11), wcss_list2)
plt.title('Elbow Method - Scaled Features (except age)')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans2 = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_predict2 = kmeans2.fit_predict(X_scaled)

comparison = pd.DataFrame({
    'No_Scaling': y_predict1,
    'Scaled_Except_Age': y_predict2
})
print(comparison.head(20))