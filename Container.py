from typing import Type, TypeVar, Generic, TypedDict, List, Dict, get_type_hints, get_args

from typing_inspect import get_generic_type, get_generic_bases
import discord
import BotConfig
import inspect


from typing import TypeVar, Generic

T = TypeVar('T')


class Injectable(Generic[T]):
    pass


class DependencyContainer:
    singletons: Dict[str, object] = dict()
    transients: List[Type] = list()
    unloaded_dependencies: List[Type]

    def add_singleton(self, t: Type, immediate_inject: bool = True):
        if t in self.singletons:
            return
        instance = t()
        self.singletons[t.__name__] = instance
        if immediate_inject:
            self.inject_into(instance)

    def add_constant(self, obj: object):
        if obj.__class__ in self.singletons:
            return
        self.singletons[obj.__class__.__name__] = obj

    def add_transient(self, t: Type):
        if t not in self.transients:
            self.transients.append(t)

    def inject_into(self, obj: object):
        props = self.get_injectable_props(obj)
        for name in props:
            prop = props[name]
            generic_type = get_args(get_generic_type(prop))
            if generic_type[0].__name__ in [x for x in self.singletons]:
                setattr(obj, name, self.singletons[generic_type[0].__name__])
            elif generic_type[0].__name__ in [x.__name__ for x in self.transients]:
                instance = generic_type[0](type(obj).__name__)
                self.inject_into(instance)
                setattr(obj, name, instance)
            else:
                setattr(obj, name, None)
        if hasattr(obj, 'after_inject') and callable(obj.after_inject):
            obj.after_inject()
    pass

    def get_injectable_props(self, o: object):
        return {
            name: value for name, value in vars(type(o)).items()
            if isinstance(value, Injectable)
        }
