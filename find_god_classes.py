import javalang
import os
import pandas as pd
from pprint import pprint



def scan_files(folder) :

    df = pd.DataFrame(columns = ['class_name','method_num'])

    for root,dir,files in os.walk(folder):
        for file in files:
            if file.endswith('.java'):
                source = os.path.join(root,file)
                source_code = open(source).read()
                tree = javalang.parse.parse(source_code)
                for path,node in tree :
                    if isinstance(node,javalang.tree.ClassDeclaration):
                        count = 0
                        for inner in node.body :
                            if isinstance(inner,javalang.tree.MethodDeclaration) :
                                count += 1
                        df = df._append({'class_name': node.name,'method_num' : count},ignore_index = True)
    return df.sort_values('method_num',ascending=False).iloc[0:4]['class_name']

def get_path(folder) :
    gods = scan_files(folder)
    paths = []
    for god in gods :
        for root,dir,files in os.walk('Scan/resources'):
            for file in files:
                if file.endswith('.java'):
                    filepath = os.path.join(root,file)
                    filename = os.path.splitext(os.path.basename(filepath))[0]
                    if filename == god :
                        paths.append(filepath)
    return paths





