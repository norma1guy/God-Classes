from find_god_classes import scan_files
from extract_feature_vectors import create_fv
from prec_recall import calc_pre_recall
from clustering import clustering
from silhouette import compute_silhouette
from ground_truth import generate_ground_truth_keywords,create_ground_truth
import pandas as pd
from pprint import pprint
import os

def output(folder,algos = ['kmeans','agglo']):
    god_classes = scan_files(folder)
    if not os.path.isdir('Data'):
        os.makedirs('Data')

    
    #Create FVs for all the god classes
    gt_dict = {}
    for index,god in god_classes.iterrows():
        gt_dict.update(create_fv(god['path']))
    
    fv_prefix = 'Data/fvs/'
    #Apply clustering algorithms 
    if not os.path.isdir('Data/clustering'):
        os.makedirs('Data/clustering')
    cluster_prefix = 'Data/clustering/'
    for algo in algos :
        for index,god in god_classes.iterrows():
            clustering(algo,god['class_name']) 

    #Create keywords for  ground truth based on the method names used
    
    #Create the ground truth csvs
    for index,god in god_classes.iterrows():
        create_ground_truth(generate_ground_truth_keywords(god_classes,gt_dict),fv_prefix+god['class_name']+'.csv',god['class_name'])
    
    gt_prefix = 'Data/gt/'


    #Calculate the precision and recall for god classes    
    for index,god in god_classes.iterrows():
        for algo in algos :
            cluster_file = cluster_prefix + god['class_name'] + '_' + algo + '.csv'
            ground_truth = gt_prefix + god['class_name'] + '_ground-truth.csv'
            print(f'The god class {god["class_name"]} for the algorithm {algo} has \n')
            calc_pre_recall(cluster_file,ground_truth)

    #Calculate silhouette score for god classes
    result = []
    for index,god in god_classes.iterrows():
        for algo in algos :
            result.append(compute_silhouette(god['class_name'],algo))
    
    pprint(result)


    
    
    

    
        
    






    

if __name__ == '__main__' :
    #folder = sys.argv[1]
    output('Scan/resources')


