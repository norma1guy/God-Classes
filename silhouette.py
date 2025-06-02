from sklearn.metrics import silhouette_score
import pandas as pd
from find_god_classes import scan_files
from clustering import clustering

def compute_silhouette(god,havefile,max=0):
    algos = ['kmeans','agglo']
    fv = pd.read_csv(god+'.csv')
    X = fv.drop(['method_name'],axis=1)
    X = X.values

    for algo in algos :
        if havefile == 'y' :
            cluster_df = pd.read_csv(god + '_' + algo + '.csv')
            score = silhouette_score(X,cluster_df['cluster_id'])
            print(algo,score)
        
        else :
            results = {}
            for k in range(2,max + 1):
                clusterfile = clustering(algo,god,k)
                cluster_df = pd.read_csv(clusterfile)
                score = silhouette_score(X,cluster_df['cluster_id'])
                results.update({k:score})
            print(algo,results)
            

if __name__ == '__main__':

    gods = scan_files('Scan/resources')
    while True:
        print('Select which god class you want to calculate the silhouette score for\n')
        for index,value in gods.items() :
            print(f'{index}.{gods.loc[index]}\n')

        file = int(input('Enter the number\n'))
        filename = gods.loc[file]
        choice = input('Do you have a clustering file ?(y/n)')
        if choice=='n' :
            k = int(input('Till how many clusters do you want to calculate the silhoutte score?\n'))
        if choice == 'y':
            compute_silhouette(filename,choice)
        else :
            compute_silhouette(filename,choice,k)
        cont = input('Do you want to continue? (y/n)\n')
        if cont == 'n':
            break
    



