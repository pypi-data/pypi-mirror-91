from pyStaticAnalyzer.walker import ProjectGraph
import ast
from pyStaticAnalyzer.astpretty import pprint


class FolderNode:
    def __init__(self, name, type, ast):
        self.name = name
        self.type = type
        self.ast = ast
        self.children = {}


class CallNode:
    def __init__(self, id, name, type, imported_from=None):
        self.id = id
        self.name = name
        self.type = type
        self.imported_from = imported_from
        self.children = []


def print_ast(ast_node):
    pprint(ast_node)


def get_class_methods(class_node):
    if class_node.type != "class":
        return None

    res = {}
    for child in class_node.children.keys():
        if class_node.children[child].type == "function":
            res[child] = class_node.children[child]
    return res


def get_nested_classes(class_node):
    if class_node.type != "class":
        return None

    res = {}
    for child in class_node.children.keys():
        if class_node.children[child].type == "class":
            res[child] = class_node.children[child]
    return res


def get_nested_functions(func_node):
    if func_node.type != "function":
        return None

    res = {}
    for child in func_node.children.keys():
        if func_node.children[child].type == "function":
            res[child] = func_node.children[child]
    return res


def get_classes_from_function(func_node):
    if func_node.type != "function":
        return None

    res = {}
    for child in func_node.children.keys():
        if func_node.children[child].type == "class":
            res[child] = func_node.children[child]
    return res


def find_imports(node):
    res = {}
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ImportFrom):
            for name in child.names:
                res[name.name] = child.module
    return res


