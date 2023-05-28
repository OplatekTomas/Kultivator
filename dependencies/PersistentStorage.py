import os.path
from typing import IO
from BaseDependencies import TransientDependency


class PersistentStorage(TransientDependency):

    base_dir = "./storage"

    def load_file(self, path: str, mode: str = "r") -> IO:
        module_dir = f"{self.base_dir}/{self.target_name}/"
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)
        file_path = module_dir + path

        if not os.path.exists(file_path):
            with open(file_path, 'w') as fp:
                pass

        return open(file_path, mode)

    def create_dir(self, name: str):
        dir = f"{self.base_dir}/{self.target_name}/{name}"
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

