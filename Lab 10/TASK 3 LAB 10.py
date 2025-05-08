import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

students = pd.read_csv('student_data.csv')
features = students[['GPA', 'study_hours', 'attendance_rate']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
wcss = []
for k in range(2, 7):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)

plt.plot(range(2, 7), wcss, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
students['cluster'] = kmeans.fit_predict(scaled_features)
plt.figure(figsize=(10, 6))
colors = ['red', 'blue', 'green', 'purple', 'orange']
for i in range(optimal_k):
    cluster_data = students[students['cluster'] == i]
    plt.scatter(cluster_data['study_hours'], 
                cluster_data['GPA'], 
                c=colors[i], 
                label=f'Cluster {i+1}')

plt.title('Student Clusters by Study Hours and GPA')
plt.xlabel('Weekly Study Hours')
plt.ylabel('GPA')
plt.legend()
plt.grid(True)
plt.show()
print(students[['student_id', 'cluster']])