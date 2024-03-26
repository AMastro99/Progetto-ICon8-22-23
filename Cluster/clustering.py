import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import silhouette_score
from Preprocessing import preprocessing


def categorical_feature_encoding(dataset):
    categorical_features = ['qualifica', 'anzianita', 'classificazione']

    onehot_encoder = OneHotEncoder(sparse_output=False)
    encoded_dataset = onehot_encoder.fit_transform(dataset[categorical_features])

    return pd.concat([dataset.drop(columns=categorical_features), pd.DataFrame(encoded_dataset)], axis=1)


def elbow_method(dataset):
    dataset = np.array(dataset)
    wcss = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans.fit(dataset)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, 11), wcss, 'bx-')
    plt.title("elbow method")
    plt.xlabel("Numero di cluster (K)")
    plt.ylabel("WCSS")
    plt.show()


def clustering(dataset, k_cluster):
    dataset = np.array(dataset)
    kmeans = KMeans(n_clusters=k_cluster, n_init=10, random_state=42)
    kmeans.fit(dataset)
    validation(kmeans, dataset)
    return kmeans.labels_


def validation(k_means, dataset):
    wcss = k_means.inertia_
    print("\nWCSS:", wcss)

    silhouette_avg = silhouette_score(dataset, k_means.labels_)
    print("Silhouette Score:", silhouette_avg)


def inizia_clustering():
    preprocessing.preprocessing()
    dataset_path = '../dataset/datasetForClustering.csv'
    dataset = pd.read_csv(dataset_path)
    encoded_dataset = categorical_feature_encoding(dataset)
    elbow_method(encoded_dataset)

    if os.path.exists("../dataset/dataset+Cluster.csv"):
        clustering(encoded_dataset, 2)
    else:
        cluster_result = clustering(encoded_dataset, 2)
        dataset_path = '../dataset/dataset.csv'
        dataset = pd.read_csv(dataset_path)
        dataset['cluster'] = cluster_result
        dataset.to_csv("../dataset/dataset+Cluster.csv", index=False)

    preprocessing.elimina_preprocessing()
