import os


class ProjectGraph:
    def __init__(self, path, ignored=None):
        if ignored is None:
            ignored = {}
        self.__path = path
        self.__ignored = ignored
        self.__adj = {self.__path: []}
        self.__sources = {}
        self.__build()

    def __build(self):
        for (path, folders, files) in os.walk(self.__path):
            folders[:] = [folder for folder in folders if folder not in self.__ignored]
            if path not in self.__adj.keys():
                self.__adj[path] = []
            for folder in folders:
                self.__adj[path].append(os.path.join(path, folder))

            for file in files:
                if file.endswith('.py'):
                    filename = os.path.join(path, file)
                    with open(filename, 'r', encoding='UTF-8') as current_file:
                        self.__sources[filename] = current_file.read()
                    self.__adj[path].append(filename)
                    self.__adj[filename] = []

    def __dfs_print(self, used, cur, indent, indent_count):
        if cur not in used:
            print(indent + cur)
            used.add(cur)
            for child in self.__adj[cur]:
                self.__dfs_print(used, child, indent + ' ' * indent_count, indent_count)

    def print(self, indent_count=4):
        used = set()
        self.__dfs_print(used, self.__path, '', indent_count)

    def print_folder(self, folder_name, indent_count=4):
        used = set()
        self.__dfs_print(used, folder_name, '', indent_count)

    @property
    def get_source_codes(self):
        return self.__sources

    @property
    def get_adj_matrix(self):
        return self.__adj
