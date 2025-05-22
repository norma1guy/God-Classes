import javalang
from pprint import pprint
from find_god_classes import scan_files

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

'''def get_fields_accessed_by_method(method):
    
    for node in method.body :
        if isinstance(node,javalang.tree)'''

#def get_methods_accessed_by_method(method):



test = javalang.parse.parse("class A { int x;int y ; int f() { x = 69; y = 1; x = x*y;return 0;} int g(){return 0; class B{int h(){return 0;} int y ;}}  }")
for path,node in test :
    if isinstance(node,javalang.tree.MethodDeclaration):
        pprint(node)

