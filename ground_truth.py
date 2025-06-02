import pandas as pd
from find_god_classes import scan_files
import os 
def create_ground_truth(words,fv,name):
    df = pd.read_csv(fv)
    df.insert(0,'cluster_id',0)
    for i in range(len(words)) :
        for index,value in df.iterrows():
            if words[i] in value['method_name'].lower() and df.at[index,'cluster_id'] == 0:
                df.at[index,'cluster_id'] = i + 1
    df = df[['cluster_id','method_name']]
    df.to_csv('Data/gt/' + name + '_ground-truth.csv',index=False)

if __name__ == '__main__':

    os.makedirs('Data/gt/')
    with open('keywords.txt','r') as file :
        words = file.read().split(',')
    gods = scan_files('Scan/resources')
    for god in gods:
        fv_file = god + '.csv'
        create_ground_truth(words,fv_file,god)

    
    