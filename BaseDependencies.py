

class SingletonDependency:
    pass


class TransientDependency:

    target_name: str

    def __init__(self, name: str):
        self.target_name = name
        pass
