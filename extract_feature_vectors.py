import javalang
from pprint import pprint
import os
import pandas as pd
from find_god_classes import scan_files
import numpy as np

def get_methods(java_class) :
    methods = []
    for node in java_class.body :
        if isinstance(node,javalang.tree.MethodDeclaration):
            methods.append(node)

    return methods

def get_fields(java_class) :
    fields = []
    for node in java_class.body :
        if isinstance(node,javalang.tree.FieldDeclaration) :
            fields.append(node)
    return fields

def get_fields_accessed_by_method(method):
    fields = []
    for path,node in method.filter(javalang.tree.MemberReference):
        if not node.qualifier :
            if node.member not in fields :
                fields.append(node.member)
        elif node.qualifier not in fields :
            fields.append(node.qualifier)
    return fields


def get_methods_accessed_by_method(method):
    methods = []

    for path,node in method.filter(javalang.tree.MethodInvocation):
        if node.member not in methods :
            methods.append(node.member)
    return methods

def create_dict(arr):

    result = {}
    for entry in arr :
        if entry.name in result.keys():
            continue
        else :
            result[entry.name] = entry
    return result





def create_fv(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    
    with open(filepath, 'r') as file:
        source_code = file.read()

    tree = javalang.parse.parse(source_code)
    gt_dict = {}
    for path, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration) and node.name == filename:
            fields_nodes = get_fields(node)
            method_nodes = get_methods(node)
            
            fields = {field.declarators[0].name for field in fields_nodes}
            methods_dict = create_dict(method_nodes)
            
            methods = list(methods_dict.keys())
            gt_dict[filename] = methods
            
            combine = list(fields.union(methods))
            method_index = {method: i for i, method in enumerate(methods)}
            feature_index = {feature: i for i, feature in enumerate(combine)}
            
            data = np.zeros((len(methods), len(combine)), dtype=int)

            for method in methods:
                faccess = get_fields_accessed_by_method(methods_dict[method])
                maccess = get_methods_accessed_by_method(methods_dict[method])

                row_idx = method_index[method]
                for field in faccess:
                    if field in feature_index:
                        data[row_idx, feature_index[field]] = 1
                for m in maccess:
                    if m in feature_index:
                        data[row_idx, feature_index[m]] = 1

            df = pd.DataFrame(data, columns=combine)
            df.insert(0, 'method_name', methods)
            if not os.path.isdir('Data/fvs'):
                os.makedirs('Data/fvs')
            df.to_csv(f'Data/fvs/{filename}.csv', index=False)
    return gt_dict

    



            


