import argparse
from pyStaticAnalyzer.kernel import FileKernel, ProjectKernel, print_ast
from pyStaticAnalyzer.checker import Checker
parser = argparse.ArgumentParser("command line linter interface")

parser.add_argument("--file-ast", dest="filename_ast", action="store", type=str, help='print file ast')
parser.add_argument("--folder-asts", dest="folder", action="store", type=str, help='print folder asts')
parser.add_argument("--structure", dest="folder_structure", action="store", type=str, help='print folder structure')
parser.add_argument("--call-graph", dest="filename_graph", action="store", type=str, help='print call graph')
parser.add_argument("--function-ast", dest="function_ast", action="store", type=str, help='print function ast (must '
                                                                                          'be used with --file)')
parser.add_argument("--class-ast", dest="class_ast", action="store", type=str, help='print class ast (must be used '
                                                                                    'with --file)')
parser.add_argument("--file", dest="filename", action="store", type=str, help='filename for function and class ast '
                                                                              'search')
parser.add_argument("--check-file", dest="filename_check", action="store", type=str, help='run checks for file')
parser.add_argument("--check-folder", dest="folder_check", action="store", type=str, help='run checks for folder')

args = parser.parse_args()
if args.filename_ast:
    kernel = FileKernel(args.filename_ast)
    kernel.print_file_ast(args.filename_ast)
elif args.folder:
    kernel = ProjectKernel(args.folder, ignored={'venv', '.idea', '__pycache__'})
    kernel.print_folder_asts(args.folder)
elif args.folder_structure:
    kernel = ProjectKernel(args.folder_structure, ignored={'venv', '.idea', '__pycache__'})
    kernel.print_structure()
elif args.filename_graph:
    kernel = FileKernel(args.filename_graph)
    kernel.print_call_graph()
elif args.function_ast:
    kernel = FileKernel(args.filename)
    function_ast = kernel.find_function_ast(args.filename, args.function_ast)
    print_ast(function_ast)
elif args.class_ast:
    kernel = FileKernel(args.filename)
    class_ast = kernel.find_class_ast(args.filename, args.class_ast)
    print_ast(class_ast)
elif args.filename_check:
    kernel = FileKernel(args.filename_check)
    c = Checker()
    c.run_all_checks([[kernel], [kernel]])
elif args.folder_check:
    kernel = ProjectKernel(args.folder_check)
    c = Checker()
    c.run_all_checks([[kernel], [kernel]])



