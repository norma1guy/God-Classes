import pandas as pd
from sklearn.cluster import KMeans,AgglomerativeClustering
from find_god_classes import scan_files
import os


def clustering(choice,god,k = 5) :

    df = pd.read_csv(god + '.csv')
    X = df.drop(['method_name'],axis=1)
    X = X.values
    if choice == 'kmeans':
        clusters = KMeans(n_clusters=k,random_state=0).fit(X)
    else :
        clusters = AgglomerativeClustering(n_clusters=k).fit(X)
    df.insert(0,'cluster_id',clusters.labels_)
    df = df[['cluster_id','method_name']]
    df.to_csv('Data/clustering/' + god+ f'_{choice}.csv',index=False)
    return f'Data/clustering/{god}_{choice}.csv'


if __name__ == "__main__" :
    os.makedirs('Data/clustering/')
    algos = ['kmeans','agglo']
    gods = scan_files('Scan/resources')
    for algo in algos :
        for god in gods :
            clustering(algo,god)