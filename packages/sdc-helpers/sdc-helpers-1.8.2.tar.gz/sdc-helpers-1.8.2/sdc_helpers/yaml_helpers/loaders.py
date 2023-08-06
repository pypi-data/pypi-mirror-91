"""Yaml Loader Constructors"""
import os
import yaml

def get_yaml_config(filepath: str, loader: yaml.SafeLoader = None) -> dict:
    """flexible yaml loader that takes defaults to safeloader"""
    if loader is None:
        loader = yaml.SafeLoader

    with open(filepath, 'r') as file_:
        return yaml.load(file_, Loader=loader)

class ExtendedSafeLoader(yaml.SafeLoader):
    """Extensible yaml.SafeLoader class where we add extra constructor"""

    # pylint: disable=too-many-ancestors
    def __init__(self, stream):
        """init ExtendedSafeLoader"""
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)

    def include(self, node):
        """macro to include !include function to yaml.load"""
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as file_:
            return yaml.load(file_, Loader=ExtendedSafeLoader)

    def join(self, node):
        """macro to include !join function to yaml.load"""
        seq = self.construct_sequence(node)
        return ''.join([str(i) for i in seq])

    def load_sql(self, node):
        """macro to include !load_sql function to yaml.load"""
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as file_:
            return file_.read()
