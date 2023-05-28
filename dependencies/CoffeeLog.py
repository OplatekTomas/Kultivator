from datetime import datetime
from enum import Enum
from typing import Dict, List


from BaseDependencies import SingletonDependency
from Container import Injectable
from dependencies.PersistentStorage import PersistentStorage
from dependencies.ModuleConfig import ModuleConfig

class CoffeeType(Enum):
    NORMAL = 1
    DOUBLE = 2
    INSTINCT = 3


class Coffee:
    timestamp: datetime
    kind: CoffeeType

class CoffeeLog(SingletonDependency):

    storage: PersistentStorage = Injectable[PersistentStorage]()
    config: ModuleConfig = Injectable[ModuleConfig]()
    data: Dict[int, List[Coffee]]

    def after_inject(self):
        if "dir" not in self.config:
            self.config["dir"] = "user_data"
        if "ext" not in self.config:
            self.config["ext"] = ".kafolog"
        dir = self.storage.create_dir(self.config["dir"])
        pass

    def add_coffee(self, user_id: int, coffee_type: CoffeeType):
        if user_id not in self.data:
            self.data[user_id] = list()
        with self.storage.load_file(f"{dir}/{user_id}/{self.config['ext']}", mode="a") as f:
            f.write("test\n")
    pass