import os.path
from typing import IO, List
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
        dir = self.get_full_path(name)
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def get_full_path(self, file: str):
        return os.path.join(os.path.join(self.base_dir, self.target_name), file)
    def list_files(self, path: str) -> List[str]:
        result = []
        dir = self.get_full_path(path)
        if not os.path.exists(dir):
            return result
        for root, dirs, files in os.walk(dir):
            for file in files:
                file_path = os.path.join(path, file)
                result.append(file_path)
        return result
