import pandas as pd
from sklearn.cluster import KMeans,AgglomerativeClustering
from find_god_classes import scan_files
import os


def clustering(choice,god,k = 5) :
    '''
    Applies clustering algorithm to the feature vectors and creates new csv files with the cluster_id.
    choice : Algorithm to apply as string
    god : Name of the god class as string
    k : Number of clusters to create(default = 5)
    '''

    df = pd.read_csv('Data/fvs/' + god + '.csv')
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
