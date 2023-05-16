from typing import TypeVar, Generic

from BaseDependencies import TransientDependency
from Container import Injectable
from BotConfig import BotConfig


class ModuleConfig(TransientDependency):
    __base_config__: BotConfig = Injectable[BotConfig]()

    def __getitem__(self, item: str):
        return self.__base_config__.module_configs[self.target_name][item]

    def __setitem__(self, key: str, value):
        self.__base_config__.module_configs[self.target_name][key] = value
        self.__base_config__.save()

    def __contains__(self, item):
        return item in self.__base_config__.module_configs[self.target_name]

    def save(self):
        self.__base_config__.save()
