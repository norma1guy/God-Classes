import javalang
from pprint import pprint
import os
import pandas as pd
from find_god_classes import get_path

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
    source_code = open(filepath).read()
    tree = javalang.parse.parse(source_code)
    for path,node in tree :
        if isinstance(node,javalang.tree.ClassDeclaration) and  node.name == filename:
            fields_nodes = get_fields(node)
            method_nodes = get_methods(node)
            fields = list(set([field.declarators[0].name for field in fields_nodes]))
            methods_dict = create_dict(method_nodes)
            methods = list(methods_dict.keys())
            combine = fields + methods
            data = [[0] * len(combine) for _ in methods]
            df = pd.DataFrame(data,columns = combine)
            df.insert(0,'method_name',methods)
            for method in methods :
                faccess =get_fields_accessed_by_method(methods_dict[method])
                maccess = get_methods_accessed_by_method(methods_dict[method])
                for index,row in df.iterrows():
                    if row['method_name'] == method :
                        for entry in faccess:
                            df.at[index,entry] = 1
                        for entry in maccess:
                            df.at[index,entry] = 1
            df = df.fillna(0)
            
            df.to_csv('Data/fvs/' + filename + '.csv',index=False)


if __name__ == "__main__":

    god_classes = get_path('Scan/resources')
    os.makedirs('Data/fvs/')
    for god in god_classes:
        create_fv(god)

    



            


