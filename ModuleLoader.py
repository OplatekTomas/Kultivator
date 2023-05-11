import glob
import importlib
import inspect
import os
from typing import List

import discord.ext.commands
from discord.ext.commands import Bot

from BaseDependencies import SingletonDependency, TransientDependency
from BaseModule import BaseModule
from BotConfig import BotConfig
from Container import DependencyContainer


class ModuleLoader:

    modules: List[BaseModule]
    container: DependencyContainer
    config: BotConfig
    client: discord.ext.commands.Bot

    def __init__(self, config: BotConfig, client: discord.ext.commands.Bot):
        self.modules = []
        self.config = config
        self.client = client
        pass

    def init_di_container(self):
        self.container = DependencyContainer()
        self.container.add_constant(self.client)
        self.container.add_constant(self.config)
        pass

    def load_dependencies(self):
        deps = glob.glob('./dependencies/*.py')
        for dependency in deps:
            dependency_name = os.path.basename(dependency).split('.')[0]
            spec = importlib.util.spec_from_file_location("dependencies." + dependency_name, dependency)
            dep = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dep)
            if not dir(dep).__contains__(dependency_name):
                pass
            for name, t in inspect.getmembers(dep):
                if inspect.isclass(t) and issubclass(t, SingletonDependency):
                    self.container.add_singleton(t, False)
                elif inspect.isclass(t) and issubclass(t, TransientDependency):
                    self.container.add_transient(t)
        for t, instance in self.container.singletons.items():
            self.container.inject_into(instance)
        pass

    async def import_modules(self):
        modules = glob.glob('./modules/*Module.py')
        module_list = []
        module_names = []
        for module in modules:
            module_name = os.path.basename(module).split('.')[0]
            spec = importlib.util.spec_from_file_location(module_name, module)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if not dir(module).__contains__(module_name):
                pass
            for name, t in inspect.getmembers(module):
                if inspect.isclass(t) and issubclass(t, BaseModule) and t != BaseModule:
                    module_names.append(name)
                    module_list.append(t)
        for module in module_list:
            self.client.load_extension("modules." + module.__name__)
            pass
        for name in self.client._CogMixin__cogs:
            instance = self.client.get_cog(name)
            self.container.inject_into(instance)
            self.modules.append(instance)

        for name in module_names:
            self.config.handle_config_creation(name)
        self.config.save()

