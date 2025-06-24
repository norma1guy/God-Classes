import javalang
import os
import pandas as pd
from pprint import pprint

def scan_files(folder) :
    '''
    Returns dataframe containing the top 4 classes according to the number of methods they have.
    Has class_name,method_num and path columns
    '''
    records = []
    df = pd.DataFrame(columns = ['class_name','method_num'])

    for root,dir,files in os.walk(folder):
        for file in files:
            if file.endswith('.java'):
                source = os.path.join(root,file)
                with open(source,'r',encoding='utf-8',errors='ignore') as f:
                    try :
                        source_code = f.read()
                        tree = javalang.parse.parse(source_code)
                        for node in tree.types :
                            if isinstance(node,javalang.tree.ClassDeclaration):
                                count = sum(isinstance(inner,javalang.tree.MethodDeclaration) for inner in node.body)
                                records.append((node.name,count,source))
                    except (javalang.parser.JavaSyntaxError,UnicodeDecodeError):
                        continue             
    df = pd.DataFrame(records,columns=['class_name','method_num','path'])
    return df.sort_values('method_num',ascending=False).iloc[0:4]