class FileKernel:
    def __init__(self, path):
        self.__path = path
        self.__file_tree = {}
        self.__sources = {}
        self.__create_tree()
        self.__parse_source_code()
        self.__call_graph_id = 0

    @property
    def get_path(self):
        return self.__path

    @property
    def get_all_tree(self):
        return self.__file_tree

    @property
    def get_source_codes(self):
        return self.__sources

    @property
    def get_structure(self):
        return {self.__path: []}

    def get_source_code(self, filename):
        return self.__sources[filename]

    def get_file_ast(self, filename):
        return self.__file_tree[filename].ast

    def get_file_classes_and_function(self, filename):
        return self.__file_tree[filename]

    def __look_for_func_in_class(self, node, name):
        functions = get_class_methods(node)
        classes = get_nested_classes(node)

        for func in functions:
            if functions[func].name == name:
                return functions[func].ast

        res = None
        for func in functions:
            res = self.__look_for_func_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_func_in_class(classes[cl], name)
            if res:
                return res

        return res

    def __look_for_func_in_func(self, node, name):
        functions = get_nested_functions(node)
        classes = get_classes_from_function(node)

        for func in functions:
            if functions[func].name == name:
                return functions[func].ast

        res = None
        for func in functions:
            res = self.__look_for_func_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_func_in_class(classes[cl], name)
            if res:
                return res

        return res

    def __look_for_class_in_class(self, node, name):
        functions = get_class_methods(node)
        classes = get_nested_classes(node)

        for cl in classes:
            if classes[cl].name == name:
                return classes[cl].ast

        res = None
        for func in functions:
            res = self.__look_for_class_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_class_in_class(classes[cl], name)
            if res:
                return res

        return res

    def __look_for_class_in_func(self, node, name):
        functions = get_nested_functions(node)
        classes = get_classes_from_function(node)

        for cl in classes:
            if classes[cl].name == name:
                return classes[cl].ast

        res = None
        for func in functions:
            res = self.__look_for_class_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_class_in_class(classes[cl], name)
            if res:
                return res

        return res

    def find_function_ast(self, file, name):
        file_content = self.get_file_classes_and_function(file)

        for val in file_content.children:
            if file_content.children[val].name == name and file_content.children[val].type == "function":
                return file_content.children[val].ast
        res = None
        for val in file_content.children:
            if file_content.children[val].type == "function":
                res = self.__look_for_func_in_func(file_content.children[val], name)
                if res:
                    return res
            if file_content.children[val].type == "class":
                res = self.__look_for_func_in_class(file_content.children[val], name)
                if res:
                    return res
        return res

    def find_class_ast(self, file, name):
        file_content = self.get_file_classes_and_function(file)

        for val in file_content.children:
            if file_content.children[val].name == name and file_content.children[val].type == "class":
                return file_content.children[val].ast
        res = None
        for val in file_content.children:
            if file_content.children[val].type == "function":
                res = self.__look_for_class_in_func(file_content.children[val], name)
                if res:
                    return res
            if file_content.children[val].type == "class":
                res = self.__look_for_class_in_class(file_content.children[val], name)
                if res:
                    return res
        return res

    def print_file_ast(self, filename):
        pprint(self.__file_tree[filename].ast)

    def print_all_asts(self):
        pprint(self.__file_tree[self.__path].ast)

    def print_structure(self):
        print(self.__path)

    def __parse_source_code(self):
        with open(self.__path, 'r', encoding='UTF-8') as current_file:
            self.__sources[self.__path] = current_file.read()

    def __dfs_file_ast(self, used, name, prefix, cur_ast, file_dict):
        if prefix + name not in used:
            used.add(prefix + name)
            for cl in cur_ast.body:
                if isinstance(cl, ast.ClassDef):
                    file_dict[cl.name] = FolderNode(cl.name, "class", cl)
                    self.__dfs_file_ast(used, cl.name, prefix + cl.name, cl, file_dict[cl.name].children)
            for func in cur_ast.body:
                if isinstance(func, ast.FunctionDef):
                    file_dict[func.name] = FolderNode(func.name, "function", func)
                    self.__dfs_file_ast(used, func.name, prefix + func.name, func, file_dict[func.name].children)

    def __create_tree(self):
        with open(self.__path, 'r', encoding='UTF-8') as file:
            cur_ast = ast.parse(file.read(), filename=self.__path, mode='exec')
        self.__file_tree[self.__path] = FolderNode(self.__path, "file", cur_ast)
        tree_used = set()
        self.__dfs_file_ast(tree_used, self.__path, "", cur_ast, self.__file_tree[self.__path].children)

    def __find_calls(self, node, res):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                continue

            if isinstance(child, ast.Call):
                res.append(child)
                continue

            self.__find_calls(child, res)

    def __inspect_func_ast(self, graph, imports, filename, func_ast):
        calls = []
        self.__find_calls(func_ast, calls)
        for call in calls:
            if isinstance(call.func, ast.Name):
                if call.func.id in imports.keys():
                    self.__call_graph_id += 1
                    graph.children.append(
                        CallNode(self.__call_graph_id, call.func.id, "imported_function", imported_from=imports[call.func.id]))
                elif call.func.id not in self.__file_tree[filename].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "function"))
                elif self.__file_tree[filename].children[call.func.id].type == "class":
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "class"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.id, "function")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(filename, call.func.id)
                    self.__inspect_func_ast(node, imports, filename, func_ast)
            elif isinstance(call.func, ast.Attribute):
                if call.func.attr not in self.__file_tree[filename].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.attr, "method"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.attr, "method")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(filename, call.func.attr)
                    self.__inspect_func_ast(node, imports, filename, func_ast)

    def build_call_graph(self):
        file_ast = self.__file_tree[self.__path].ast
        imports = find_imports(file_ast)
        graph = CallNode(self.__call_graph_id, 'main', 'main')
        calls = []
        self.__find_calls(file_ast, calls)
        for call in calls:
            if isinstance(call.func, ast.Name):
                if call.func.id in imports.keys():
                    self.__call_graph_id += 1
                    graph.children.append(
                        CallNode(self.__call_graph_id, call.func.id, "imported_function", imported_from=imports[call.func.id]))
                elif call.func.id not in self.__file_tree[self.__path].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "function"))
                elif self.__file_tree[self.__path].children[call.func.id].type == "class":
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "class"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.id, "function")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(self.__path, call.func.id)
                    self.__inspect_func_ast(node, imports, self.__path, func_ast)
            elif isinstance(call.func, ast.Attribute):
                if call.func.attr not in self.__file_tree[self.__path].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.attr, "method"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.attr, "method")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(self.__path, call.func.attr)
                    self.__inspect_func_ast(node, imports, self.__path, func_ast)
        return graph

    def __dfs_call_graph_print(self, used, cur, indent, indent_count):
        if cur.id not in used:
            used.add(cur.id)
            print(indent + cur.type + " " + cur.name)
            for child in cur.children:
                self.__dfs_call_graph_print(used, child, indent + ' ' * indent_count, indent_count)

    def print_call_graph(self, indent_count=4):
        graph = self.build_call_graph()
        used = set()
        self.__dfs_call_graph_print(used, graph, '', indent_count)


