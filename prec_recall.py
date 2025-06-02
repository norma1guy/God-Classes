import pandas as pd
from itertools import combinations
from find_god_classes import scan_files

def calc_pre_recall(cluster,gt):

    cluster_df = pd.read_csv(cluster)
    gt_df = pd.read_csv(gt)
    combined_df = pd.merge(cluster_df,gt_df,on='method_name',suffixes=('_prediction','_truth'))
    pairs = list(combinations(combined_df.index, 2)) 
    TP = FP = FN = 0

    for i, j in pairs:
        same_pred = combined_df.loc[i, 'cluster_id_prediction'] == combined_df.loc[j, 'cluster_id_prediction']
        same_true = combined_df.loc[i, 'cluster_id_truth'] == combined_df.loc[j, 'cluster_id_truth']

        if same_pred and same_true:
            TP += 1
        elif same_pred and not same_true:
            FP += 1
        elif not same_pred and same_true:
            FN += 1

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")


if __name__ == '__main__' :
    gods = scan_files('Scan/resources')
    for god in gods :
        algos = ['kmeans','agglo']
        for algo in algos :
            cluster_file = 'Data/clustering/' + god + '_' + algo + '.csv'
            ground_truth = 'Data/gt/' + god + '_ground-truth.csv'
            print(f'\nThe god class {god} for the algorithm {algo} has\n')
            calc_pre_recall(cluster_file,ground_truth)
