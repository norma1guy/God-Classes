import pandas as pd
from find_god_classes import scan_files
import os 
import re
from collections import Counter

def extract_keywords_from_method_name(method_name):
    # Split camelCase and snake_case into words
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', method_name)  # camelCase → camel Case
    words = words.replace('_', ' ')  # snake_case → snake case
    return words.lower().split()

def generate_ground_truth_keywords(df, methods_dict, method_threshold=10, top_n=20, output_file="ground_truth_keywords.txt"):
    """
    df: DataFrame with 'class_name' and 'method_num'
    methods_dict: dict where keys are filenames, values are list of method names
    method_threshold: number of methods beyond which a class is suspicious
    top_n: number of top keywords to write to file
    """

    keyword_counter = Counter()

    for _, row in df.iterrows():
        filename = row['class_name']
        num_methods = row['method_num']

        if num_methods >= method_threshold:
            method_names = methods_dict.get(filename, [])
            for method in method_names:
                keywords = extract_keywords_from_method_name(method)
                keyword_counter.update(keywords)

    # Get the most common keywords
    most_common_keywords = keyword_counter.most_common(top_n)
    
    words = []

    for keyword, count in most_common_keywords:
        words.append(keyword)
    
    return words


def create_ground_truth(words,fv,name):
    df = pd.read_csv(fv)
    df.insert(0,'cluster_id',0)
    for i in range(len(words)) :
        for index,value in df.iterrows():
            if words[i] in value['method_name'].lower() and df.at[index,'cluster_id'] == 0:
                df.at[index,'cluster_id'] = i + 1
    df = df[['cluster_id','method_name']]
    if not os.path.isdir('Data/gt'):
        os.makedirs('Data/gt')
    df.to_csv('Data/gt/' + name + '_ground-truth.csv',index=False)



    
    