class ProjectKernel:

    def __init__(self, path, ignored=None):
        if ignored is None:
            ignored = {}
        self.__path = path
        self.__graph = ProjectGraph(path, ignored=ignored)
        self.__folder_tree = {}
        self.__call_graph_id = 0
        self.__create_tree()

    @property
    def get_path(self):
        return self.__path

    @property
    def get_all_tree(self):
        return self.__folder_tree

    @property
    def get_source_codes(self):
        return self.__graph.get_source_codes

    @property
    def get_structure(self):
        return self.__graph.get_adj_matrix

    def get_source_code(self, filename):
        return self.__graph.get_source_codes[filename]

    def get_file_ast(self, filename):
        return self.__folder_tree[filename].ast

    def get_file_classes_and_function(self, filename):
        return self.__folder_tree[filename]

    def __look_for_func_in_class(self, node, name):
        functions = get_class_methods(node)
        classes = get_nested_classes(node)

        for func in functions:
            if functions[func].name == name:
                return functions[func].ast

        res = None
        for func in functions:
            res = self.__look_for_func_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_func_in_class(classes[cl], name)
            if res:
                return res

        return res

    def __look_for_func_in_func(self, node, name):
        functions = get_nested_functions(node)
        classes = get_classes_from_function(node)

        for func in functions:
            if functions[func].name == name:
                return functions[func].ast

        res = None
        for func in functions:
            res = self.__look_for_func_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_func_in_class(classes[cl], name)
            if res:
                return res

        return res

    def __look_for_class_in_class(self, node, name):
        functions = get_class_methods(node)
        classes = get_nested_classes(node)

        for cl in classes:
            if classes[cl].name == name:
                return classes[cl].ast

        res = None
        for func in functions:
            res = self.__look_for_class_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_class_in_class(classes[cl], name)
            if res:
                return res

        return res

    def __look_for_class_in_func(self, node, name):
        functions = get_nested_functions(node)
        classes = get_classes_from_function(node)

        for cl in classes:
            if classes[cl].name == name:
                return classes[cl].ast

        res = None
        for func in functions:
            res = self.__look_for_class_in_func(functions[func], name)
            if res:
                return res

        for cl in classes:
            res = self.__look_for_class_in_class(classes[cl], name)
            if res:
                return res

        return res

    def find_function_ast(self, file, name):
        file_content = self.get_file_classes_and_function(file)

        for val in file_content.children:
            if file_content.children[val].name == name and file_content.children[val].type == "function":
                return file_content.children[val].ast
        res = None
        for val in file_content.children:
            if file_content.children[val].type == "function":
                res = self.__look_for_func_in_func(file_content.children[val], name)
                if res:
                    return res
            if file_content.children[val].type == "class":
                res = self.__look_for_func_in_class(file_content.children[val], name)
                if res:
                    return res
        return res

    def find_class_ast(self, file, name):
        file_content = self.get_file_classes_and_function(file)

        for val in file_content.children:
            if file_content.children[val].name == name and file_content.children[val].type == "class":
                return file_content.children[val].ast
        res = None
        for val in file_content.children:
            if file_content.children[val].type == "function":
                res = self.__look_for_class_in_func(file_content.children[val], name)
                if res:
                    return res
            if file_content.children[val].type == "class":
                res = self.__look_for_class_in_class(file_content.children[val], name)
                if res:
                    return res
        return res

    def print_file_ast(self, filename):
        pprint(self.__folder_tree[filename].ast)

    def print_folder_asts(self, folder):
        used = set()
        self.__dfs_print(used, folder)

    def print_all_asts(self):
        used = set()
        self.__dfs_print(used, self.__path)

    def print_structure(self, indent_count=4):
        self.__graph.print(indent_count)

    def print_folder(self, folder_name, indent_count=4):
        self.__graph.print_folder(folder_name, indent_count)

    def __dfs_print(self, used, cur):
        if cur not in used:
            if cur.endswith(".py"):
                print(cur)
                self.print_file_ast(cur)
                print()
            used.add(cur)
            for child in self.__graph.get_adj_matrix[cur]:
                self.__dfs_print(used, child)

    def __dfs_file_ast(self, used, name, prefix, cur_ast, file_dict):
        if prefix + name not in used:
            used.add(prefix + name)
            for cl in cur_ast.body:
                if isinstance(cl, ast.ClassDef):
                    file_dict[cl.name] = FolderNode(cl.name, "class", cl)
                    self.__dfs_file_ast(used, cl.name, prefix + cl.name, cl, file_dict[cl.name].children)
            for func in cur_ast.body:
                if isinstance(func, ast.FunctionDef):
                    file_dict[func.name] = FolderNode(func.name, "function", func)
                    self.__dfs_file_ast(used, func.name, prefix + func.name, func, file_dict[func.name].children)

    def __dfs_ast(self, used, cur):
        if cur not in used:
            used.add(cur)
            if cur.endswith(".py"):
                with open(cur, 'r', encoding='UTF-8') as file:
                    cur_ast = ast.parse(file.read(), filename=cur, mode='exec')
                self.__folder_tree[cur] = FolderNode(cur, "file", cur_ast)
                tree_used = set()
                self.__dfs_file_ast(tree_used, cur, "", cur_ast, self.__folder_tree[cur].children)
            for child in self.__graph.get_adj_matrix[cur]:
                self.__dfs_ast(used, child)

    def __create_tree(self):
        used = set()
        self.__dfs_ast(used, self.__path)

    def __find_calls(self, node, res):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                continue

            if isinstance(child, ast.Call):
                res.append(child)
                continue

            self.__find_calls(child, res)

    def __inspect_func_ast(self, graph, imports, filename, func_ast):
        calls = []
        self.__find_calls(func_ast, calls)
        for call in calls:
            if isinstance(call.func, ast.Name):
                if call.func.id in imports.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "imported_function", imported_from=imports[call.func.id]))
                elif call.func.id not in self.__folder_tree[filename].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "function"))
                elif self.__folder_tree[filename].children[call.func.id].type == "class":
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "class"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.id, "function")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(filename, call.func.id)
                    self.__inspect_func_ast(node, imports, filename, func_ast)
            elif isinstance(call.func, ast.Attribute):
                if call.func.attr not in self.__folder_tree[filename].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.attr, "method"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.attr, "method")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(filename, call.func.attr)
                    self.__inspect_func_ast(node, imports, filename, func_ast)

    def build_call_graph(self, filename):
        file_ast = self.__folder_tree[filename].ast
        imports = find_imports(file_ast)
        graph = CallNode(self.__call_graph_id, 'main', 'main')
        calls = []
        self.__find_calls(file_ast, calls)
        for call in calls:
            if isinstance(call.func, ast.Name):
                if call.func.id in imports.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "imported_function", imported_from=imports[call.func.id]))
                elif call.func.id not in self.__folder_tree[filename].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "function"))
                elif self.__folder_tree[filename].children[call.func.id].type == "class":
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.id, "class"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.id, "function")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(filename, call.func.id)
                    self.__inspect_func_ast(node, imports, filename, func_ast)
            elif isinstance(call.func, ast.Attribute):
                if call.func.attr not in self.__folder_tree[filename].children.keys():
                    self.__call_graph_id += 1
                    graph.children.append(CallNode(self.__call_graph_id, call.func.attr, "method"))
                else:
                    self.__call_graph_id += 1
                    node = CallNode(self.__call_graph_id, call.func.attr, "method")
                    graph.children.append(node)
                    func_ast = self.find_function_ast(filename, call.func.attr)
                    self.__inspect_func_ast(node, imports, filename, func_ast)
        return graph

    def __dfs_call_graph_print(self, used, cur, indent, indent_count):
        if cur.id not in used:
            used.add(cur.id)
            print(indent + cur.type + " " + cur.name)
            for child in cur.children:
                self.__dfs_call_graph_print(used, child, indent + ' ' * indent_count, indent_count)

    def print_call_graph(self, filename, indent_count=4):
        graph = self.build_call_graph(filename)
        used = set()
        self.__dfs_call_graph_print(used, graph, '', indent_count)

