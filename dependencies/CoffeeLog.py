import glob
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List


from BaseDependencies import SingletonDependency
from Container import Injectable
from dependencies.PersistentStorage import PersistentStorage
from dependencies.ModuleConfig import ModuleConfig

class CoffeeType(Enum):
    NORMAL = 1
    DOUBLE = 2
    INSTINCT = 2
    ENERGY = 4


class Coffee:
    timestamp: datetime
    kind: CoffeeType

    def __init__(self, kind: CoffeeType = None):
        self.kind = kind
        self.timestamp = datetime.now()

    def from_str(self, csv: str):
        parts = csv.strip().split(";")
        self.timestamp = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S.%f")
        self.kind = CoffeeType[parts[1]]
        pass

    def to_str(self) -> str:
        return f"{self.timestamp};{self.kind.name}"


class CoffeeLog(SingletonDependency):

    storage: PersistentStorage = Injectable[PersistentStorage]()
    config: ModuleConfig = Injectable[ModuleConfig]()
    data: Dict[int, List[Coffee]] = dict()

    def after_inject(self):
        if "dir" not in self.config:
            self.config["dir"] = "user_data"
        if "ext" not in self.config:
            self.config["ext"] = ".kafolog"
        self.prepare_directory()
        self.parse_legacy()

    def prepare_directory(self):
        dir = self.storage.create_dir(self.config["dir"])
        for file in glob.glob(f"{dir}/*{self.config['ext']}"):
            with open(file, "r") as f:
                name = Path(file).stem
                user_id = int(name)
                self.data[user_id] = list()
                for line in f.readlines():
                    c = Coffee()
                    c.from_str(line)
                    self.data[user_id].append(c)

    def parse_legacy(self):
        if "KafoModule" not in self.config.__base_config__.module_configs or "score" not in self.config.__base_config__.module_configs["KafoModule"]:
            return
        for user_id in self.config.__base_config__.module_configs["KafoModule"]["score"]:
            for i in range(self.config.__base_config__.module_configs["KafoModule"]["score"][user_id]):
                self.add_coffee(int(user_id), CoffeeType.NORMAL)
        self.config.__base_config__.module_configs["KafoModule"].pop("score")
        self.config.save()

    def add_coffee(self, user_id: int, coffee_type: CoffeeType):
        if user_id not in self.data:
            self.data[user_id] = list()
        coffee = Coffee(coffee_type)
        with self.storage.load_file(f"{self.config['dir']}/{user_id}{self.config['ext']}", mode="a") as f:
            f.write(coffee.to_str() + "\n")
        self.data[user_id].append(coffee)
    pass