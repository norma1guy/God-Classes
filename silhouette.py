from sklearn.metrics import silhouette_score
import pandas as pd
from find_god_classes import scan_files
from clustering import clustering

def compute_silhouette(god,algo):
    fv = pd.read_csv('Data/fvs/' + god + '.csv')
    X = fv.drop(['method_name'],axis=1)
    X = X.values
    data = []

    results = []
    
    cluster_df = pd.read_csv('Data/clustering/' + god + '_' + algo + '.csv')
    score = silhouette_score(X,cluster_df['cluster_id'])
    results.append({'Clusters' :len(cluster_df['cluster_id'].unique()),'Score' : score})
    
    data.append({'Algorithm' : algo,'Results': results})

    return data
            
            

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
    



