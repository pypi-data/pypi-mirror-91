from functools import wraps
import ast
import re


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args):
            return func(*args)

        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally

    return decorator


class Checker:
    def __init__(self):
        pass

    def get_all_checks(self):
        checks = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith("check")]
        return checks

    def run_check(self, name, *args):
        check = getattr(self, name)
        return check(*args)

    def run_all_checks(self, args=None):
        checks = self.get_all_checks()
        if not args:
            for i in range(len(checks)):
                self.run_check(checks[i])
        else:
            for i in range(len(checks)):
                self.run_check(checks[i], *args[i])


def dfs_check_bad_names(k, bad_names_list, cur, used):
    if cur not in used:
        if cur.endswith(".py"):
            messages = []
            cur_ast = k.get_file_ast(cur)
            for node in ast.walk(cur_ast):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) \
                        and node.id in bad_names_list:
                    messages.append(
                        "line {}: C0102 Black listed name \"{}\" (blacklisted-name)".format(node.lineno, node.id))
                elif isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) \
                        and node.name in bad_names_list:
                    messages.append(
                        "line {}: C0102 Black listed name \"{}\" (blacklisted-name)".format(node.lineno, node.name))
                elif isinstance(node, ast.Attribute) \
                        and node.attr in bad_names_list:
                    messages.append(
                        "line {}: C0102 Black listed name \"{}\" (blacklisted-name)".format(node.lineno, node.attr))
            if messages:
                print(cur)
                for message in messages:
                    print(message)
                print()
        used.add(cur)
        for child in k.get_structure[cur]:
            dfs_check_bad_names(k, bad_names_list, child, used)


def dfs_check_invalid_names(k, good_names_list, regexs, cur, used):
    if cur not in used:
        if cur.endswith(".py"):
            messages = []
            cur_ast = k.get_file_ast(cur)
            for node in ast.walk(cur_ast):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name not in good_names_list and regexs['function-rgx'].match(node.name) is None:
                        messages.append(
                            "line {}: C0103 invalid function name \"{}\"".format(node.lineno, node.name))
                    for arg in node.args.args:
                        if arg.arg not in good_names_list and regexs['argument-rgx'].match(arg.arg) is None:
                            messages.append(
                                "line {}: C0103 invalid argument name \"{}\"".format(node.lineno, arg.arg))
                if isinstance(node, ast.Attribute) and node.attr not in good_names_list and regexs['attr-rgx'].match(
                        node.attr) is None:
                    messages.append(
                        "line {}: C0103 invalid attribute name \"{}\"".format(node.lineno, node.attr))
                if isinstance(node, ast.ClassDef) and node.name not in good_names_list and regexs['class-rgx'].match(
                        node.name) is None:
                    messages.append(
                        "line {}: C0103 invalid class name \"{}\"".format(node.lineno, node.name))
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id not in good_names_list and regexs['class-rgx'].match(
                        node.id) is None:
                    messages.append(
                        "line {}: C0103 invalid variable name \"{}\"".format(node.lineno, node.id))
                if isinstance(node, ast.ImportFrom) and node.module not in good_names_list and regexs['module-rgx'].match(
                        node.module) is None:
                    messages.append(
                        "line {}: C0103 invalid module name \"{}\"".format(node.lineno, node.module))
            if messages:
                print(cur)
                for message in messages:
                    print(message)
                print()
        used.add(cur)
        for child in k.get_structure[cur]:
            dfs_check_invalid_names(k, good_names_list, regexs, child, used)


# pylint C0102
@add_method(Checker)
def check_bad_names(k, bad_names_list=None):
    if bad_names_list is None:
        bad_names_list = ["foo", "bar", "baz", "toto", "tutu", "tata"]
    used = set()
    dfs_check_bad_names(k, bad_names_list, k.get_path, used)


# pylint C0103
@add_method(Checker)
def check_invalid_names(k, good_names_list=None, regexs=None):
    if good_names_list is None:
        good_names_list = []
    defaults_regexs = {'argument-rgx': re.compile('[a-z_][a-z0-9_]{2,30}$'),
                       'attr-rgx': re.compile('[a-z_][a-z0-9_]{2,30}$'),
                       'class-rgx': re.compile('[A-Z_][a-zA-Z0-9]+$'),
                       'function-rgx': re.compile('[a-z_][a-z0-9_]{2,30}$'),
                       'module-rgx': re.compile('(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$'),
                       'variable-rgx': re.compile('[a-z_][a-z0-9_]{2,30}$')}
    if regexs is not None:
        for key in regexs.keys():
            defaults_regexs[key] = re.compile(regexs[key])
    used = set()
    dfs_check_invalid_names(k, good_names_list, defaults_regexs, k.get_path, used)
